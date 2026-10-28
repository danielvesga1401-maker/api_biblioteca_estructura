from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.core.database import obtener_db
from app.models import Autor, Categoria, Libro, Prestamo, libro_categoria

router=APIRouter(prefix="/reportes",tags=["Reportes"])
@router.get("/libros-mas-prestados",summary="Reporte Libros Más Prestados")
def libros_mas_prestados(limite:int=Query(10,ge=1,le=100),db:Session=Depends(obtener_db)):
    q=select(Libro.id,Libro.titulo,Autor.nombre.label("autor"),func.count(Prestamo.id).label("total_prestamos")).join(Autor).outerjoin(Prestamo).group_by(Libro.id,Libro.titulo,Autor.nombre).order_by(func.count(Prestamo.id).desc()).limit(limite)
    return db.execute(q).mappings().all()
@router.get("/categorias",summary="Reporte Categorías")
def reporte_categorias(db:Session=Depends(obtener_db)):
    q=select(Categoria.id,Categoria.nombre,func.count(func.distinct(libro_categoria.c.libro_id)).label("total_libros")).outerjoin(libro_categoria,libro_categoria.c.categoria_id==Categoria.id).group_by(Categoria.id,Categoria.nombre).order_by(Categoria.nombre)
    return db.execute(q).mappings().all()
