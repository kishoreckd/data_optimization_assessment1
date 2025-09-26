import os
import json
from app.core.config import settings

BLOB_DIR = settings.BLOB_DIR
os.makedirs(BLOB_DIR, exist_ok=True)  

def simulate_blob_upload(asset_id: str, content: dict) -> str:
    """This Function is used to simulate the blob storage by writing the content to a file with the asset_id"""
    filename = f"{asset_id}.blob"
    path = os.path.join(BLOB_DIR, filename)  
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)
    return path
