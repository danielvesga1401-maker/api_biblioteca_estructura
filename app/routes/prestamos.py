from datetime import date, timedelta
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.core.database import obtener_db
from app.models import Prestamo, Libro, Socio
from app.schemas import PrestamoIn, PagoMulta

router=APIRouter(prefix="/prestamos",tags=["Préstamos"])
def salida(p):
    return {"id":p.id,"libro_id":p.libro_id,"libro":p.libro.titulo,"socio_id":p.socio_id,"socio":p.socio.nombre,
            "fecha_prestamo":p.fecha_prestamo,"fecha_limite":p.fecha_limite,"fecha_devolucion":p.fecha_devolucion,
            "estado":p.estado,"multa":float(p.multa),"multa_pagada":p.multa_pagada}
@router.get("",summary="Listar Préstamos")
def todos(db:Session=Depends(obtener_db)):
    ps=db.scalars(select(Prestamo).options(joinedload(Prestamo.libro),joinedload(Prestamo.socio)).order_by(Prestamo.id.desc())).all()
    return [salida(p) for p in ps]
@router.post("",status_code=201,summary="Registrar Préstamo")
def crear(datos:PrestamoIn,db:Session=Depends(obtener_db)):
    l=db.scalar(select(Libro).where(Libro.id==datos.libro_id).with_for_update())
    if l is None: raise HTTPException(404,"Libro no encontrado")
    s=db.get(Socio,datos.socio_id)
    if s is None: raise HTTPException(404,"Socio no encontrado")
    if not s.activo: raise HTTPException(400,"El socio está inactivo")
    if l.ejemplares_disponibles<1: raise HTTPException(400,"No hay ejemplares disponibles")
    l.ejemplares_disponibles-=1
    p=Prestamo(libro_id=l.id,socio_id=s.id,fecha_limite=date.today()+timedelta(days=datos.dias_prestamo))
    db.add(p); db.commit(); db.refresh(p)
    return p
@router.get("/{id}",summary="Obtener Préstamo")
def uno(id:int,db:Session=Depends(obtener_db)):
    p=db.scalar(select(Prestamo).options(joinedload(Prestamo.libro),joinedload(Prestamo.socio)).where(Prestamo.id==id))
    if p is None: raise HTTPException(404,"Préstamo no encontrado")
    return salida(p)
@router.post("/{id}/devolucion",summary="Registrar Devolución")
def devolucion(id:int,db:Session=Depends(obtener_db)):
    p=db.scalar(select(Prestamo).where(Prestamo.id==id).with_for_update())
    if p is None: raise HTTPException(404,"Préstamo no encontrado")
    if p.estado=="devuelto": raise HTTPException(400,"Este préstamo ya fue devuelto")
    hoy=date.today(); atraso=max((hoy-p.fecha_limite).days,0)
    p.fecha_devolucion=hoy; p.estado="devuelto"; p.multa=Decimal(atraso*1000)
    l=db.get(Libro,p.libro_id); l.ejemplares_disponibles+=1
    db.commit()
    return {"mensaje":"Devolución registrada","prestamo_id":id,"fecha_devolucion":hoy,"dias_atraso":atraso,"multa":float(p.multa)}
@router.post("/{id}/multa/pago",summary="Pagar Multa")
def pagar(id:int,datos:PagoMulta,db:Session=Depends(obtener_db)):
    p=db.get(Prestamo,id)
    if p is None: raise HTTPException(404,"Préstamo no encontrado")
    if p.estado!="devuelto": raise HTTPException(400,"Registra primero la devolución")
    if p.multa<=0: raise HTTPException(400,"Este préstamo no tiene multa")
    if p.multa_pagada: raise HTTPException(400,"La multa ya fue pagada")
    if Decimal(str(datos.monto))<p.multa: raise HTTPException(400,f"El pago debe ser al menos {p.multa}")
    p.multa_pagada=True; db.commit(); db.refresh(p); return p
