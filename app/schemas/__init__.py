from datetime import date
from pydantic import BaseModel, ConfigDict, Field

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class AutorIn(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    nacionalidad: str | None = Field(default=None, max_length=80)
class AutorOut(ORMModel):
    id: int
    nombre: str
    nacionalidad: str | None

class CategoriaIn(BaseModel):
    nombre: str = Field(min_length=1, max_length=80)
    descripcion: str | None = None
class CategoriaOut(ORMModel):
    id: int
    nombre: str
    descripcion: str | None

class LibroIn(BaseModel):
    titulo: str = Field(min_length=1, max_length=150)
    isbn: str | None = None
    anio_publicacion: int | None = Field(default=None, ge=0, le=2100)
    autor_id: int
    ejemplares_disponibles: int = Field(default=1, ge=0)
    categorias: list[int] = Field(default_factory=list)
class SocioIn(BaseModel):
    nombre: str
    correo: str
    telefono: str | None = None
    activo: bool = True
class SocioOut(ORMModel):
    id: int
    nombre: str
    correo: str
    telefono: str | None
    activo: bool
class PrestamoIn(BaseModel):
    libro_id: int
    socio_id: int
    dias_prestamo: int = Field(default=14, ge=1, le=90)
class PagoMulta(BaseModel):
    monto: float = Field(gt=0)
