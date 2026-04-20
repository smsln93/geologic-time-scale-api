from pathlib import Path

from dotenv import dotenv_values

from .config_paths import ENV_FILE

class Config:
    """
    Loads API_KEY, API_BASE_URL and DATABASE_URL values from the .env file.

    Attributes:
        env_config_path (Path): Path to the .env file.
    """
    def __init__(self, env_config_path: Path) -> None:
        self.env_config_path = env_config_path

        self._load_env()
        self._assign_parameters()

    def _load_env(self) -> None:
        self.env_variables = dotenv_values(self.env_config_path)
        if not self.env_variables:
            raise RuntimeError(".env file not found or empty")

    def _assign_parameters(self) -> None:
        self.api_key = self.env_variables.get("API_KEY")
        self.api_base_url = self._required("API_BASE_URL")
        self.database_url = self._required("DATABASE_URL")

    def _required(self, key: str) -> str:
        value = self.env_variables.get(key)
        if not value:
            raise RuntimeError(f"Missing env variable: {key}")
        return value

app_configuration = Config(ENV_FILE)
