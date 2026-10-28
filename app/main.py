from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import Base, engine, probar_conexion
from app import models
from app.routes import autores, categorias, libros, socios, prestamos, reportes

@asynccontextmanager
async def lifespan(app: FastAPI):
    probar_conexion()
    Base.metadata.create_all(bind=engine)
    yield

app=FastAPI(
    title="API de Biblioteca",
    description="Gestión de autores, categorías, libros, socios, préstamos y reportes.",
    version="1.0.0",
    openapi_tags=[
        {"name":"Autores","description":"Administrar autores y sus libros."},
        {"name":"Categorías","description":"Administrar categorías."},
        {"name":"Libros","description":"Administrar libros."},
        {"name":"Socios","description":"Administrar socios."},
        {"name":"Préstamos","description":"Préstamos, devoluciones y multas."},
        {"name":"Reportes","description":"Estadísticas de la biblioteca."},
    ],
    lifespan=lifespan,
)
app.include_router(autores.router)
app.include_router(categorias.router)
app.include_router(libros.router)
app.include_router(socios.router)
app.include_router(prestamos.router)
app.include_router(reportes.router)

@app.get("/salud",include_in_schema=False)
def salud():
    probar_conexion()
    return {"estado":"conectado","base_de_datos":"PostgreSQL"}
