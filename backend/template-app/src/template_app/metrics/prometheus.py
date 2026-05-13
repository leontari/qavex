"""
Prometheus metrics definitions.
"""

from prometheus_client import Counter
from prometheus_client import Gauge


health_requests_total = Counter(
    "health_requests_total",
    "Total number of health requests",
)


readiness_status = Gauge(
    "app_readiness_status",
    "Application readiness status",
)


cpu_usage_gauge = Gauge(
    "app_cpu_usage_percent",
    "CPU usage percent",
)


memory_usage_gauge = Gauge(
    "app_memory_usage_mb",
    "Memory usage in MB",
)
