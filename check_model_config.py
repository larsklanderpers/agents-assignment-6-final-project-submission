"""Check local configuration without displaying credentials or calling a service."""
import json
import os
from pathlib import Path

from dotenv import dotenv_values


def configuration_status() -> dict[str, bool]:
    values = dotenv_values(Path(__file__).with_name(".env"))
    key = os.environ.get("GOOGLE_API_KEY") or values.get("GOOGLE_API_KEY")
    model = os.environ.get("REVIEW_LEDGER_MODEL") or values.get("REVIEW_LEDGER_MODEL")
    return {"gemini_key_configured": bool(key and key.strip()),
            "model_configured": bool(model and model.strip())}


if __name__ == "__main__":
    print(json.dumps(configuration_status()))
