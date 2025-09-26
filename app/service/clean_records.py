import pandas as pd
import numpy as np
import datetime
import math
import os
import json
from app.core.config import settings

def write_json(path: str, data):
    """Safe JSON dump with NaN -> null and checking nan and inf"""

    def default(obj):
        if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
            return None
        return obj
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=default)


def clean_records(records: list):
    """Getting the records and cleaning them by filling the timestamp and rating_imputed"""
    df = pd.DataFrame(records)

    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"
    df["timestamp"] = df.get("timestamp", None).fillna(now_iso)

    median_rating = float(df["rating"].dropna().median()) if not df["rating"].dropna().empty else 7.0
    df["rating_imputed"] = df["rating"].fillna(median_rating)

    # converting the text to string
    df["text"] = df["text"].astype(str)

    # replacing the inf and -inf with nan
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.astype(object).mask(pd.isna(df), None)

    # converting the dataframe to dictionary
    cleaned = df.to_dict(orient="records")
    write_json(settings.CLEANED_FILE, cleaned)
    return cleaned, settings.CLEANED_FILE
