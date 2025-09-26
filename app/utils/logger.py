import os
import datetime
from app.core.config import settings

LOG_DIR = os.path.join(settings.STORAGE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def get_log_file():
    """Generate a unique log file per request and ensure directory exists"""
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return os.path.join(LOG_DIR, f"log_{timestamp}.log")

def log_step(logfile: str, message: str):
    """Append a timestamped message to the log file"""
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(f"{ts} {message}\n")
