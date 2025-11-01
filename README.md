
# 🚀 QUICKSTART (1‑shot boot)

```bash
# clone + enter
git clone https://github.com/<you>/NICEDAYTODAY.git
cd NICEDAYTODAY

# backend deps + boot (port 8000)
python3 -m venv venv && source venv/bin/activate
pip install -r backend/requirements.txt
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 &
cd ..

# frontend (serve ./frontend on port 3000)
npx serve frontend -p 3000

# open:
echo "👉 Frontend: http://localhost:3000"
echo "👉 Backend:  http://localhost:8000"
```

---

# CrateJuice — One‑Shot (CJ_19)

**Goal:** paste URL → rip MP3 → play/download.  
Deploy fast on Render (backend) + Netlify (frontend).

## Structure
```
backend/     # FastAPI: /rip /batch /recent /dl/{file}
frontend/    # Minimal UI + player + 'Rip Everything' buttons
playlists/   # vol1.txt ... vol10.txt (one URL per line)
apt.txt      # ffmpeg for Render
render.yaml  # Render config
.netlify.toml# CORS helpers
.gitignore
README.md
```

## Deploy (Render backend)
- Build: `pip install -r backend/requirements.txt`
- Start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- Ensure repo root has `apt.txt` with `ffmpeg`

## Deploy (Netlify frontend)
- New site → drag `frontend/` directory
- Open: `https://<yoursite>.netlify.app/?api=https://<your-render>.onrender.com`

## Use
- Paste one URL → **Rip One**
- Paste many in textarea → **Rip EVERYTHING**
- See **Recent**; click any item to download or play inline

© CJ 2025 — PLUR
