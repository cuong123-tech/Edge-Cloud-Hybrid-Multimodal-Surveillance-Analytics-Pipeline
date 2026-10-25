import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EdgeStats:
    frames_received: int = 0
    _fps_ema: float = 0.0
    _last_frame_ts: Optional[float] = None
    camera_id: Optional[str] = None
    _ema_alpha: float = 0.2

    def record_frame(self) -> None:
        now = time.monotonic()
        self.frames_received += 1
        if self._last_frame_ts is not None:
            dt = now - self._last_frame_ts
            if dt > 0:
                instant_fps = 1.0 / dt
                if self._fps_ema <= 0:
                    self._fps_ema = instant_fps
                else:
                    self._fps_ema = (
                        self._ema_alpha * instant_fps
                        + (1 - self._ema_alpha) * self._fps_ema
                    )
        self._last_frame_ts = now

    @property
    def fps_ema(self) -> float:
        return round(self._fps_ema, 2)


edge_stats = EdgeStats()
