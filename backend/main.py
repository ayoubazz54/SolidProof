from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import os

app = FastAPI()


class ProofRequest(BaseModel):
    code: str


@app.get("/")
def home():
    return {"message": "SolidProof is running"}


@app.post("/verify")
def verify(request: ProofRequest):

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".lean",
        delete=False
    ) as f:
        f.write(request.code)
        file_path = f.name

    try:
        result = subprocess.run(
            [
                "lake",
                "env",
                "lean",
                file_path
            ],
            cwd="../MathProof",
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            return {
                "status": "VERIFIED"
            }

        return {
            "status": "FAILED",
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    finally:
        os.remove(file_path)