from datetime import datetime, timezone
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Body, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

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
from app.schemas.game import GameBase, GameDetail
from app.schemas.copy import CopyBase, CopyCreate, CopyUpdate
from app.schemas.tag import TagBase, TagCreate
from app.schemas.image import ImageBase, ImageCreate
from app.crud import (
    create_copy,
    get_copies_for_game,
    update_copy,
    create_tag,
    get_tag_by_name,
    list_tags,
    delete_tag,
    add_tag_to_copy,
    remove_tag_from_copy,
    get_copy,
    get_tag,
    create_image,
    get_images_for_copy,
    delete_image,
)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

def get_or_create(session: Session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return instance

@app.post("/admin/import-game")
def import_game(igdb_id: IGDBGameID, db: Session = Depends(get_db)):
    token = get_twitch_token()
    game_details = igdb_get_game_details(igdb_id.igdb_id, token)
    if not game_details:
        raise HTTPException(status_code=404, detail="Game not found in IGDB")

    genres = [get_or_create(db, Genre, name=genre['name']) for genre in game_details.get('genres', [])]
    themes = [get_or_create(db, Theme, name=theme['name']) for theme in game_details.get('themes', [])]
    modes = [get_or_create(db, Mode, name=mode['name']) for mode in game_details.get('game_modes', [])]
    perspectives = [get_or_create(db, Perspective, name=pers['name']) for pers in game_details.get('player_perspectives', [])]

    series = None
    if game_details.get("series"):
        series = get_or_create(db, Series, name=game_details["series"]["name"])

    developers, publishers = [], []
    for ic in game_details.get('involved_companies', []):
        name = ic["company"]["name"]
        company = get_or_create(db, Company, name=name)
        if ic.get("developer"):
            developers.append(company)
        if ic.get("publisher"):
            publishers.append(company)

    release_date = None
    if game_details.get("first_release_date"):
        try:
            release_date = datetime.fromtimestamp(game_details["first_release_date"], timezone.utc).date()
        except Exception:
            release_date = None

    game = get_or_create(
        db,
        Game,
        igdb_id=game_details["id"],
        name=game_details.get("name", ""),
        cover_url=game_details.get("cover", {}).get("url", ""),
        summary=game_details.get("summary", ""),
        release_date=release_date,
        series=series
    )

    game.genres = genres
    game.themes = themes
    game.modes = modes
    game.perspectives = perspectives
    game.developers = developers
    game.publishers = publishers

    db.add(game)
    db.commit()
    db.refresh(game)

    return {"imported_game": game.name, "id": game.id}

def fix_cover_url(url: str) -> Optional[str]:
    if not url:
        return None
    url = url.replace("t_thumb", "t_cover_big")
    if url.startswith("//"):
        url = "https:" + url
    elif not url.startswith("http"):
        url = "https://" + url
    return url

def extract_year_from_date(date):
    if not date:
        return None
    try:
        return date.year
    except Exception:
        return None

@app.get("/admin/games", response_model=List[GameBase])
def api_list_games(db: Session = Depends(get_db)):
    games = db.query(Game).all()
    result = []
    for game in games:
        release_year = extract_year_from_date(game.release_date)
        cover_url = fix_cover_url(game.cover_url)
        result.append(
            GameBase(
                id=game.id,
                igdb_id=game.igdb_id,
                name=game.name,
                cover_url=cover_url,
                release_year=release_year
            )
        )
    return result


@app.get("/admin/games/{game_id}", response_model=GameDetail)
def api_get_game_detail(game_id: int, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@app.get("/admin/games/{game_id}/copies", response_model=List[CopyBase])
def api_list_copies(game_id: int, db: Session = Depends(get_db)):
    copies = get_copies_for_game(db, game_id)
    return copies

@app.post("/admin/games/{game_id}/copies", response_model=CopyBase)
def api_create_copy(game_id: int, copy: CopyCreate, db: Session = Depends(get_db)):
    db_copy = create_copy(db, game_id=game_id, copy_data=copy.model_dump(exclude_unset=True))
    return db_copy

@app.put("/admin/copies/{copy_id}", response_model=CopyBase)
def api_update_copy(copy_id: int, copy_update: CopyUpdate, db: Session = Depends(get_db)):
    copy = update_copy(db, copy_id, copy_update.model_dump(exclude_unset=True))
    if not copy:
        raise HTTPException(status_code=404, detail="Copy not found")
    return copy

@app.post("/admin/tags", response_model=TagBase)
def api_create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    existing = get_tag_by_name(db, tag.name)
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")
    return create_tag(db, tag.name)

@app.get("/admin/tags", response_model=List[TagBase])
def api_list_tags(db: Session = Depends(get_db)):
    return list_tags(db)

@app.delete("/admin/tags/{tag_id}", status_code=204)
def api_delete_tag(tag_id: int, db: Session = Depends(get_db)):
    success = delete_tag(db, tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")

@app.post("/admin/copies/{copy_id}/tags/{tag_id}", response_model=TagBase)
def api_add_tag_to_copy(copy_id: int, tag_id: int, db: Session = Depends(get_db)):
    copy = get_copy(db, copy_id)
    if not copy:
        raise HTTPException(status_code=404, detail="Copy not found")
    tag = get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    updated_copy = add_tag_to_copy(db, copy, tag)
    return tag

@app.delete("/admin/copies/{copy_id}/tags/{tag_id}", status_code=204)
def api_remove_tag_from_copy(copy_id: int, tag_id: int, db: Session = Depends(get_db)):
    copy = get_copy(db, copy_id)
    if not copy:
        raise HTTPException(status_code=404, detail="Copy not found")
    tag = get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    updated_copy = remove_tag_from_copy(db, copy, tag)

@app.post("/admin/copies/{copy_id}/images", response_model=ImageBase)
def api_create_image(copy_id: int, image: ImageCreate = Body(...), db: Session = Depends(get_db)):
    img = create_image(db, copy_id, image.file_path, image.description)
    return img

@app.get("/admin/copies/{copy_id}/images", response_model=List[ImageBase])
def api_list_images(copy_id: int, db: Session = Depends(get_db)):
    images = get_images_for_copy(db, copy_id)
    return images

@app.delete("/admin/images/{image_id}", status_code=204)
def api_delete_image(image_id: int, db: Session = Depends(get_db)):
    success = delete_image(db, image_id)
    if not success:
        raise HTTPException(status_code=404, detail="Image not found")
