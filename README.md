# BFHL API (FastAPI)

## Setup
1. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
```

2. Configure your personal details in `main.py`:
- `FULL_NAME_LOWER` (e.g., `john_doe`)
- `DOB_DDMMYYYY` (e.g., `17091999`)
- `EMAIL` (e.g., `john@xyz.com`)
- `ROLL_NUMBER` (e.g., `ABCD123`)

3. Run locally:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. Test:
```bash
curl -X POST http://127.0.0.1:8000/bfhl \
  -H "Content-Type: application/json" \
  -d '{"data": ["a","1","334","4","R","$"]}'
```

## Notes
- Numbers must be treated as strings in input and output.
- Alphabets are returned uppercase; special characters are everything else.
- `concat_string` is all letters from input flattened, reversed, and alternating caps (Upper, lower, ...).
- Docs: visit `/docs` when the server is running.