import re
from typing import List, Dict, Any
import pdfplumber  # pip install pdfplumber

def extract_text_by_page(pdf_path: str) -> List[str]:
    """
    Extract text from each page of a PDF.
    Returns a list of page texts.
    """
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return pages

def find_snippets_for_pointer(pointer: str, pages: List[str], window: int = 50) -> List[Dict[str, Any]]:
    hits: List[Dict[str, Any]] = []
    pointer_low = pointer.lower()

    # 1️⃣ Currency-like search
    if any(word in pointer_low for word in ['total', 'amount', 'value', 'price', 'invoice', 'consideration']):
        money_regex2 = r"\b(?:Rs\.?\s?|INR\s?|USD\s?|£|€)?\s?[0-9\,]+(?:\.\d+)?\b"
        for i, text in enumerate(pages):
            for m in re.finditer(money_regex2, text):
                start, end = m.span()
                snippet = text[max(0, start-window):min(len(text), end+window)]
                hits.append({
                    'page': i + 1,
                    'start_char': start,
                    'end_char': end,
                    'snippet': snippet.strip(),
                    'rationale': 'Found currency-like number'
                })
        if hits:
            return hits

    # 2️⃣ Exact substring search
    for i, text in enumerate(pages):
        idx = text.lower().find(pointer_low)
        if idx != -1:
            start = idx
            end = idx + len(pointer_low)
            snippet = text[max(0, start-window):min(len(text), end+window)]
            hits.append({
                'page': i + 1,
                'start_char': start,
                'end_char': end,
                'snippet': snippet.strip(),
                'rationale': 'Exact substring match (case-insensitive)'
            })

    # 3️⃣ Fuzzy word overlap
    if not hits:
        words = [w for w in re.findall(r"\w+", pointer_low) if len(w) > 2]
        if words:
            scores = []
            for i, text in enumerate(pages):
                text_low = text.lower()
                count = sum(1 for w in words if w in text_low)
                scores.append((count, i))
            scores.sort(reverse=True)
            for count, i in scores[:2]:
                if count == 0:
                    continue
                text = pages[i]
                for w in words:
                    j = text.lower().find(w)
                    if j != -1:
                        start = max(0, j - window)
                        end = min(len(text), j + len(w) + window)
                        hits.append({
                            'page': i + 1,
                            'start_char': start,
                            'end_char': end,
                            'snippet': text[start:end].strip(),
                            'rationale': f"Fuzzy match using keyword '{w}' (page score {count})"
                        })
                        break
    return hits
