import os
import sqlite3
from datetime import datetime, timezone
from html import escape
from typing import Any
from urllib.parse import parse_qs

import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel

DB_PATH = os.getenv("FOOTOON_DB", "footoon.db")
MAX_TITLE_LENGTH = 60


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                football_context TEXT NOT NULL,
                social_context TEXT NOT NULL,
                song_context TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


init_db()


class IdeaRequest(BaseModel):
    prompt: str | None = None


class RemixRequest(BaseModel):
    prompt: str | None = None


def _safe_get(url: str, **kwargs: Any) -> dict[str, Any] | None:
    try:
        response = requests.get(url, timeout=10, **kwargs)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def fetch_football_context() -> list[str]:
    token = os.getenv("FOOTBALL_DATA_API_KEY")
    if not token:
        return ["Add FOOTBALL_DATA_API_KEY for live match + transfer context."]

    data = _safe_get(
        "https://api.football-data.org/v4/matches?status=LIVE",
        headers={"X-Auth-Token": token},
    )
    if not data:
        return ["Football API currently unavailable."]

    matches = data.get("matches", [])[:5]
    if not matches:
        return ["No live matches right now."]

    context: list[str] = []
    for match in matches:
        home = match.get("homeTeam", {}).get("name", "Home")
        away = match.get("awayTeam", {}).get("name", "Away")
        score = match.get("score", {}).get("fullTime", {})
        context.append(f"{home} vs {away} ({score.get('home', 0)}-{score.get('away', 0)})")
    return context


def fetch_social_trends() -> dict[str, list[str]]:
    trends: dict[str, list[str]] = {}

    reddit = _safe_get(
        "https://www.reddit.com/r/soccer/hot.json?limit=5",
        headers={"User-Agent": "footoon-idea-generator/1.0"},
    )
    if reddit:
        reddit_posts = [
            child.get("data", {}).get("title", "")
            for child in reddit.get("data", {}).get("children", [])
        ]
        trends["reddit"] = [title for title in reddit_posts if title]

    twitter_bearer = os.getenv("TWITTER_BEARER_TOKEN")
    if twitter_bearer:
        twitter_auth_header = "{} {}".format("Bearer", twitter_bearer)
        twitter = _safe_get(
            "https://api.twitter.com/2/tweets/search/recent?query=(football%20OR%20soccer)%20-is:retweet&max_results=10",
            headers={"Authorization": twitter_auth_header},
        )
        if twitter:
            trends["twitter"] = [tweet.get("text", "") for tweet in twitter.get("data", []) if tweet.get("text")]

    tiktok_url = os.getenv("TIKTOK_TRENDS_URL")
    if tiktok_url:
        tiktok = _safe_get(
            tiktok_url,
            headers={"X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY", "")},
        )
        if tiktok:
            items = tiktok.get("data", [])
            trends["tiktok"] = [item.get("title", "") for item in items if item.get("title")]

    if not trends:
        return {"general": ["Add API credentials to pull Twitter/X, Reddit, and TikTok trends."]}

    return trends


def fetch_song_trends() -> list[str]:
    spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if spotify_client_id and spotify_client_secret:
        try:
            token_response = requests.post(
                "https://accounts.spotify.com/api/token",
                data={"grant_type": "client_credentials"},
                auth=(spotify_client_id, spotify_client_secret),
                timeout=10,
            )
            token_response.raise_for_status()
            access_token = token_response.json()["access_token"]
            spotify_auth_header = "{} {}".format("Bearer", access_token)
            releases = requests.get(
                "https://api.spotify.com/v1/browse/new-releases?limit=5",
                headers={"Authorization": spotify_auth_header},
                timeout=10,
            )
            releases.raise_for_status()
            return [
                album.get("name", "")
                for album in releases.json().get("albums", {}).get("items", [])
                if album.get("name")
            ]
        except Exception:
            pass

    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    if youtube_api_key:
        youtube = _safe_get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={
                "part": "snippet",
                "chart": "mostPopular",
                "videoCategoryId": 10,
                "maxResults": 5,
                "key": youtube_api_key,
            },
        )
        if youtube:
            return [
                item.get("snippet", {}).get("title", "")
                for item in youtube.get("items", [])
                if item.get("snippet", {}).get("title")
            ]

    return ["Add Spotify or YouTube credentials for live music trends."]


def generate_script_idea(
    football_context: list[str],
    social_context: dict[str, list[str]],
    song_context: list[str],
    user_prompt: str | None = None,
) -> tuple[str, str]:
    top_football = football_context[0] if football_context else "No football context"

    social_platform = next(iter(social_context), "general")
    social_item = social_context.get(social_platform, ["No social context"])[0]
    top_song = song_context[0] if song_context else "No song context"

    prompt_line = f"Creator twist: {user_prompt}." if user_prompt else ""
    title = f"FootToon: {top_football[:MAX_TITLE_LENGTH]}"
    body = (
        f"Cold open: The squad enters a cartoon stadium inspired by '{top_football}'.\n"
        f"Meme beat: They react to {social_platform} trend '{social_item}'.\n"
        f"Music cue: Transition with '{top_song}'.\n"
        "Punchline: A transfer rumor appears as a talking mascot and causes chaos.\n"
        f"{prompt_line}".strip()
    )
    return title, body


def persist_script(
    title: str,
    body: str,
    football_context: list[str],
    social_context: dict[str, list[str]],
    song_context: list[str],
) -> int:
    with get_conn() as conn:
        cursor = conn.execute(
            """
            INSERT INTO scripts (title, body, football_context, social_context, song_context, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                body,
                " | ".join(football_context),
                " | ".join([f"{k}:{', '.join(v)}" for k, v in social_context.items()]),
                " | ".join(song_context),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def build_idea(prompt: str | None = None) -> dict[str, Any]:
    football_context = fetch_football_context()
    social_context = fetch_social_trends()
    song_context = fetch_song_trends()
    title, body = generate_script_idea(football_context, social_context, song_context, prompt)
    script_id = persist_script(title, body, football_context, social_context, song_context)
    return {"id": script_id, "title": title, "body": body}


def list_scripts() -> list[dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute("SELECT id, title, body, created_at FROM scripts ORDER BY id DESC").fetchall()
        return [dict(row) for row in rows]


app = FastAPI(title="FootToon Idea Generator")


@app.get("/api/trends")
def get_trends() -> dict[str, Any]:
    return {
        "football": fetch_football_context(),
        "social": fetch_social_trends(),
        "songs": fetch_song_trends(),
    }


@app.get("/api/ideas")
def get_ideas() -> list[dict[str, Any]]:
    return list_scripts()


def _extract_prompt(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped or None


@app.post("/api/ideas")
async def create_idea(request: Request) -> dict[str, Any]:
    prompt: str | None = None
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        payload = await request.json()
        if isinstance(payload, dict):
            prompt = _extract_prompt(payload.get("prompt"))
    elif "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        form = await request.form()
        prompt = _extract_prompt(form.get("prompt"))
    else:
        body = (await request.body()).decode(errors="ignore")
        prompt = _extract_prompt(parse_qs(body).get("prompt", [None])[0])

    return build_idea(prompt)


@app.post("/api/ideas/{idea_id}/remix")
def remix_idea(idea_id: int, request: RemixRequest | None = None) -> dict[str, Any]:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM scripts WHERE id = ?", (idea_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Idea not found")

    football_context = [item.strip() for item in row["football_context"].split("|") if item.strip()]
    social_context: dict[str, list[str]] = {}
    for section in row["social_context"].split("|"):
        section = section.strip()
        if not section:
            continue
        platform, separator, values = section.partition(":")
        items = [item.strip() for item in values.split(",") if item.strip()] if separator else [section]
        social_context[platform.strip() if platform else "general"] = items
    if not social_context:
        social_context = {"general": ["No social context"]}
    song_context = [item.strip() for item in row["song_context"].split("|") if item.strip()]

    prompt = request.prompt if request else None
    title, body = generate_script_idea(football_context, social_context, song_context, prompt)
    new_id = persist_script(title, body, football_context, social_context, song_context)
    return {"id": new_id, "title": title, "body": body}


@app.get("/api/ideas/{idea_id}/download")
def download_idea(idea_id: int) -> PlainTextResponse:
    with get_conn() as conn:
        row = conn.execute("SELECT title, body FROM scripts WHERE id = ?", (idea_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Idea not found")

    filename = f"footoon-idea-{idea_id}.txt"
    content = f"{row['title']}\n\n{row['body']}"
    response = PlainTextResponse(content)
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    items = list_scripts()
    list_markup = "".join(
        [
            "<li><strong>{}</strong> - <a href='/api/ideas/{}/download'>Download</a></li>".format(
                escape(str(item["title"])),
                int(item["id"]),
            )
            for item in items
        ]
    )
    return f"""
    <html>
      <head><title>FootToon Idea Generator</title></head>
      <body>
        <h1>FootToon Idea Generator</h1>
        <p>Generate script ideas using football trends + social memes + songs.</p>
        <form method='post' action='/api/ideas'>
          <label>Optional prompt:</label>
          <input name='prompt' />
          <button type='submit'>Generate</button>
        </form>
        <h2>Saved ideas</h2>
        <ul>{list_markup or '<li>No ideas yet</li>'}</ul>
      </body>
    </html>
    """
