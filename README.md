# FootToon Idea Generator

FootToon is a full-stack scaffold for turning live football trends into cartoon script ideas.

## Project Structure

- `/backend` - Node.js + Express API for trends, script generation, and database operations
- `/frontend` - React (Vite) app for browsing trends and managing script ideas

## Backend Features

- `GET /api/football-trends` - football players, matches, and transfer trend feed
- `GET /api/trending-content` - memes, themes, and song trend feed
- `POST /api/script-generator` - generate a cartoon script idea from selected trend inputs
- `GET /api/scripts` - list stored scripts
- `POST /api/scripts` - save a generated script to SQLite
- Middleware: request logging, 404 handling, centralized error handling

## Frontend Features

- Trends dashboard
- Script generator form
- Script idea preview and saved ideas browser
- API integration via environment-configurable backend URL

## Environment Setup

### Backend

1. Copy environment template:
   ```bash
   cp backend/.env.example backend/.env
   ```
2. Install dependencies:
   ```bash
   cd backend
   npm install
   ```
3. Run backend:
   ```bash
   npm run dev
   ```

### Frontend

1. Copy environment template:
   ```bash
   cp frontend/.env.example frontend/.env
   ```
2. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
3. Run frontend:
   ```bash
   npm run dev
   ```

Frontend defaults to `http://localhost:5173`, backend defaults to `http://localhost:4000`.

## Database

- SQLite database path is configured with `DB_PATH`.
- Schema file: `backend/src/db/schema.sql`
- Tables:
  - `trends`
  - `script_ideas`

The backend auto-initializes schema on startup.

## Validation Commands

- Backend tests: `cd backend && npm test`
- Frontend lint: `cd frontend && npm run lint`
- Frontend build: `cd frontend && npm run build`

## Next Steps

- Replace placeholder trend providers with real football/trend APIs.
- Add authentication and idea collaboration flows.
- Add richer script templates and AI model integration.
