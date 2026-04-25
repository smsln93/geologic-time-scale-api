import os
from pathlib import Path


class Config:
    def __init__(self, require_api: bool = True):
        self.api_key = os.getenv("API_KEY")
        self.api_base_url = os.getenv("API_BASE_URL")
        self.database_url = os.getenv("DATABASE_URL")

        self._validate_required(require_api=require_api)

    def _validate_required(self, require_api: bool):

        if require_api:
            if not self.api_base_url:
                raise RuntimeError("API Base URL not set")

        if not self.database_url:
            raise RuntimeError("Database URL not set")
