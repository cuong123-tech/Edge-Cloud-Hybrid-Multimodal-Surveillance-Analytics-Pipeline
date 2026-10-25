"""Send one JPEG file over the edge WebSocket (smoke test without browser)."""

import argparse
import asyncio
import json
import sys
from pathlib import Path

import websockets

JPEG_MAGIC = b"\xff\xd8"


async def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "jpeg",
        type=Path,
        help="Path to a .jpg / .jpeg file",
    )
    parser.add_argument(
        "--url",
        default="ws://localhost:8000/ws/frames",
        help="WebSocket URL",
    )
    args = parser.parse_args()

    data = args.jpeg.read_bytes()
    if len(data) < 2 or data[:2] != JPEG_MAGIC:
        print("Not a JPEG file (missing FF D8 magic)", file=sys.stderr)
        return 1

    async with websockets.connect(args.url) as ws:
        await ws.send(
            json.dumps(
                {
                    "type": "session_start",
                    "camera_id": "test-script",
                    "client_fps_cap": 12,
                }
            )
        )
        await ws.send(data)
        reply = await ws.recv()
        print(reply)

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
