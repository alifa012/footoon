# footoon

FootToon Idea Generator MVP for creating cartoon script ideas from:
- football context (Football-Data.org)
- social trends (Reddit + optional Twitter/X + optional TikTok source)
- music trends (Spotify or YouTube)

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000` for the web UI.

## API endpoints

- `GET /api/trends` – aggregated trend sources
- `POST /api/ideas` – generate and save an idea (`{"prompt": "optional"}`)
- `GET /api/ideas` – list saved ideas
- `POST /api/ideas/{id}/remix` – remix an existing idea
- `GET /api/ideas/{id}/download` – download idea as text

## Environment variables

- `FOOTBALL_DATA_API_KEY`
- `TWITTER_BEARER_TOKEN`
- `TIKTOK_TRENDS_URL` (+ optional `RAPIDAPI_KEY`)
- `SPOTIFY_CLIENT_ID` + `SPOTIFY_CLIENT_SECRET`
- `YOUTUBE_API_KEY`
- `FOOTOON_DB` (defaults to `footoon.db`)
