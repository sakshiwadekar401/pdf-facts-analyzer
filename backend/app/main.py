from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import json
from pathlib import Path

from .utils import extract_text_by_page, find_snippets_for_pointer

app = FastAPI(title="PDF Facts Analyzer")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to save PDFs
UPLOAD_DIR = Path(__file__).parent.parent / "sample_pdfs"
UPLOAD_DIR.mkdir(exist_ok=True)

# Models
class AnalyzeResponseItem(BaseModel):
    pointer: str
    results: List[Dict[str, Any]]

@app.post("/analyze", response_model=List[AnalyzeResponseItem])
async def analyze(file: UploadFile = File(...), pointers: str = Form(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Save file
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Parse pointers
    try:
        pointer_list = json.loads(pointers)
        if not isinstance(pointer_list, list):
            raise ValueError
    except Exception:
        raise HTTPException(status_code=400, detail="Pointers must be a JSON array.")

    # Extract text
    pages = extract_text_by_page(str(file_path))

    # Search for pointers
    results = []
    for pointer in pointer_list:
        hits = find_snippets_for_pointer(pointer, pages)
        results.append(AnalyzeResponseItem(pointer=pointer, results=hits))

    return results
