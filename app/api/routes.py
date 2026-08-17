from __future__ import annotations
import orjson
import json
import asyncio
import re
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel
from app.backend.engine import llm_engine
from app.backend.rag import rag_engine, _clean_response
from app.backend.documents import document_processor
from app.backend.assistants import get_expert_response, SYSTEM_PROMPTS
from app.backend.languages import get_language_prompt, SUPPORTED_LANGUAGES
from app.backend import calculators
from utils.logger import logger
from utils.monitor import get_cpu_usage, get_ram_usage_gb, Timer
from config.settings import settings
from pathlib import Path
import shutil
import time

router = APIRouter()


def clean_text(text: str) -> str:
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

def oj(data) -> Response:
    return Response(orjson.dumps(data), media_type="application/json")


class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []
    language: str = "english"


class ExpertRequest(BaseModel):
    message: str
    expert_type: str = "engineering"
    history: List[dict] = []


class CalculatorRequest(BaseModel):
    calculator: str
    params: dict


@router.get("/health")
async def health():
    return oj({
        "status": "ok",
        "model_loaded": llm_engine.is_loaded,
        "cpu_percent": get_cpu_usage(),
        "ram_gb": round(get_ram_usage_gb(), 2),
    })


@router.post("/chat")
async def chat(request: ChatRequest):
    timer = Timer()
    timer.start = time.perf_counter()

    result = rag_engine.generate_grounded_response(request.message, request.history, request.language)

    response_text = clean_text(result["response"]).strip()
    elapsed = time.perf_counter() - timer.start

    return oj({
        "response": response_text,
        "evidence": result.get("evidence", ""),
        "answer": result.get("answer", ""),
        "confidence": result.get("confidence", ""),
        "cpu_percent": get_cpu_usage(),
        "ram_gb": round(get_ram_usage_gb(), 2),
        "response_time_s": round(elapsed, 3),
        "tokens": result.get("tokens", llm_engine.count_tokens(response_text)),
        "sources": result.get("sources", []),
        "retrieval_failure": result.get("retrieval_failure", False),
    })


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    t_start = time.perf_counter()

    retrieved = rag_engine.retrieve(request.message)
    quality = rag_engine._assess_retrieval_quality(retrieved)
    context = rag_engine.build_context(retrieved)
    prompt = rag_engine._build_prompt(request.message, context, quality, request.language)

    messages = [{"role": "user", "content": prompt}]
    if request.history:
        messages = request.history[-2:] + messages

    sources = [
        {"source": d["source"], "relevance": f"{d.get('similarity', 0):.0%}"}
        for d in retrieved
        if d.get('similarity', 0) > 0 and quality in ("strong", "weak")
    ]

    async def generate():
        if sources:
            yield f"data: {json.dumps({'sources': sources})}\n\n"

        collected = []
        for token in llm_engine.generate(messages, stream=True):
            collected.append(token)
            yield f"data: {json.dumps({'token': token})}\n\n"

        raw_output = _clean_response("".join(collected))
        elapsed = time.perf_counter() - t_start

        meta = {
            "tokens": llm_engine.count_tokens(raw_output),
            "time": round(elapsed, 3),
            "cpu": get_cpu_usage(),
            "ram": round(get_ram_usage_gb(), 2),
            "sources": sources,
        }
        yield f"data: {json.dumps({'meta': meta})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.post("/expert")
async def expert(request: ExpertRequest):
    timer = Timer()
    timer.start = time.perf_counter()

    collected = []
    for token in get_expert_response(request.message, request.expert_type, request.history, stream=False):
        collected.append(token)

    response_text = clean_text("".join(collected)).strip()
    elapsed = time.perf_counter() - timer.start

    return oj({
        "response": response_text,
        "expert_type": request.expert_type,
        "cpu_percent": get_cpu_usage(),
        "ram_gb": round(get_ram_usage_gb(), 2),
        "response_time_s": round(elapsed, 3),
        "tokens": llm_engine.count_tokens(response_text),
    })


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower().lstrip(".")
    if ext not in settings.supported_formats:
        raise HTTPException(400, f"Unsupported format: {ext}. Supported: {settings.supported_formats}")

    save_path = settings.documents_dir / file.filename
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)

    chunks = document_processor.process_file(save_path)
    if not chunks:
        return oj({"filename": file.filename, "chunks_indexed": 0, "status": "no text extracted"})

    indexed = rag_engine.index_document_chunks(chunks)
    return oj({
        "filename": file.filename,
        "chunks_indexed": indexed,
        "status": "indexed" if indexed > 0 else "failed",
    })


@router.get("/knowledge/stats")
async def knowledge_stats():
    return oj(rag_engine.get_knowledge_stats())


@router.post("/knowledge/clear")
async def clear_knowledge():
    success = rag_engine.clear_knowledge_base()
    return oj({"status": "cleared" if success else "failed"})


@router.post("/knowledge/index-all")
async def index_all():
    count = 0
    for file_path in document_processor.scan_knowledge_base():
        chunks = document_processor.process_file(file_path)
        if chunks:
            indexed = rag_engine.index_document_chunks(chunks)
            count += indexed
    return oj({"files_indexed": count, "status": "completed"})


@router.post("/calculator")
async def calculate(request: CalculatorRequest):
    calc_name = request.calculator
    params = request.params

    calc_functions = {
        "concrete_mix": calculators.concrete_mix_ratio,
        "traffic_volume": calculators.traffic_volume,
        "aadt": calculators.aadt_calculation,
        "pavement_thickness": calculators.pavement_thickness,
        "earthwork": calculators.earthwork_volume,
        "drainage": calculators.drainage_flow,
        "unit_conversion": calculators.unit_conversion,
        "bearing_capacity": calculators.bearing_capacity,
        "area": calculators.area_calculation,
        "volume": calculators.volume_calculation,
        "slope": calculators.slope_calculation,
    }

    func = calc_functions.get(calc_name)
    if not func:
        raise HTTPException(400, f"Unknown calculator: {calc_name}")

    try:
        result = func(**params)
    except Exception as e:
        raise HTTPException(400, f"Calculation error: {e}")

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(400, result["error"])

    return oj({
        "result": result,
        "cpu_percent": get_cpu_usage(),
        "ram_gb": round(get_ram_usage_gb(), 2),
    })


@router.get("/experts")
async def list_experts():
    return oj({"experts": list(SYSTEM_PROMPTS.keys())})


@router.get("/languages")
async def list_languages():
    return oj({"languages": SUPPORTED_LANGUAGES})


@router.get("/metrics")
async def metrics():
    return oj({
        "cpu_percent": get_cpu_usage(),
        "ram_gb": round(get_ram_usage_gb(), 2),
        "ram_percent": round(get_ram_usage_gb() / settings.max_ram_gb * 100, 1),
        "model_loaded": llm_engine.is_loaded,
        "cache_size": rag_engine.cache.size,
        "knowledge_stats": rag_engine.get_knowledge_stats(),
    })
