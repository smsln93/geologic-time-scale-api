import argparse
import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv


def run():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Run Geologic Time Scale API")
    parser.add_argument("--db-path", type=Path, required=False, help="Optional path to SQLite database")

    args = parser.parse_args()

    if args.db_path is not None:
        db_path = args.db_path.resolve()

        if not db_path.is_file():
            parser.error(f"Database not found: {db_path}")

        os.environ["DATABASE_URL"] = f"sqlite:///{db_path.as_posix()}"

    uvicorn.run(
        app="app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    run()
