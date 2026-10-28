from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import obtener_db
from app.controllers.crud import obtener, listar, guardar, eliminar
from app.models import Categoria
from app.schemas import CategoriaIn, CategoriaOut

router = APIRouter(prefix="/categorias", tags=["Categorías"])
@router.get("", response_model=list[CategoriaOut], summary="Listar Categorías")
def todos(db: Session = Depends(obtener_db)): return listar(db, Categoria)
@router.post("", response_model=CategoriaOut, status_code=201, summary="Crear Categoría")
def crear(datos: CategoriaIn, db: Session = Depends(obtener_db)): return guardar(db, Categoria(**datos.model_dump()))
@router.get("/{id}", response_model=CategoriaOut, summary="Obtener Categoría")
def uno(id: int, db: Session = Depends(obtener_db)): return obtener(db, Categoria, id, "Categoría")
@router.put("/{id}", response_model=CategoriaOut, summary="Actualizar Categoría")
def actualizar(id: int, datos: CategoriaIn, db: Session = Depends(obtener_db)):
    obj=obtener(db,Categoria,id,"Categoría")
    for k,v in datos.model_dump().items(): setattr(obj,k,v)
    return guardar(db,obj)
@router.delete("/{id}", summary="Eliminar Categoría")
def borrar(id: int, db: Session = Depends(obtener_db)):
    eliminar(db,obtener(db,Categoria,id,"Categoría")); return {"mensaje":"Categoría eliminada"}
