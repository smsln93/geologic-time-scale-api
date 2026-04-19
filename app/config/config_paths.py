from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
APP_DIR = PROJECT_ROOT.joinpath("app")
EXPORT_DIR = PROJECT_ROOT.joinpath("exports")
APP_CONFIG_DIR = APP_DIR.joinpath("config")
ENV_FILE = PROJECT_ROOT.joinpath(".env")