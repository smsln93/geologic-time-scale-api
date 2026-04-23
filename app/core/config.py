from pathlib import Path

from dotenv import dotenv_values

from .paths import ENV_FILE

class Config:
    """
    Application configuration loader based on a .env file.

    Loads required environment variables and exposes them
    as class attributes.

    Attributes:
        env_config_path (Path): Path to the .env file.
        api_key (str | None): API authentication key.
        api_base_url (str): Base URL for the API.
        database_url (str): Database connection string.

    Raises:
        RuntimeError: If the .env file is missing or required
        variables are not defined.
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
        if value is None or value == "":
            raise RuntimeError(f"Missing env variable: {key}")
        return value

app_configuration = Config(ENV_FILE)
