from sqlalchemy.sql import func # Es el reemplazo de datetime y funcionó para resolver el problema con el horario atrasado por 3 horas y 10 minutos
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Cada fila que tiene el atributo 'unique' significa que hay un único valor y que no puede haber más valores iguales

class Usuarios(db.Model):
    __name__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    contrasenia = db.Column(db.String(20), nullable=False) # 20 caracteres como máximo
    rango = db.Column(db.String(15), nullable=False)
    # Acá es donde tuvimos problemas con el horario, ya que la base de datos ahora toma el horario de Argentina.
    # En cambio python no, lo cual nos llevo a usar el atributo server_default (Lo mismo está en las otras dos tablas)
    fecha_ingreso = db.Column(db.DateTime(timezone=True), server_default=func.now())

class Clientes(db.Model):
    __name__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    codigo_ingreso = db.Column(db.Integer, unique=True, nullable=False) # 8 dígitos y no se puede repetir
    fecha_inscripcion = db.Column(db.DateTime(timezone=True), server_default=func.now())

# Esta tabla usa 2 foreign keys para las columnas id_cliente (relación con la tabla 'clientes') e id_tecnico (relación con la tabla 'usuarios')
class Equipos(db.Model):
    __name__ = "equipos"
    id = db.Column(db.Integer, primary_key=True)
    tipo_equipo = db.Column(db.String(255), nullable=False)
    marca = db.Column(db.String(255), nullable=False)
    modelo = db.Column(db.String(255), nullable=False)
    num_serie = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(30), nullable=False) # Nuevo Ingreso; En revisión/reparación; Reparado; No Reparado
    observaciones = db.Column(db.String(500)) # Esto es para que el técnico le explique al cliente lo que pudo reparar y/o lo que no
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id"))
    id_tecnico = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    fecha_ingreso = db.Column(db.DateTime(timezone=True), server_default=func.now())
