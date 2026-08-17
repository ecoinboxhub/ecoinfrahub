"""Run EcoInfraMind AI API server."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uvicorn
from config.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False,
        log_level="info",
    )
