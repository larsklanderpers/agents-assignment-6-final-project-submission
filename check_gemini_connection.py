"""One bounded structured-output request; never prints secrets or raw errors."""
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel


class ConnectionReply(BaseModel):
    status: str


def main():
    load_dotenv(Path(__file__).with_name(".env"))
    model = os.environ.get("REVIEW_LEDGER_MODEL", "gemini-3.8-flash")
    try:
        with genai.Client(http_options=types.HttpOptions(
            timeout=30000, retry_options=types.HttpRetryOptions(attempts=1)
        )) as client:
            response = client.models.generate_content(
                model=model,
                contents='Return a JSON object with status set to "connected".',
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ConnectionReply,
                    max_output_tokens=256,
                ),
            )
            reply = ConnectionReply.model_validate_json(response.text)
            if reply.status != "connected":
                raise ValueError("Unexpected response")
            print(json.dumps({"connected": True, "structured_output": True,
                              "requested_model": model,
                              "reported_model": response.model_version}))
    except Exception as error:
        print(json.dumps({"connected": False, "error_type": type(error).__name__,
                          "http_code": getattr(error, "code", None)}))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
