import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="IPTV Proxy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Modèles ───────────────────────────────────────────────────────────────────

class Credentials(BaseModel):
    host: str
    username: str
    password: str

# ─── Helpers ───────────────────────────────────────────────────────────────────

def build_api_url(host: str, username: str, password: str, action: str) -> str:
    host = host.rstrip("/")
    return f"{host}/player_api.php?username={username}&password={password}&action={action}"

async def xtream_get(url: str) -> dict:
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()

# ─── Routes Auth ───────────────────────────────────────────────────────────────

@app.post("/api/auth")
async def authenticate(creds: Credentials):
    """Vérifie les credentials et retourne les infos du compte."""
    url = f"{creds.host.rstrip('/')}/player_api.php?username={creds.username}&password={creds.password}"
    try:
        data = await xtream_get(url)
        if data.get("user_info", {}).get("auth") == 0:
            raise HTTPException(status_code=401, detail="Credentials invalides")
        return data
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Serveur IPTV injoignable: {str(e)}")

# ─── Routes Live TV ────────────────────────────────────────────────────────────

@app.get("/api/live/categories")
async def get_live_categories(host: str, username: str, password: str):
    url = build_api_url(host, username, password, "get_live_categories")
    try:
        return await xtream_get(url)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

@app.get("/api/live/streams")
async def get_live_streams(
    host: str, username: str, password: str,
    category_id: str = Query(default=None)
):
    action = "get_live_streams"
    url = build_api_url(host, username, password, action)
    if category_id:
        url += f"&category_id={category_id}"
    try:
        return await xtream_get(url)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

# ─── Routes VOD ────────────────────────────────────────────────────────────────

@app.get("/api/vod/categories")
async def get_vod_categories(host: str, username: str, password: str):
    url = build_api_url(host, username, password, "get_vod_categories")
    try:
        return await xtream_get(url)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

@app.get("/api/vod/streams")
async def get_vod_streams(
    host: str, username: str, password: str,
    category_id: str = Query(default=None)
):
    url = build_api_url(host, username, password, "get_vod_streams")
    if category_id:
        url += f"&category_id={category_id}"
    try:
        return await xtream_get(url)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

# ─── Proxy Stream (résout le CORS sur les flux vidéo) ─────────────────────────

@app.get("/api/stream/proxy")
async def proxy_stream(url: str):
    """
    Proxifie un flux HLS/M3U8 pour contourner les restrictions CORS.
    Le frontend appelle cette route au lieu du stream direct.
    """
    async def stream_generator():
        async with httpx.AsyncClient(timeout=30) as client:
            async with client.stream("GET", url) as response:
                async for chunk in response.aiter_bytes(chunk_size=8192):
                    yield chunk

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            head = await client.head(url)
            content_type = head.headers.get("content-type", "application/octet-stream")
    except:
        content_type = "application/vnd.apple.mpegurl"

    return StreamingResponse(stream_generator(), media_type=content_type)

# ─── Sanity check ──────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "IPTV Proxy running 🚀"}
