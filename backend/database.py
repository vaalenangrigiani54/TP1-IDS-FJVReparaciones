import datetime as dt
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Usuarios(db.Model):
    __name__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    contrasenia = db.Column(db.String(20), nullable=False) # 15 caracteres como máximo
    rango = db.Column(db.String(15), nullable=False)
    fecha_ingreso = db.Column(db.DateTime, default=dt.datetime.now())


class Clientes(db.Model):
    __name__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    codigo_ingreso = db.Column(db.Integer, unique=True, nullable=False) # 8 dígitos y no se puede repetir
    fecha_inscripcion = db.Column(db.DateTime, default=dt.datetime.now())


class Equipos(db.Model):
    __name__ = "equipos"
    id = db.Column(db.Integer, primary_key=True)
    tipo_equipo = db.Column(db.String(255), nullable=False)
    marca = db.Column(db.String(255), nullable=False)
    modelo = db.Column(db.String(255), nullable=False)
    num_serie = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(30), nullable=False) # Nuevo Ingreso | En revisión | En reparación | Reparado | No reparado
    observaciones = db.Column(db.String(500)) # Esto es para que el técnico le explique al cliente lo que pudo reparar y/o lo que no
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id"))
    id_tecnico = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    fecha_ingreso = db.Column(db.DateTime, default=dt.datetime.now())