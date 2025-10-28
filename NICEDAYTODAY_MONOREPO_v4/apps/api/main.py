from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import qrcode, io
from fastapi.responses import StreamingResponse

app = FastAPI(title="CrateJuice API")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.get("/")
def root(): return {"ok": True, "msg": "CrateJuice API live"}

@app.get("/health")
def health(): return {"status":"up"}

@app.get("/qr")
def qr(link: str = Query(...)):
    qr_img = qrcode.make(link)
    buf = io.BytesIO()
    qr_img.save(buf, format='PNG')
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
