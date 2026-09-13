from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import os
from typing import Literal


app = FastAPI()


class LLMAnalysis(BaseModel):
    interpretation: str
    mathematical_claim: Literal["TRUE", "FALSE", "UNKNOWN"]
    lean_statement: str | None = None
    proof: str | None = None
    counterexample: str | None = None
    reasoning_summary: str


@app.get("/")
def home():
    return {"message": "SolidProof is running"}


@app.post("/verify")
def verify(lean_code: str):

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".lean",
        delete=False
    ) as f:
        f.write(lean_code)
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


@app.post("/verify-analysis")
def verify_analysis(analysis: LLMAnalysis):

    if analysis.mathematical_claim != "TRUE":
        return {
            "status": "UNKNOWN",
            "message": "La vérification automatique d'une preuve est utilisée uniquement pour une proposition marquée TRUE."
        }

    if analysis.lean_statement is None:
        return {
            "status": "FORMALIZATION_FAILED"
        }

    if analysis.proof is None:
        return {
            "status": "FORMALIZATION_FAILED"
        }

    lean_code = f"""
import Mathlib

example : {analysis.lean_statement} := {analysis.proof}
"""

    return verify(lean_code)