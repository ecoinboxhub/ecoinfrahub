"""Index all knowledge documents into ChromaDB vector store."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.settings import settings
from utils.logger import logger, setup_logger
from app.backend.documents import document_processor
from app.backend.embeddings import embedding_engine
from app.backend.rag import rag_engine

logger = setup_logger("indexer")

def main():
    start = time.time()
    logger.info("=" * 60)
    logger.info("  EcoInfraMind AI - Knowledge Base Indexer")
    logger.info("=" * 60)

    total_indexed = 0
    kb_path = settings.knowledge_dir
    files = sorted(kb_path.glob("*.md"))

    if not files:
        logger.warning(f"No markdown files found in {kb_path}")
        return

    logger.info(f"Found {len(files)} documents to index")

    for file_path in files:
        logger.info(f"Processing: {file_path.name}")
        chunks = document_processor.process_file(file_path)
        if chunks:
            count = rag_engine.index_document_chunks(chunks)
            total_indexed += count
            logger.info(f"  -> Indexed {count} chunks")
        else:
            logger.warning(f"  -> No text extracted")

    elapsed = time.time() - start
    stats = rag_engine.get_knowledge_stats()

    logger.info("=" * 60)
    logger.info(f"  Indexing complete!")
    logger.info(f"  Documents processed: {len(files)}")
    logger.info(f"  Total chunks indexed: {total_indexed}")
    logger.info(f"  ChromaDB collection size: {stats['total_chunks']}")
    logger.info(f"  Time: {elapsed:.1f}s")
    logger.info("=" * 60)

    # Unload embedding model to free RAM
    embedding_engine.unload()
    logger.info("Embedding model unloaded to free memory")

if __name__ == "__main__":
    main()
