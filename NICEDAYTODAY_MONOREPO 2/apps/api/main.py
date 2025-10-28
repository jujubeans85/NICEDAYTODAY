from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CrateJuice API")

app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

@app.get("/")
def root(): return {"ok": True, "msg": "CrateJuice API live"}

@app.get("/health")
def health(): return {"status":"up"}