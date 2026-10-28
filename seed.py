"""Datos de ejemplo opcionales: py seed.py"""
from sqlalchemy import select
from app.core.database import Base, engine, SessionLocal, probar_conexion
from app import models
from app.models import Autor, Categoria, Libro, Socio

probar_conexion()
Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    a=db.scalar(select(Autor).where(Autor.nombre=="Gabriel García Márquez"))
    if a is None:
        a=Autor(nombre="Gabriel García Márquez",nacionalidad="Colombiana"); db.add(a); db.flush()
    c=db.scalar(select(Categoria).where(Categoria.nombre=="Novela"))
    if c is None:
        c=Categoria(nombre="Novela",descripcion="Obras narrativas"); db.add(c); db.flush()
    s=db.scalar(select(Socio).where(Socio.correo=="socio@example.com"))
    if s is None: db.add(Socio(nombre="Socio de prueba",correo="socio@example.com"))
    l=db.scalar(select(Libro).where(Libro.titulo=="Cien años de soledad"))
    if l is None: db.add(Libro(titulo="Cien años de soledad",autor_id=a.id,ejemplares_disponibles=3,categorias=[c]))
    db.commit()
print("Datos de ejemplo insertados o ya existentes.")
