
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import re

app = FastAPI(title="BFHL API", version="1.0.0")

# Enable CORS for local development (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FULL_NAME_LOWER = "deepakkurra"
DOB_DDMMYYYY = "22022005"
EMAIL = "deepak@gmail.com"
ROLL_NUMBER = "22BCE20015"

DIGITS_ONLY = re.compile(r"^\d+$")
LETTERS_ONLY = re.compile(r"^[A-Za-z]+$")



class DataRequest(BaseModel):
    data: List[str]



def build_user_id() -> str:
    if not FULL_NAME_LOWER or not DOB_DDMMYYYY:
        raise HTTPException(status_code=500, detail="Server not configured: set FULL_NAME_LOWER and DOB_DDMMYYYY in main.py")
    return f"{FULL_NAME_LOWER}_{DOB_DDMMYYYY}"



def is_number_str(s: str) -> bool:
    return bool(DIGITS_ONLY.match(s))



def is_alpha_str(s: str) -> bool:
    return bool(LETTERS_ONLY.match(s))



def alternating_caps_reversed_from_letters(letter_chunks: List[str]) -> str:
    letters: List[str] = []
    for chunk in letter_chunks:
        letters.extend(list(chunk))
    letters.reverse()
    out_chars: List[str] = []
    for i, ch in enumerate(letters):
        base = ch.upper()
        if i % 2 == 0:
            out_chars.append(base)
        else:
            out_chars.append(base.lower())
    return "".join(out_chars)



@app.post("/bfhl")
async def bfhl(payload: DataRequest) -> Dict[str, Any]:
    try:
        items = payload.data
        even_numbers: List[str] = []
        odd_numbers: List[str] = []
        alphabets: List[str] = []
        special_characters: List[str] = []
        total_sum = 0
        alpha_chunks_for_concat: List[str] = []
        for item in items:
            if is_number_str(item):
                n = int(item)
                total_sum += n
                if n % 2 == 0:
                    even_numbers.append(item)
                else:
                    odd_numbers.append(item)
            elif is_alpha_str(item):
                upper_item = item.upper()
                alphabets.append(upper_item)
                alpha_chunks_for_concat.append(item)
            else:
                special_characters.append(item)
        concat_string = alternating_caps_reversed_from_letters(alpha_chunks_for_concat)
        response = {
            "is_success": True,
            "user_id": build_user_id(),
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_characters,
            "sum": str(total_sum),
            "concat_string": concat_string,
        }
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.get("/")
async def root():
    return {"status": "BFHL API running", "docs": "/docs"}