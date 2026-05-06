import os


class Config:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.api_base_url = os.getenv("API_BASE_URL")
        self.database_url = os.getenv("DATABASE_URL")