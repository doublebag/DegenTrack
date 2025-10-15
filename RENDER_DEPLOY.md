# Deploying DegenTracks to Render (Free Tier)

1. Create a GitHub repo and push the project root to it.

2. Sign up / log in to Render (https://render.com).

3. Create a new **Web Service**:
   - Connect GitHub and choose your repo.
   - Root directory: backend
   - Start command: uvicorn main:app --host 0.0.0.0 --port $PORT
   - Build command (optional): pip install -r requirements.txt

4. Add environment variables (Dashboard -> Environment):
   - JWT_SECRET (set a secure value)
   - ACCESS_TOKEN_EXPIRE_MINUTES (optional)

5. Deploy and visit the URL Render provides.

Notes:
- For persistent data use Render Postgres and set DATABASE_URL accordingly.
- Replace placeholder bootstrap CSS with CDN link in templates for better styling.
