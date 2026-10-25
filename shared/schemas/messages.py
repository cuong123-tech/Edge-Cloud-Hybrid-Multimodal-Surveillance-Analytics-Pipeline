from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, Field


class ActivityState(str, Enum):
    """Stub for week 2+ activity classification."""

    unknown = "unknown"


class SessionStart(BaseModel):
    type: Literal["session_start"] = "session_start"
    camera_id: str = "laptop-01"
    client_fps_cap: int = Field(default=12, ge=1, le=60)


class FrameAck(BaseModel):
    type: Literal["frame_ack"] = "frame_ack"
    ok: bool
    ts_server_ms: int
    seq: int
    bytes: Optional[int] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: str = "edge-inference"


class StatsResponse(BaseModel):
    frames_received: int
    fps_ema: float
    camera_id: Optional[str] = None
