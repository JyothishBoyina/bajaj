# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import re

# Initialize FastAPI app
app = FastAPI(title="BFHL API", version="1.0.0")

# Enable CORS (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- User Info ---
FULL_NAME_LOWER = "deepakkurra"
DOB_DDMMYYYY = "22022005"
EMAIL = "deepak@gmail.com"
ROLL_NUMBER = "22BCE20015"

# --- Regex ---
DIGITS_ONLY = re.compile(r"^\d+$")
LETTERS_ONLY = re.compile(r"^[A-Za-z]+$")


# --- Request Model ---
class DataRequest(BaseModel):
    data: List[str]


# --- Helper Functions ---
def build_user_id() -> str:
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
        if i % 2 == 0:
            out_chars.append(ch.upper())
        else:
            out_chars.append(ch.lower())
    return "".join(out_chars)


# --- Routes ---
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
                alphabets.append(item.upper())
                alpha_chunks_for_concat.append(item)
            else:
                special_characters.append(item)

        concat_string = alternating_caps_reversed_from_letters(alpha_chunks_for_concat)

        return {
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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
async def root():
    return {"status": "BFHL API running", "docs": "/docs"}
