from sqlalchemy.orm import Session
from app.models.copy import Copy
from app.models.tag import Tag
from app.models.image import Image

def create_copy(db: Session, game_id: int, copy_data: dict):
    copy = Copy(game_id=game_id, **copy_data)
    db.add(copy)
    db.commit()
    db.refresh(copy)
    return copy

def get_copy(db: Session, copy_id: int):
    return db.query(Copy).filter(Copy.id == copy_id).first()

def get_copies_for_game(db: Session, game_id: int):
    return db.query(Copy).filter(Copy.game_id == game_id).all()

def update_copy(db: Session, copy_id: int, update_data: dict):
    copy = get_copy(db, copy_id)
    if not copy:
        return None
    for key, value in update_data.items():
        setattr(copy, key, value)
    db.commit()
    db.refresh(copy)
    return copy

def delete_copy(db: Session, copy_id: int):
    copy = get_copy(db, copy_id)
    if not copy:
        return False
    db.delete(copy)
    db.commit()
    return True

def create_tag(db: Session, name: str):
    tag = Tag(name=name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

def get_tag_by_name(db: Session, name: str):
    return db.query(Tag).filter(Tag.name == name).first()

def get_tag(db: Session, tag_id: int):
    return db.query(Tag).filter(Tag.id == tag_id).first()

def list_tags(db: Session):
    return db.query(Tag).all()

def delete_tag(db: Session, tag_id: int):
    tag = get_tag(db, tag_id)
    if not tag:
        return False
    db.delete(tag)
    db.commit()
    return True

def add_tag_to_copy(db: Session, copy: Copy, tag: Tag):
    if tag not in copy.tags:
        copy.tags.append(tag)
        db.commit()
        db.refresh(copy)
    return copy

def remove_tag_from_copy(db: Session, copy: Copy, tag: Tag):
    if tag in copy.tags:
        copy.tags.remove(tag)
        db.commit()
        db.refresh(copy)
    return copy

def create_image(db: Session, copy_id: int, file_path: str, description: str = None):
    image = Image(copy_id=copy_id, file_path=file_path, description=description)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

def get_image(db: Session, image_id: int):
    return db.query(Image).filter(Image.id == image_id).first()

def get_images_for_copy(db: Session, copy_id: int):
    return db.query(Image).filter(Image.copy_id == copy_id).all()

def delete_image(db: Session, image_id: int):
    image = get_image(db, image_id)
    if not image:
        return False
    db.delete(image)
    db.commit()
    return True
