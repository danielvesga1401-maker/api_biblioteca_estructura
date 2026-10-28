from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.core.database import obtener_db
from app.controllers.crud import obtener, guardar, eliminar
from app.models import Libro, Autor, Categoria
from app.schemas import LibroIn

router = APIRouter(prefix="/libros", tags=["Libros"])
def salida(l):
    return {"id":l.id,"titulo":l.titulo,"isbn":l.isbn,"anio_publicacion":l.anio_publicacion,
            "autor_id":l.autor_id,"autor":l.autor.nombre,"ejemplares_disponibles":l.ejemplares_disponibles,
            "categorias":[{"id":c.id,"nombre":c.nombre} for c in l.categorias]}
@router.get("", summary="Listar Libros")
def todos(db: Session = Depends(obtener_db)):
    libros=db.scalars(select(Libro).options(selectinload(Libro.autor),selectinload(Libro.categorias)).order_by(Libro.id)).all()
    return [salida(l) for l in libros]
@router.post("", status_code=201, summary="Crear Libro")
def crear(datos: LibroIn, db: Session = Depends(obtener_db)):
    d=datos.model_dump(); ids=d.pop("categorias")
    if db.get(Autor,d["autor_id"]) is None: raise HTTPException(400,"El autor no existe")
    cats=[]
    for cid in ids:
        c=db.get(Categoria,cid)
        if c is None: raise HTTPException(400,f"La categoría {cid} no existe")
        cats.append(c)
    l=Libro(**d,categorias=cats); guardar(db,l)
    l=db.scalar(select(Libro).options(selectinload(Libro.autor),selectinload(Libro.categorias)).where(Libro.id==l.id))
    return salida(l)
@router.get("/{id}", summary="Obtener Libro")
def uno(id: int, db: Session = Depends(obtener_db)):
    l=db.scalar(select(Libro).options(selectinload(Libro.autor),selectinload(Libro.categorias)).where(Libro.id==id))
    if l is None: raise HTTPException(404,"Libro no encontrado")
    return salida(l)
@router.put("/{id}", summary="Actualizar Libro")
def actualizar(id: int, datos: LibroIn, db: Session = Depends(obtener_db)):
    l=obtener(db,Libro,id,"Libro"); d=datos.model_dump(); ids=d.pop("categorias")
    if db.get(Autor,d["autor_id"]) is None: raise HTTPException(400,"El autor no existe")
    cats=[]
    for cid in ids:
        c=db.get(Categoria,cid)
        if c is None: raise HTTPException(400,f"La categoría {cid} no existe")
        cats.append(c)
    for k,v in d.items(): setattr(l,k,v)
    l.categorias=cats; guardar(db,l)
    return uno(id,db)
@router.delete("/{id}", summary="Eliminar Libro")
def borrar(id: int, db: Session = Depends(obtener_db)):
    eliminar(db,obtener(db,Libro,id,"Libro")); return {"mensaje":"Libro eliminado"}
