from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shared.schemas.messages import HealthResponse, StatsResponse
from app.config import settings
from app.stats import edge_stats
from app.ws_frames import router as ws_router

app = FastAPI(title="edge-inference", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws_router)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@app.get("/stats", response_model=StatsResponse)
def stats() -> StatsResponse:
    return StatsResponse(
        frames_received=edge_stats.frames_received,
        fps_ema=edge_stats.fps_ema,
        camera_id=edge_stats.camera_id,
    )
