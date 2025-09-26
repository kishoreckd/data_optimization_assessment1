from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Settings(BaseSettings):
    """Settings model to read configuration from environment variables"""

    AUTH_TOKEN: str="E6DEhEuDGacV3p97TmKjJxLGmMKM9Zw6w9vyuvxR"
    RATE_LIMIT_PER_MINUTE: int = 10

    # Storage
    STORAGE_DIR: str = "./storage"
    BLOB_DIR: str = "./blob_storage"
    SPACY_MODEL: str = "en_core_web_sm"

    #storage files
    @property
    def CLEANED_FILE(self) -> Path:
        return Path(self.STORAGE_DIR) / "cleaned.json"
    @property
    def FINAL_FILE(self) -> Path:
        return Path(self.STORAGE_DIR) / "final_records.json"
    @property
    def METADATA_FILE(self) -> Path:
        return Path(self.STORAGE_DIR) / "metadata.json"

    @property
    def QTABLE_FILE(self) -> Path:
        return Path(self.STORAGE_DIR) / "qtable.pkl"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Initiate settings
settings = Settings()
