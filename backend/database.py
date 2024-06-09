import datetime as dt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuarios(db.Model):
    __name__ = "usuarios"
    ID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Contrasenia = db.Column(db.String(255), nullable=False)
    Rango = db.Column(db.String(15), nullable=False)
    Fecha_Ingreso = db.Column(db.DateTime, default=dt.datetime.now())

class Clientes(db.Model):
    __name__ = "clientes"
    ID = db.Column(db.Integer, primary_key=True)
    Nombre_Cliente = db.Column(db.String(255), unique=True, nullable=False)
    Fecha_Ingreso = db.Column(db.DateTime, default=dt.datetime.now())

class Equipos(db.Model):
    __name__ = "equipos"
    ID = db.Column(db.Integer, primary_key=True)
    Tipo_Equipo = db.Column(db.String(255), nullable=False)
    Marca = db.Column(db.String(255), nullable=False)
    Modelo = db.Column(db.String(255), nullable=False)
    Num_Serie = db.Column(db.String(255), nullable=False)
    ID_Cliente = db.Column(db.Integer, db.ForeignKey("clientes.ID"))
    ID_Tecnico = db.Column(db.Integer, db.ForeignKey("usuarios.ID"))
    Fecha_Ingreso = db.Column(db.DateTime, default=dt.datetime.now())
