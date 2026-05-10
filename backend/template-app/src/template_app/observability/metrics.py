from __future__ import annotations

import time

import psutil
from fastapi import APIRouter

router = APIRouter()


@router.get("/metrics")
def metrics():
    process = psutil.Process()

    return {
        "uptime_seconds": time.time() - process.create_time(),
        "cpu_percent": process.cpu_percent(interval=0.1),
        "memory_rss_mb": process.memory_info().rss / 1024 / 1024,
        "memory_vms_mb": process.memory_info().vms / 1024 / 1024,
        "open_fds": process.num_fds() if hasattr(process, "num_fds") else None,
        "threads": process.num_threads(),
    }
