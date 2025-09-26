import uuid
import math
import os
import json
import pickle

from app.service.blob_storage import simulate_blob_upload
from app.service.meta_data import nlp
from app.core.config import settings
from app.utils.logger import log_step

# Path to store Q-learning state (persistent)
QTABLE_FILE = os.path.join(settings.STORAGE_DIR, "qtable.pkl")

# ---- Q-learning agent ----
class QLearningAgent:
    """
    Simple Q-learning agent to refine predicted ratings 
    based on past feedback and rewards.
    """
    def __init__(self, qfile=QTABLE_FILE, alpha=0.5, gamma=0.9):
        self.qfile = qfile
        self.alpha = alpha  
        self.gamma = gamma  

        # Load Q-table from disk if available
        if os.path.exists(qfile):
            with open(qfile, "rb") as f:
                self.q = pickle.load(f)
        else:
            self.q = {}

        self.actions = [-1, 0, 1]

    def get_q(self, state, action):
        """Return Q-value for (state, action), default 0.0"""
        return self.q.get((state, action), 0.0)

    def best_action(self, state):
        """Choose best action (maximize Q-value)"""
        values = [(self.get_q(state, a), a) for a in self.actions]
        # Tie-break: prefer smaller adjustment
        best = max(values, key=lambda x: (x[0], -abs(x[1])))
        return best[1]

    def update(self, state, action, reward, next_state):
        """Update Q-value for state-action pair"""
        current = self.get_q(state, action)
        next_v = max(self.get_q(next_state, a) for a in self.actions)
        self.q[(state, action)] = current + self.alpha * (reward + self.gamma * next_v - current)

        # Persist Q-table
        with open(self.qfile, "wb") as f:
            pickle.dump(self.q, f)


# Initialize a single shared Q-agent
qagent = QLearningAgent()


# ---- Utility functions ----
def sanitize_record(rec: dict):
    """Replace any NaN or Inf with None for JSON safety"""
    for k, v in rec.items():
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            rec[k] = None
    return rec


def mask_persons(text: str):
    """Mask PERSON entities using spaCy NER (fallback: replace names manually)"""
    try:
        doc = nlp(text)
        spans = [(ent.start_char, ent.end_char) for ent in doc.ents if ent.label_ == "PERSON"]
        if not spans:
            return text

        # Replace PERSON spans with [MASKED]
        masked = []
        last = 0
        for s, e in spans:
            masked.append(text[last:s])
            masked.append("[MASKED]")
            last = e
        masked.append(text[last:])
        return "".join(masked)
    except Exception:
        # Simple fallback replacement if spaCy fails
        return text.replace("John", "[MASKED]").replace("Sarah", "[MASKED]")


# ---- Refinement pipeline ----
def refine_records(records: list, sentiment_pipe, logfile=None):
    """
    Refine records:
    - Predict sentiment score → convert to rating
    - Apply Q-learning to adjust rating
    - Mask sensitive entities
    - Store results in simulated blob storage
    """
    os.makedirs(settings.BLOB_DIR, exist_ok=True)
    final_records = []

    for rec in records:
        text = rec.get("text", "")

        # --- Step 1: Sentiment prediction (transformers pipeline) ---
        try:
            result = sentiment_pipe(text[:512])[0]  # limit input length
            label = result.get("label", "")
            score = float(result.get("score", 0.0))

            # Convert sentiment → rating (0–10 scale)
            predicted_rating = score * 10 if label.upper() == "POSITIVE" else (1.0 - score) * 10
            predicted_rating = round(predicted_rating, 2)
        except Exception:
            # Fallback to imputed rating
            predicted_rating = rec.get("rating_imputed") or 7.0

        # --- Step 2: Q-learning refinement ---
        state = int(round(predicted_rating))
        action = qagent.best_action(state)

        imputed = rec.get("rating_imputed") or 7.0
        refined = max(0, min(10, max(imputed, predicted_rating + action)))  

        # Reward = closer refined rating to actual rating
        actual = rec.get("rating")
        if actual is not None and not (isinstance(actual, float) and math.isnan(actual)):
            reward = max(0.0, 1.0 - abs(refined - actual) / 10.0)
        else:
            reward = 0.5  # neutral reward if no actual rating available
        next_state = int(round(refined))
        qagent.update(state, action, reward, next_state)

        # --- Step 3: Build output record ---
        rec_out = {
            "asset_id": f"asset_{str(uuid.uuid4())[:8]}",
            "original_text_masked": mask_persons(text),
            "refined_rating": refined,
            "rating_imputed": imputed,
            "original_rating": rec.get("rating"),
            "timestamp": rec.get("timestamp")
        }

        rec_out = sanitize_record(rec_out)

        # --- Step 4: Simulate blob storage ---
        blob_path = simulate_blob_upload(rec_out["asset_id"], rec_out)
        # rec_out["blob_path"] = blob_path  

        final_records.append(rec_out)

        
        if logfile:
            log_step(logfile, f"Uploaded blob for {rec_out['asset_id']} to {blob_path}")

    # Save final results to JSON file
    with open(settings.FINAL_FILE, "w", encoding="utf-8") as f:
        json.dump([sanitize_record(r) for r in final_records], f, indent=2)

    return final_records
