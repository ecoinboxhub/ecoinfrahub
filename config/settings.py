import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        protected_namespaces=("settings_",),
    )

    app_name: str = "EcoInfraMind AI"
    version: str = "1.0.0"
    debug: bool = False

    base_dir: Path = Path(__file__).resolve().parent.parent

    models_dir: Path = base_dir / "models"
    knowledge_dir: Path = base_dir / "knowledge"
    documents_dir: Path = base_dir / "documents"
    embeddings_dir: Path = base_dir / "embeddings"
    database_dir: Path = base_dir / "database"
    evaluation_dir: Path = base_dir / "evaluation"

    model_path: Path = base_dir / "model" / "ecoinframind-ai-model.gguf"
    embedding_model: str = "all-MiniLM-L6-v2"  # offline-safe; avoid nomic-embed-text (requires HF auth, breaks internet-free rule)
    embedding_model_fallback: str = "all-MiniLM-L6-v2"

    chroma_host: str = "localhost"
    chroma_port: int = 8000
    chroma_collection: str = "ecoinframind_knowledge"

    n_ctx: int = 4096
    n_threads: int = 8
    n_batch: int = 1024

    max_tokens: int = 512
    temperature: float = 0.3
    top_p: float = 0.8
    top_k: int = 16
    repeat_penalty: float = 1.0
    do_sample: bool = True

    chunk_size: int = 1500
    chunk_overlap: int = 128
    max_retrieved: int = 3

    retrieval_top_k: int = 6
    rerank_top_k: int = 5
    similarity_threshold: float = 0.40

    retrieval_validate: bool = True
    context_verify: bool = True
    hallucination_detect: bool = True
    second_verification_pass: bool = False

    reranker_model: str = "BAAI/bge-reranker-base"
    reranker_enabled: bool = False
    reranker_device: str = "cpu"

    max_ram_gb: float = 3.5
    cache_ttl: int = 3600

    upload_max_size_mb: int = 50
    supported_formats: list[str] = ["pdf", "docx", "txt", "md"]

    api_host: str = "127.0.0.1"
    api_port: int = 8432


settings = Settings()
