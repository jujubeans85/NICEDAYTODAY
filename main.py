
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import os, subprocess, glob, time, pathlib, re, shutil

APP = pathlib.Path(__file__).parent.resolve()
STORE = APP / "store"
STORE.mkdir(exist_ok=True)

app = FastAPI(title="CJ-19 Ripper")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SAFE = re.compile(r"[^a-zA-Z0-9._-]+")
def safe(s): 
    s = SAFE.sub("_", s).strip("_")
    return s or f"track_{int(time.time())}"

@app.get("/health")
def health(): 
    return {"ok": True, "ffmpeg": shutil.which("ffmpeg") is not None}

@app.get("/recent")
def recent(limit: int = 50):
    files = sorted(STORE.glob("*.mp3"), key=lambda p: p.stat().st_mtime, reverse=True)
    return {"items":[{"file":f.name,"size":f.stat().st_size,"url":f"/dl/{f.name}"} for f in files[:limit]]}

@app.get("/dl/{name}")
def dl(name: str):
    p = STORE / name
    if not p.exists(): 
        raise HTTPException(404, "not found")
    return FileResponse(str(p), media_type="audio/mpeg", filename=name)

class RipIn(BaseModel):
    url: HttpUrl
    title: Optional[str] = None

@app.post("/rip")
def rip(inp: RipIn):
    outtmpl = str(STORE / "%(uploader)s-%(title)s.%(ext)s")
    cmd = ["yt-dlp","-x","--audio-format","mp3","-o", outtmpl, str(inp.url)]
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        raise HTTPException(500, f"yt-dlp failed: {e}")

    mp3s = sorted(STORE.glob("*.mp3"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not mp3s: 
        raise HTTPException(500, "no mp3 produced")
    latest = mp3s[0]
    if inp.title:
        target = STORE / (safe(inp.title)+".mp3")
        if latest != target: 
            target.write_bytes(latest.read_bytes())
            latest = target
    return {"ok": True, "file": latest.name, "url": f"/dl/{latest.name}"}

class BatchIn(BaseModel):
    urls: List[HttpUrl]

@app.post("/batch")
def batch(inp: BatchIn):
    out = []
    for i,u in enumerate(inp.urls,1):
        try:
            res = rip(RipIn(url=u, title=f"cj_{i:03d}"))
            out.append({"ok":True,"url":str(u),"file":res["file"]})
        except Exception as e:
            out.append({"ok":False,"url":str(u),"error":str(e)})
    return {"ok": True, "count": len(out), "results": out}
