# AI Token Optimization & Cost Management Platform

Phase 3 extends the FastAPI-based AI Gateway with Redis caching so repeated prompts can be served without another Gemini call.

## Features

- POST `/ask` endpoint
- Pydantic request validation
- Dedicated Gemini service layer
- Redis-backed prompt cache with TTL
- Environment-based configuration
- Structured error handling
- Cache-aware analytics

## Project Structure

- `app/main.py`: FastAPI application entry point.
- `app/routes/`: API route modules.
- `app/services/`: External service integrations.
- `app/schemas/`: Pydantic request and response models.
- `app/config/`: Application settings and environment loading.
- `alembic/versions/`: Database migration history.

## Setup

1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your runtime values directly in `.env`.
   - Keep `GEMINI_MODEL=gemini-flash-lite-latest` as the free-tier-friendly default.
   - Set `DATABASE_URL`, `INPUT_COST_PER_MILLION_TOKENS`, and `OUTPUT_COST_PER_MILLION_TOKENS` there.
   - Set `REDIS_URL` and `CACHE_TTL_SECONDS` for cache behavior.
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
   "cached": false,
  "created_at": "2026-06-04T00:00:00Z"
}
```

## Cache Behavior

- Cache hits return immediately from Redis and skip Gemini.
- Cache misses fall back to Gemini and store the response back in Redis.
- Redis failures are treated as cache misses so the API remains available.
- `/analytics` now reports cache hits, cache misses, hit rate, and estimated requests saved.
