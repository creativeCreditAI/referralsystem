# Referral System

A full-stack referral platform with FastAPI backend and React frontend. Users can generate unique referral links, share them, and earn rewards for successful referrals.

## Project Structure

```
referralsystem/
├── frontend/              # React + Vite SPA
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js        # Backend API client
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── package.json
│   ├── vite.config.js
│   └── .env              # Frontend config
│
├── models/               # Data models & schemas
│   ├── models.py         # SQLAlchemy ORM
│   ├── schemas.py        # Pydantic validators
│   └── database.py       # SQLAlchemy setup
│
├── routes/               # API routes
│   └── router.py         # FastAPI router
│
├── services/             # Business logic
│   └── referral.py       # Referral generation & tracking
│
├── main.py               # FastAPI app entry
├── requirements.txt      # Python dependencies
└── README.md
```

## Setup

### Backend

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```
   Server runs at `http://localhost:8000`

3. **API documentation:**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Frontend

1. **Install Node dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Create `.env` file** (if not present):
   ```bash
   cp .env.example .env
   ```

3. **Run dev server:**
   ```bash
   npm run dev
   ```
   Frontend runs at `http://localhost:5173`

## Features

### Routes

**Home / Referral Generator** (`/`)
- Create unique referral links
- Display referral token and shareable URL
- Copy-to-clipboard functionality
- Dummy stats dashboard

**Signup with Referral** (`/signup?ref=TOKEN`)
- Accept referral token from query param
- Sign up new user
- Track referral and award points
- Auto-populate referral context

### API Endpoints

- `POST /api/referral/` - Create referral link
- `POST /api/signup/?ref=TOKEN` - Sign up with referral
- `GET /api/r/{token}` - Redirect referral link (old style, can be deprecated)

### Database

SQLite database with three tables:
- **users** - User accounts with referral tokens/links
- **referrals** - Referral tracking (count of successful signups)
- **reward_system** - Points awarded to referrers

## Data Flow

1. **User A generates referral:**
   - Frontend: POST `/api/referral/` with name/email/position
   - Backend: Create user, generate unique token, create referral record
   - Response: `{ user_id, referral_token, referral_link }`
   - Frontend: Display link for sharing

2. **User B clicks referral link:**
   - Frontend: Visit `/signup?ref=<token>`
   - App detects signup mode, prefills token

3. **User B completes signup:**
   - Frontend: POST `/api/signup/?ref=<token>`
   - Backend: Create user B, track referral under User A, award points
   - Response: User B's referral info

## Environment Variables

**Frontend (`.env`):**
```
VITE_API_BASE_URL=http://localhost:8000/api
```

**Backend (via `.env` or `os.getenv()`):**
```
FRONTEND_URL=http://localhost:5173
BASE_REF_URL=http://localhost:8000/api/r
```

## Development

### Frontend Debug
API calls are logged to console. Check browser dev tools for request/response details.

### Backend Debug
Enable debug logging in FastAPI with:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Production Deployment

1. **Backend:** Use `gunicorn` or similar ASGI server
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   ```

2. **Frontend:** Build and serve static files
   ```bash
   npm run build
   ```

3. **Database:** Switch from SQLite to PostgreSQL for production
   ```python
   DATABASE_URL = "postgresql://user:password@localhost/referraldb"
   ```

## Notes

- Referral tokens are generated using `secrets.token_urlsafe(12)` for uniqueness
- CORS is enabled for `localhost:5173` and `localhost:3000`
- Database auto-creates on server startup
- All timestamps are UTC with timezone awareness
