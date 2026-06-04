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
3. Configure your runtime values directly in `.env`.
   - Keep `GEMINI_MODEL=gemini-flash-lite-latest` as the free-tier-friendly default.
   - Set `DATABASE_URL`, `INPUT_COST_PER_MILLION_TOKENS`, and `OUTPUT_COST_PER_MILLION_TOKENS` there.
4. Set `GEMINI_API_KEY` in `.env`.
5. Run the initial migration:
   ```bash
   alembic upgrade head
   ```
6. Run the app:
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
  "id": 1,
  "prompt": "Explain Docker",
  "response": "AI generated response",
  "input_tokens": 3,
  "output_tokens": 12,
  "total_tokens": 15,
  "estimated_cost": "0.000000",
  "created_at": "2026-06-04T00:00:00Z"
}
```
