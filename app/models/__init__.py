from datetime import date, timedelta
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Numeric, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

libro_categoria = Table(
    "libro_categoria", Base.metadata,
    Column("libro_id", ForeignKey("libros.id", ondelete="CASCADE"), primary_key=True),
    Column("categoria_id", ForeignKey("categorias.id", ondelete="CASCADE"), primary_key=True),
)

class Autor(Base):
    __tablename__ = "autores"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    nacionalidad: Mapped[str | None] = mapped_column(String(80))
    libros: Mapped[list["Libro"]] = relationship(back_populates="autor")

class Categoria(Base):
    __tablename__ = "categorias"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text)
    libros: Mapped[list["Libro"]] = relationship(secondary=libro_categoria, back_populates="categorias")

class Libro(Base):
    __tablename__ = "libros"
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    isbn: Mapped[str | None] = mapped_column(String(20), unique=True)
    anio_publicacion: Mapped[int | None] = mapped_column(Integer)
    autor_id: Mapped[int] = mapped_column(ForeignKey("autores.id"), nullable=False)
    ejemplares_disponibles: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    autor: Mapped["Autor"] = relationship(back_populates="libros")
    categorias: Mapped[list["Categoria"]] = relationship(secondary=libro_categoria, back_populates="libros")
    prestamos: Mapped[list["Prestamo"]] = relationship(back_populates="libro")

class Socio(Base):
    __tablename__ = "socios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    correo: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(30))
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    prestamos: Mapped[list["Prestamo"]] = relationship(back_populates="socio")

class Prestamo(Base):
    __tablename__ = "prestamos"
    id: Mapped[int] = mapped_column(primary_key=True)
    libro_id: Mapped[int] = mapped_column(ForeignKey("libros.id"), nullable=False)
    socio_id: Mapped[int] = mapped_column(ForeignKey("socios.id"), nullable=False)
    fecha_prestamo: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    fecha_limite: Mapped[date] = mapped_column(Date, default=lambda: date.today() + timedelta(days=14), nullable=False)
    fecha_devolucion: Mapped[date | None] = mapped_column(Date)
    estado: Mapped[str] = mapped_column(String(20), default="activo", nullable=False)
    multa: Mapped[float] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    multa_pagada: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    libro: Mapped["Libro"] = relationship(back_populates="prestamos")
    socio: Mapped["Socio"] = relationship(back_populates="prestamos")
