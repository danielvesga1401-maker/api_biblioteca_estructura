from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

def obtener(db, modelo, registro_id: int, nombre="Registro"):
    obj = db.get(modelo, registro_id)
    if obj is None:
        raise HTTPException(status_code=404, detail=f"{nombre} no encontrado.")
    return obj

def listar(db, modelo):
    return db.scalars(select(modelo).order_by(modelo.id)).all()

def guardar(db, obj):
    db.add(obj)
    try:
        db.commit()
        db.refresh(obj)
        return obj
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Dato duplicado o relación inválida.") from exc

def eliminar(db, obj):
    db.delete(obj)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="No se puede eliminar porque el registro está relacionado con otros datos.") from exc
