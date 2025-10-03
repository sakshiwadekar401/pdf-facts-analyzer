# PDF Facts Analyzer
## Project Overview
**PDF Facts Analyzer** is a small full-stack application that extracts requested facts from PDF documents. Users can upload a PDF and provide textual pointers (instructions) like “List all dates”, “Who signed?”, or “Total contract value?”. The app returns relevant text snippets, page numbers, character offsets, and a short rationale for each pointer.

---

## Features

### Backend (FastAPI)
- Accepts PDF uploads (single file).  
- Accepts a JSON array of textual pointers.  
- Extracts text from PDFs (text-based).  
- Returns for each pointer:
  - Text snippet(s)  
  - Page number  
  - Character offset (start/end)  
  - Short rationale/explanation  

### Frontend (Next.js)
- Form to upload PDF and enter multiple pointers.  
- Submit button calls backend API.  
- Displays results per pointer:
  - Snippets with page number  
  - Optionally expandable to show context  

### Data Storage
- Stores uploaded PDFs locally (or in-memory for simplicity).  
- Sample PDFs included for testing.  

---
