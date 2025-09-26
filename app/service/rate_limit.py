import time
import threading
from app.core.config import settings

rate_lock = threading.Lock()
request_counters = {}

def check_rate_limit(api_key: str):
    """This Function is used to check the rate limit for the api key"""
    now = time.time()
    with rate_lock:
        entry = request_counters.get(api_key)
        if entry is None or now - entry["window_start"] >= 60:
            request_counters[api_key] = {"window_start": now, "count": 1}
            return True
        else:
            if entry["count"] >= settings.RATE_LIMIT_PER_MINUTE:
                return False
            entry["count"] += 1
            return True
