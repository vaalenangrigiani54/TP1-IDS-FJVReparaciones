from sqlalchemy.sql import func #es el remplazo del date time y funciono para resolver el problema con el horario adelantado por 2 horas y 10 minutos
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# cada fila que tiene el atributo unique es que significa que hay un unico valor y que no puede haber mas valores iguales 

#en las tres tablas esta como primary key id(comentario en linea 27)
class Usuarios(db.Model):
    __name__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    contrasenia = db.Column(db.String(20), nullable=False) # 20 caracteres como máximo
    rango = db.Column(db.String(15), nullable=False)
    #aca en este caso tuvimos que problemas con el horario 
    #ya que la base de datos tomaba el horario de argentina en cambio phyton lo cual nos llevo a usar server_default
    fecha_ingreso = db.Column(db.DateTime(timezone=True), server_default=func.now())

class Clientes(db.Model):
    __name__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    codigo_ingreso = db.Column(db.Integer, unique=True, nullable=False) # 8 dígitos y no se puede repetir
    fecha_inscripcion = db.Column(db.DateTime(timezone=True), server_default=func.now())

#en esta tabla a diferencia de las otros usa dos foreignkey para las columnas id cliente y id tecnico
class Equipos(db.Model):
    __name__ = "equipos"
    id = db.Column(db.Integer, primary_key=True)
    tipo_equipo = db.Column(db.String(255), nullable=False)
    marca = db.Column(db.String(255), nullable=False)
    modelo = db.Column(db.String(255), nullable=False)
    num_serie = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(30), nullable=False) # Nuevo Ingreso; En Revisión/Reparación; Reparado; No Reparado
    observaciones = db.Column(db.String(500)) # Esto es para que el técnico le explique al cliente lo que pudo reparar y/o lo que no
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id"))
    id_tecnico = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    fecha_ingreso = db.Column(db.DateTime(timezone=True), server_default=func.now())
