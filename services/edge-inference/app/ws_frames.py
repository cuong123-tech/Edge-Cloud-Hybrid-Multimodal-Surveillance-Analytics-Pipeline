import json
import time

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from shared.schemas.messages import FrameAck, SessionStart
from app.stats import edge_stats

router = APIRouter()

JPEG_MAGIC = b"\xff\xd8"


@router.websocket("/ws/frames")
async def ws_frames(websocket: WebSocket) -> None:
    await websocket.accept()
    seq = 0

    try:
        while True:
            message = await websocket.receive()
            if message.get("type") == "websocket.disconnect":
                break

            if message.get("text") is not None:
                text = message["text"]
                try:
                    data = json.loads(text)
                    if data.get("type") == "session_start":
                        session = SessionStart.model_validate(data)
                        edge_stats.camera_id = session.camera_id
                except (json.JSONDecodeError, ValidationError):
                    pass
                continue

            raw = message.get("bytes")
            if raw is None:
                continue

            seq += 1
            ts_ms = int(time.time() * 1000)
            nbytes = len(raw)

            if len(raw) < 2 or raw[:2] != JPEG_MAGIC:
                ack = FrameAck(
                    ok=False,
                    ts_server_ms=ts_ms,
                    seq=seq,
                    bytes=nbytes,
                    error="invalid_jpeg",
                )
                await websocket.send_text(ack.model_dump_json())
                continue

            edge_stats.record_frame()
            ack = FrameAck(
                ok=True,
                ts_server_ms=ts_ms,
                seq=seq,
                bytes=nbytes,
            )
            await websocket.send_text(ack.model_dump_json())
    except WebSocketDisconnect:
        pass
