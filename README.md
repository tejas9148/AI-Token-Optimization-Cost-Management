# AI Token Optimization & Cost Management Platform

Phase 1 of the project provides a FastAPI-based AI Gateway that accepts a prompt, sends it to Gemini, and returns the generated response.

## Features

- POST `/ask` endpoint
- Pydantic request validation
- Dedicated Gemini service layer
- Environment-based configuration
- Structured error handling

## Project Structure

- `app/main.py`: FastAPI application entry point.
- `app/routes/`: API route modules.
- `app/services/`: External service integrations.
- `app/schemas/`: Pydantic request and response models.
- `app/config/`: Application settings and environment loading.

## Setup

1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set `GEMINI_API_KEY` in `.env` and keep `GEMINI_MODEL=gemini-flash-lite-latest` as the free-tier-friendly default.
4. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```

## Example Request

```json
{
  "prompt": "Explain Docker"
}
```

## Example Response

```json
{
  "success": true,
  "prompt": "Explain Docker",
  "response": "AI generated response"
}
```
