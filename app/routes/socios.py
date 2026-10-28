from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import obtener_db
from app.controllers.crud import obtener, listar, guardar, eliminar
from app.models import Socio, Prestamo
from app.schemas import SocioIn, SocioOut

router=APIRouter(prefix="/socios",tags=["Socios"])
@router.get("",response_model=list[SocioOut],summary="Listar Socios")
def todos(db:Session=Depends(obtener_db)): return listar(db,Socio)
@router.post("",response_model=SocioOut,status_code=201,summary="Crear Socio")
def crear(datos:SocioIn,db:Session=Depends(obtener_db)): return guardar(db,Socio(**datos.model_dump()))
@router.get("/{id}",response_model=SocioOut,summary="Obtener Socio")
def uno(id:int,db:Session=Depends(obtener_db)): return obtener(db,Socio,id,"Socio")
@router.put("/{id}",response_model=SocioOut,summary="Actualizar Socio")
def actualizar(id:int,datos:SocioIn,db:Session=Depends(obtener_db)):
    o=obtener(db,Socio,id,"Socio")
    for k,v in datos.model_dump().items(): setattr(o,k,v)
    return guardar(db,o)
@router.delete("/{id}",summary="Eliminar Socio")
def borrar(id:int,db:Session=Depends(obtener_db)):
    eliminar(db,obtener(db,Socio,id,"Socio")); return {"mensaje":"Socio eliminado"}
@router.get("/{id}/prestamos",summary="Listar Préstamos Socio")
def prestamos(id:int,db:Session=Depends(obtener_db)):
    obtener(db,Socio,id,"Socio")
    return db.scalars(select(Prestamo).where(Prestamo.socio_id==id).order_by(Prestamo.id.desc())).all()
