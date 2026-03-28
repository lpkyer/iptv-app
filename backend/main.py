import httpx
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response
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

# ─── Proxy Stream HLS-aware ────────────────────────────────────────────────────

from urllib.parse import urljoin, urlparse, urlencode, quote
import re

def is_m3u8_content_type(ct: str) -> bool:
    return any(x in ct for x in ["mpegurl", "m3u8", "x-mpegURL"])

def rewrite_m3u8(content: str, original_url: str) -> str:
    """
    Réécrit toutes les URLs dans un manifest M3U8 pour les faire passer par le proxy.
    Gère les URLs absolues et relatives.
    """
    lines = content.splitlines()
    rewritten = []

    for line in lines:
        stripped = line.strip()

        # Tags avec URI= inline (ex: #EXT-X-KEY:METHOD=AES-128,URI="http://...")
        if stripped.startswith("#") and 'URI="' in stripped:
            def replace_uri(match):
                inner_url = match.group(1)
                abs_url = urljoin(original_url, inner_url)
                proxied = f'/api/stream/proxy?url={quote(abs_url, safe="")}'
                return f'URI="{proxied}"'
            rewritten.append(re.sub(r'URI="([^"]+)"', replace_uri, line))

        # Lignes qui sont des URLs (segments .ts, .m3u8, etc.) — pas des tags #
        elif stripped and not stripped.startswith("#"):
            abs_url = urljoin(original_url, stripped)
            rewritten.append(f'/api/stream/proxy?url={quote(abs_url, safe="")}')

        else:
            rewritten.append(line)

    return "\n".join(rewritten)


@app.get("/api/stream/proxy")
async def proxy_stream(url: str, request: Request):
    """
    Proxy HLS-aware :
    - Si la réponse est un manifest M3U8, réécrit toutes les URLs de segments
      pour qu'ils passent aussi par ce proxy (résout le CORS sur les .ts).
    - Sinon, streame les bytes bruts (segments vidéo, clés AES, etc.).
    """
    headers_to_forward = {}
    range_header = request.headers.get("range")
    if range_header:
        headers_to_forward["range"] = range_header

    url_path = url.split("?")[0]

    # ── Manifest M3U8 : fetch complet + réécriture URLs ──────────────────────
    if url_path.endswith(".m3u8") or url_path.endswith(".m3u"):
        try:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                response = await client.get(url, headers=headers_to_forward)
                rewritten = rewrite_m3u8(response.text, url)
                return Response(
                    content=rewritten,
                    media_type="application/vnd.apple.mpegurl",
                    headers={
                        "Access-Control-Allow-Origin": "*",
                        "Cache-Control": "no-cache",
                    }
                )
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Timeout manifest")
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=str(e))

    # ── Segments binaires (.ts, clés AES) : stream direct, SANS Content-Length
    async def stream_generator():
        try:
            async with httpx.AsyncClient(timeout=60, follow_redirects=True) as c:
                async with c.stream("GET", url, headers=headers_to_forward) as r:
                    async for chunk in r.aiter_bytes(chunk_size=32768):
                        yield chunk
        except Exception:
            return

    return StreamingResponse(
        stream_generator(),
        status_code=200,
        media_type="video/mp2t",
        headers={"Access-Control-Allow-Origin": "*"},
    )

# ─── Sanity check ──────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "IPTV Proxy running 🚀"}