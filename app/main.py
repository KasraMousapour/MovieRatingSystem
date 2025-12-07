from fastapi import FastAPI
import uvicorn
from api.routers import api_router

app = FastAPI(
    title="Movie Rating system",
    description="FastAPI backend for rating movies",
    version="1.0.0"
)

app.include_router(api_router)

def run_api(host: str = "127.0.0.1", port: int = 8000, reload: bool = True, workers: int = 1):
    # Run FastAPI app via import string so reload/workers work
    uvicorn.run("main:app", host=host, port=port, reload=reload, workers=workers)

if __name__ == "__main__":
    run_api()    