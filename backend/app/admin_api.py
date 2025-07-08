from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List
from app.igdb_helpers import (
    get_twitch_token,
    igdb_search_game,
    format_year,
    igdb_get_game_details,
)
from app.db import SessionLocal
from app.models.genre import Genre
from app.models.company import Company
from app.models.theme import Theme
from app.models.mode import Mode
from app.models.perspective import Perspective
from app.models.series import Series
from app.models.game import Game

app = FastAPI()

class IGDBGamePreview(BaseModel):
    id: int
    name: str
    year: str = ""
    genres: str = ""
    summary: str = ""
    cover_url: str = ""

@app.post("/admin/igdb-search", response_model=List[IGDBGamePreview])
def igdb_search(game_name: str = Body(..., embed=True)):
    token = get_twitch_token()
    results = igdb_search_game(game_name, token)
    previews = []
    for g in results:
        genres = ", ".join([genre["name"] for genre in g.get("genres", [])]) if g.get("genres") else ""
        year = format_year(g.get("first_release_date")) if g.get("first_release_date") else ""
        summary = g.get("summary", "")
        cover_url = g.get("cover", {}).get("url", "")
        previews.append(
            IGDBGamePreview(
                id=g["id"],
                name=g.get("name", ""),
                year=year,
                genres=genres,
                summary=summary[:120] + ("..." if len(summary) > 120 else ""),
                cover_url=cover_url,
            )
        )
    return previews

class IGDBGameID(BaseModel):
    igdb_id: int

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return instance

@app.post("/admin/import-game")
def import_game(igdb_id: IGDBGameID):
    token = get_twitch_token()
    game_details = igdb_get_game_details(igdb_id.igdb_id, token)
    if not game_details:
        raise HTTPException(status_code=404, detail="Game not found in IGDB")

    session = SessionLocal()
    genres = []
    for genre in game_details.get('genres', []):
        g = get_or_create(session, Genre, name=genre['name'])
        genres.append(g)
    themes = []
    for theme in game_details.get('themes', []):
        t = get_or_create(session, Theme, name=theme['name'])
        themes.append(t)
    modes = []
    for mode in game_details.get('game_modes', []):
        m = get_or_create(session, Mode, name=mode['name'])
        modes.append(m)
    perspectives = []
    for pers in game_details.get('player_perspectives', []):
        p = get_or_create(session, Perspective, name=pers['name'])
        perspectives.append(p)
    series = None
    if "series" in game_details and game_details["series"]:
        series = get_or_create(session, Series, name=game_details["series"]["name"])
    developers, publishers = [], []
    for ic in game_details.get('involved_companies', []):
        name = ic["company"]["name"]
        company = get_or_create(session, Company, name=name)
        if ic.get("developer"):
            developers.append(company)
        if ic.get("publisher"):
            publishers.append(company)

    game = get_or_create(
        session,
        Game,
        igdb_id=game_details["id"],
        name=game_details.get("name", ""),
        cover_url=game_details.get("cover", {}).get("url", ""),
        summary=game_details.get("summary", ""),
        series=series
    )

    game.genres = genres
    game.themes = themes
    game.modes = modes
    game.perspectives = perspectives
    game.developers = developers
    game.publishers = publishers

    session.add(game)
    session.commit()
    session.refresh(game)
    session.close()
    return {"imported_game": game.name, "id": game.id}
