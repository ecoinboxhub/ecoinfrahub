from __future__ import annotations
import re
import time
from typing import List, Generator, Optional
from config.settings import settings
from app.backend.embeddings import embedding_engine
from app.backend.engine import llm_engine
from app.backend.languages import get_language_prompt
from utils.logger import logger
from utils.cache import ResponseCache


def _normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip().lower()


def _strip_think(text: str) -> str:
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()


def _clean_response(text: str) -> str:
    text = _strip_think(text)
    for prefix in ["Evidence:", "Answer:", "Confidence:"]:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'~~(.*?)~~', r'\1', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


class RAGEngine:
    def __init__(self):
        self.cache = ResponseCache(ttl=settings.cache_ttl)
        self._collection = None

    def _get_collection(self):
        if self._collection is None:
            import chromadb
            client = chromadb.PersistentClient(path=str(settings.database_dir))
            self._collection = client.get_or_create_collection(
                name=settings.chroma_collection,
                metadata={"hnsw:space": "cosine"},
            )
        return self._collection

    def index_document_chunks(self, chunks: List[dict]) -> int:
        collection = self._get_collection()
        texts = [c["text"] for c in chunks]
        ids = [c["chunk_id"] for c in chunks]
        metadatas = [{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks]
        try:
            embeddings = embedding_engine.embed_batch(texts)
            collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids,
            )
            logger.info(f"Indexed {len(chunks)} chunks into ChromaDB")
            return len(chunks)
        except Exception as e:
            logger.error(f"Indexing error: {e}")
            return 0

    def retrieve(self, query: str, k: int | None = None) -> List[dict]:
        if k is None:
            k = settings.retrieval_top_k
        collection = self._get_collection()
        query_embedding = embedding_engine.embed(query)
        try:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                include=["documents", "metadatas", "distances"],
            )
            docs = []
            if results["documents"] and results["documents"][0]:
                for i in range(len(results["documents"][0])):
                    sim = 1.0 - results["distances"][0][i] if results["distances"] else 0.0
                    if sim >= settings.similarity_threshold * 0.5:
                        docs.append({
                            "text": results["documents"][0][i],
                            "source": results["metadatas"][0][i].get("source", "unknown"),
                            "chunk_index": results["metadatas"][0][i].get("chunk_index", 0),
                            "similarity": sim,
                        })
            docs.sort(key=lambda d: d["similarity"], reverse=True)
            # Deduplicate by source (keep the highest-scoring chunk per document)
            seen = set()
            deduped = []
            for d in docs:
                if d["source"] not in seen:
                    seen.add(d["source"])
                    deduped.append(d)
            return deduped[:settings.rerank_top_k]
        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            return []

    def _assess_retrieval_quality(self, documents: List[dict]) -> str:
        if not documents:
            return "none"
        best_sim = max(d.get("similarity", 0.0) for d in documents)
        if best_sim >= settings.similarity_threshold:
            return "strong"
        elif best_sim >= settings.similarity_threshold * 0.6:
            return "weak"
        else:
            return "minimal"

    def _build_prompt(self, query: str, context: str, quality: str, language: str = "english") -> str:
        lang = get_language_prompt(language)
        if quality == "strong":
            return lang["context_prompt"].format(context=context, query=query)
        elif quality == "weak":
            return lang["no_context_prompt"].format(context=context, query=query)
        else:
            # Ground even weak/no retrieval in available context and instruct the
            # model to answer from the context first. This prevents unfounded
            # (hallucinated) specifications when retrieval is only partial.
            grounded = lang["no_context_prompt"].format(context=context, query=query)
            if context.strip():
                return (
                    f"{grounded}\n\n"
                    "Answer strictly from the context above. If the context does not "
                    "contain the answer, say so clearly rather than guessing."
                )
            return (
                f"{lang['system']}\n\n"
                f"{lang['greeting_rules']}\n\n"
                f"Question: {query}\n\n"
                "Answer in plain text:"
            )

    def build_context(self, retrieved_docs: List[dict]) -> str:
        if not retrieved_docs:
            return ""
        parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            text = doc["text"]
            if len(text) > 900:
                text = text[:900].rstrip()
            parts.append(f"[{i}] {text}")
        return "\n\n".join(parts)

    def generate_grounded_response(self, query: str, history: List[dict] | None = None, language: str = "english") -> dict:
        t_start = time.perf_counter()
        log_entry = {"question": query}

        cached = self.cache.get(query, language=language)
        if cached is not None:
            cached["response_time_s"] = round(time.perf_counter() - t_start, 3)
            return cached

        retrieved = self.retrieve(query)
        log_entry["similarity_scores"] = [round(d.get("similarity", 0), 3) for d in retrieved]

        quality = self._assess_retrieval_quality(retrieved)

        context = self.build_context(retrieved)
        prompt = self._build_prompt(query, context, quality, language)

        messages = [{"role": "user", "content": prompt}]
        if history:
            messages = history[-2:] + messages

        collected = []
        for token in llm_engine.generate(messages, stream=False):
            collected.append(token)
        raw_output = _clean_response("".join(collected))

        if quality in ("strong", "weak"):
            sources = [
                {"source": d["source"], "relevance": f"{d.get('similarity', 0):.0%}"}
                for d in retrieved
                if d.get('similarity', 0) > 0
            ]
        else:
            sources = []

        result = {
            "response": raw_output,
            "evidence": "",
            "answer": raw_output,
            "confidence": "",
            "sources": sources,
            "response_time_s": round(time.perf_counter() - t_start, 3),
            "tokens": llm_engine.count_tokens(raw_output),
            "retrieval_failure": False,
            "retrieval_quality": quality,
        }

        self.cache.set(query, result, language=language)
        log_entry["final_answer"] = raw_output[:200]
        logger.info(f"RAG log: {log_entry}")
        return result

    def get_knowledge_stats(self) -> dict:
        try:
            collection = self._get_collection()
            count = collection.count()
            return {"total_chunks": count, "status": "ready" if count > 0 else "empty"}
        except Exception as e:
            return {"total_chunks": 0, "status": f"error: {e}"}

    def clear_knowledge_base(self) -> bool:
        try:
            import chromadb
            client = chromadb.PersistentClient(path=str(settings.database_dir))
            client.delete_collection(settings.chroma_collection)
            self._collection = None
            self.cache.clear()
            logger.info("Knowledge base and cache cleared")
            return True
        except Exception as e:
            logger.error(f"Failed to clear knowledge base: {e}")
            return False


rag_engine = RAGEngine()
