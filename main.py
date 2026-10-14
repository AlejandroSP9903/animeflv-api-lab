
import os
from fastapi import FastAPI, HTTPException, Query
from animeflv import AnimeFLV

app = FastAPI(
    title="AnimeFLV Render Lab",
    description="Laboratorio independiente para probar AnimeFLV",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "service": "AnimeFLV Render Lab",
        "status": "online",
        "docs": "/docs",
        "endpoints": [
            "/search?q=Naruto",
            "/anime/{anime_id}",
            "/episode/{episode_id}",
        ],
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
def search(q: str = Query(min_length=1, max_length=100)):
    try:
        with AnimeFLV() as api:
            result = api.search(q)
            return result
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error buscando en AnimeFLV: {exc}",
        )


@app.get("/anime/{anime_id}")
def anime_info(anime_id: str):
    try:
        with AnimeFLV() as api:
            result = api.getAnimeInfo(anime_id)
            return result
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error consultando anime: {exc}",
        )


@app.get("/episode/{episode_id:path}")
def episode_info(episode_id: str):
    try:
        with AnimeFLV() as api:
            result = api.downloadLinksByEpisodeID(episode_id)
            return result
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error consultando episodio: {exc}",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "10000")),
    )
