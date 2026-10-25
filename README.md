# Edge-Cloud Hybrid Multimodal Surveillance

A proof-of-concept pipeline that streams webcam frames from the browser to an edge inference service, then layers pose-based activity rules and (later) hybrid text/vision models to detect focus and distraction—with contextual alerts delivered over Telegram. Development is **local-first**; Docker packaging comes after the core path is stable.

## What this project explores

- **Edge:** Low-latency pose and rule-based state (`focused`, `maybe_distracted`, `away`) on ONNX Runtime.
- **Cloud / hybrid:** Route uncertain cases through a cascade (lightweight LLM or VLM) instead of sending every frame upstream.
- **Engineering:** Shared JSON contracts between services, measurable latency/FPS, and optional FP32 vs INT8 pose benchmarks.
- **Product shape:** A small web dashboard plus optional event logging and notifier integration.

This is a learning and portfolio build—not a production multi-camera or compliance-ready surveillance product. Use it only on devices and scenes you are allowed to record; see the plan doc for privacy notes.

## Architecture (target)

```
Browser (getUserMedia) → edge-inference (pose, rules)
                              → orchestrator (debounce, routing)
                                    → VLM worker / notifier (e.g. Telegram)
                              → dashboard API
```

**Current milestone (week 1):** React frontend streams JPEG frames over WebSocket to a FastAPI edge stub that acknowledges and tracks throughput.

## Quick start

1. Run **edge-inference** and **frontend** as described in [docs/DEV_LOCAL.md](docs/DEV_LOCAL.md).
2. Open http://localhost:5173, start the camera, and confirm WebSocket acks at roughly 10–15 fps.
