from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import obtener_db
from app.controllers.crud import obtener, listar, guardar, eliminar
from app.models import Autor, Libro
from app.schemas import AutorIn, AutorOut

router = APIRouter(prefix="/autores", tags=["Autores"])
@router.get("", response_model=list[AutorOut], summary="Listar Autores")
def todos(db: Session = Depends(obtener_db)): return listar(db, Autor)
@router.post("", response_model=AutorOut, status_code=201, summary="Crear Autor")
def crear(datos: AutorIn, db: Session = Depends(obtener_db)): return guardar(db, Autor(**datos.model_dump()))
@router.get("/{id}", response_model=AutorOut, summary="Obtener Autor")
def uno(id: int, db: Session = Depends(obtener_db)): return obtener(db, Autor, id, "Autor")
@router.put("/{id}", response_model=AutorOut, summary="Actualizar Autor")
def actualizar(id: int, datos: AutorIn, db: Session = Depends(obtener_db)):
    obj = obtener(db, Autor, id, "Autor")
    for k,v in datos.model_dump().items(): setattr(obj,k,v)
    return guardar(db,obj)
@router.delete("/{id}", summary="Eliminar Autor")
def borrar(id: int, db: Session = Depends(obtener_db)):
    eliminar(db, obtener(db, Autor, id, "Autor")); return {"mensaje":"Autor eliminado"}
@router.get("/{id}/libros", summary="Listar Libros Autor")
def libros(id: int, db: Session = Depends(obtener_db)):
    obtener(db, Autor, id, "Autor")
    return db.scalars(select(Libro).where(Libro.autor_id == id)).all()
