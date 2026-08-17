#!/usr/bin/env python3
"""Performance benchmark for EcoInfraMind AI."""

from __future__ import annotations
import sys
import time
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.logger import logger
from utils.monitor import get_cpu_usage, get_ram_usage_gb, Timer
from app.backend.engine import llm_engine
from app.backend.embeddings import embedding_engine
from app.backend.documents import document_processor
from app.backend.rag import rag_engine

BENCHMARK_QUESTIONS = [
    "What is the minimum CBR for highway subgrade in Nigeria?",
    "Design a concrete mix for a bridge foundation.",
    "Calculate the drainage flow for a 50ha catchment with C=0.6 and 50mm/hr rainfall.",
    "What is the recommended pavement thickness for 5 million ESA on CBR 15?",
    "Explain climate-resilient road design principles.",
    "What are the geometric standards for rural highways in Nigeria?",
    "How do you calculate bearing capacity of shallow foundations?",
    "What is the design life for flexible pavements in Nigeria?",
]

QUALITY_QUESTIONS = [
    {
        "question": "What is the standard pavement structure for a rural road in Nigeria?",
        "expected_keywords": ["subgrade", "subbase", "base", "surface", "thickness"],
        "category": "highway_engineering",
    },
    {
        "question": "Explain the Rational Method for calculating stormwater runoff.",
        "expected_keywords": ["runoff", "coefficient", "intensity", "area", "peak flow"],
        "category": "hydrology",
    },
    {
        "question": "What are the key properties of concrete for bridge construction?",
        "expected_keywords": ["strength", "durability", "workability", "cement", "aggregate"],
        "category": "materials_engineering",
    },
    {
        "question": "How do you assess flood risk for an urban drainage system?",
        "expected_keywords": ["return period", "design storm", "capacity", "overflow"],
        "category": "environmental_engineering",
    },
]


def benchmark_inference():
    logger.info("Benchmarking inference...")
    if not llm_engine.load():
        logger.error("Model not available, skipping inference benchmark")
        return None

    results = []
    for question in BENCHMARK_QUESTIONS:
        ram_before = get_ram_usage_gb()
        cpu_before = get_cpu_usage()

        timer = Timer()
        with timer:
            response = "".join(list(llm_engine.generate(
                [{"role": "user", "content": f"Answer briefly: {question}"}],
                stream=False
            )))

        ram_after = get_ram_usage_gb()
        cpu_after = get_cpu_usage()
        tokens = llm_engine.count_tokens(response)

        result = {
            "question": question[:50],
            "response_length": len(response),
            "tokens": tokens,
            "time_s": round(timer.elapsed, 3),
            "ram_before_gb": round(ram_before, 2),
            "ram_after_gb": round(ram_after, 2),
            "ram_delta_gb": round(ram_after - ram_before, 2),
            "cpu_percent": cpu_after,
            "tokens_per_second": round(tokens / timer.elapsed, 2) if timer.elapsed > 0 else 0,
        }
        results.append(result)
        logger.info(f"  Q: {question[:40]}... | Time: {timer.elapsed:.2f}s | RAM: {ram_after:.2f}GB | TPS: {result['tokens_per_second']}")

    return results


def benchmark_rag():
    logger.info("Benchmarking RAG pipeline...")
    results = []

    for question in BENCHMARK_QUESTIONS[:4]:
        timer = Timer()
        with timer:
            retrieved = rag_engine.retrieve(question)
            context = rag_engine.build_context(retrieved)

        result = {
            "question": question[:50],
            "retrieved_docs": len(retrieved),
            "context_length": len(context),
            "retrieval_time_s": round(timer.elapsed, 3),
        }
        results.append(result)
        logger.info(f"  Q: {question[:40]}... | Docs: {len(retrieved)} | Time: {timer.elapsed:.3f}s")

    return results


def benchmark_embeddings():
    logger.info("Benchmarking embeddings...")
    if not embedding_engine.load():
        logger.error("Embedding model not available")
        return None

    texts = [
        "Highway pavement design standards in Nigeria",
        "Climate adaptation strategies for road infrastructure",
        "Concrete mix design for tropical environments",
        "Flood risk assessment methodology for urban drainage",
        "Sustainable construction materials for African infrastructure",
    ]

    timer = Timer()
    with timer:
        embeddings = embedding_engine.embed_batch(texts)

    result = {
        "texts": len(texts),
        "embedding_dim": len(embeddings[0]) if embeddings else 0,
        "time_s": round(timer.elapsed, 3),
        "texts_per_second": round(len(texts) / timer.elapsed, 1) if timer.elapsed > 0 else 0,
    }
    logger.info(f"  Embedded {len(texts)} texts in {timer.elapsed:.3f}s")
    return result


def benchmark_quality():
    logger.info("Benchmarking response quality...")
    if not llm_engine.load():
        logger.error("Model not available, skipping quality benchmark")
        return None

    results = []
    for item in QUALITY_QUESTIONS:
        timer = Timer()
        with timer:
            retrieved = rag_engine.retrieve(item["question"])
            context = rag_engine.build_context(retrieved)

            if context:
                prompt = f"Based on the following context, answer the question.\n\nContext:\n{context}\n\nQuestion: {item['question']}\n\nAnswer:"
            else:
                prompt = f"Answer briefly: {item['question']}"

            response = "".join(list(llm_engine.generate(
                [{"role": "user", "content": prompt}],
                stream=False
            )))

        response_lower = response.lower()
        keywords_found = [kw for kw in item["expected_keywords"] if kw.lower() in response_lower]
        keyword_score = len(keywords_found) / len(item["expected_keywords"]) if item["expected_keywords"] else 0

        result = {
            "question": item["question"][:50],
            "category": item["category"],
            "response_length": len(response),
            "time_s": round(timer.elapsed, 3),
            "keywords_expected": len(item["expected_keywords"]),
            "keywords_found": len(keywords_found),
            "keyword_coverage": round(keyword_score, 2),
            "response_preview": response[:200],
        }
        results.append(result)
        logger.info(f"  Q: {item['question'][:40]}... | Keywords: {len(keywords_found)}/{len(item['expected_keywords'])} | Coverage: {keyword_score:.0%}")

    return results


def main():
    logger.info("=" * 60)
    logger.info("  EcoInfraMind AI Performance Benchmark")
    logger.info("=" * 60)

    results = {}

    emb_results = benchmark_embeddings()
    if emb_results:
        results["embeddings"] = emb_results

    rag_results = benchmark_rag()
    if rag_results:
        results["rag"] = rag_results

    inf_results = benchmark_inference()
    if inf_results:
        results["inference"] = inf_results

    qual_results = benchmark_quality()
    if qual_results:
        results["quality"] = qual_results

    output_path = Path(__file__).parent / "benchmark_results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    logger.info(f"\nResults saved to {output_path}")

    if inf_results:
        avg_time = sum(r["time_s"] for r in inf_results) / len(inf_results)
        avg_ram = sum(r["ram_after_gb"] for r in inf_results) / len(inf_results)
        avg_tokens = sum(r["tokens"] for r in inf_results) / len(inf_results)
        avg_tps = sum(r["tokens_per_second"] for r in inf_results) / len(inf_results)
        logger.info(f"\nInference Summary:")
        logger.info(f"  Average response time: {avg_time:.2f}s")
        logger.info(f"  Average RAM: {avg_ram:.2f}GB")
        logger.info(f"  Average tokens: {avg_tokens:.0f}")
        logger.info(f"  Average tokens/sec: {avg_tps:.2f}")

    if qual_results:
        avg_coverage = sum(r["keyword_coverage"] for r in qual_results) / len(qual_results)
        logger.info(f"\nQuality Summary:")
        logger.info(f"  Average keyword coverage: {avg_coverage:.0%}")


if __name__ == "__main__":
    main()
