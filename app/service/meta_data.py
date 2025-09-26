import spacy   
import json
from app.core.config import settings

try:
    nlp = spacy.load(settings.SPACY_MODEL)
except OSError:
    raise RuntimeError(f"Please install spaCy model: python -m spacy download {settings.SPACY_MODEL}")

def write_json(path: str, data):
    """This Function is used to write the metadata to a file"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def extract_metadata(records: list):
    """Extract named entities from text using spaCy"""
    metadata = []
    for idx, rec in enumerate(records):
        doc = nlp(rec["text"])
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        metadata.append({
            "index": idx,
            "entities": entities,
            "original_text": rec["text"]
        })
    write_json(settings.METADATA_FILE, metadata)
    return metadata, settings.METADATA_FILE
