from flask import Flask, request
from flask_cors import CORS
from sqlalchemy import desc
from database import *
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://vaalen782:2147483647@localhost:5432/tp1_ids"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

########################################################################################################################
########################################################################################################################

# Estas variables globales van a servir como control para que no se salteen la parte de login
ADMIN_SESSION_ID = 0
TECH_SESSION_ID = 0
CLIENT_SESSION_ID = 0

# Esta variable global sirve como control para no cambiar manualmente los query params de la id de un equipo
DEVICE_INFO_ID = 0


# Endpoint auxiliar para resetear las variables globales cuando se cierra sesión
@app.route("/reset_session")
def reset_session():
    global ADMIN_SESSION_ID, TECH_SESSION_ID, CLIENT_SESSION_ID, DEVICE_INFO_ID
    ADMIN_SESSION_ID = 0
    TECH_SESSION_ID = 0
    CLIENT_SESSION_ID = 0
    DEVICE_INFO_ID = 0
    return []


# Endpoint auxiliar para verificar si el usuario inició sesión o no
# Se debe hacer fetch() al mismo en todas las páginas
@app.route("/verify_session/<int:id>/<rango>")
def verify_session(id, rango):
    global ADMIN_SESSION_ID, TECH_SESSION_ID, CLIENT_SESSION_ID
    response = {"Logged": False}
    
    if id > 0:
        if rango == "administrador":
            if id == ADMIN_SESSION_ID:
                response["Logged"] = True
        elif rango == "tecnico":
            if id == TECH_SESSION_ID:
                response["Logged"] = True
        elif rango == "cliente":
            if id == CLIENT_SESSION_ID:
                response["Logged"] = True
    
    return response


# Endpoint auxiliar para verificar que no se cambien los query params de la id de un equipo
# Se debe hacer fetch() al mismo en todas las páginas que lo muestren
@app.route("/verify_deviceInfoID/<int:id>")
def verify_deviceInfoID(id):
    global DEVICE_INFO_ID
    response = {"ChangedParameter": True, "DeviceInfoID": DEVICE_INFO_ID}
    
    if id == DEVICE_INFO_ID and id > 0:
        response["ChangedParameter"] = False
    
    return response


# Por otra parte se necesita un endpoint auxiliar más para setear esa variable global que hace la verificación en el endpoint anterior
# Este endpoint se invoca desde las páginas que tienen la opción de mostrar un equipo
@app.route("/set_deviceInfoID/<id>")
def set_deviceInfoID(id):
    global DEVICE_INFO_ID
    DEVICE_INFO_ID = int(id)


########################################################################################################################
########################################################################################################################


# Endpoint para verificar el inicio de sesión de un usuario
@app.route("/loginUsuario/<email>/<contrasenia>")
def data_user(email, contrasenia):
    try:
        usuarios = Usuarios.query.where(Usuarios.email == email, Usuarios.contrasenia == contrasenia).all()
        datosUsuarios = []

        if len(usuarios) > 0:
            for usuario in usuarios:
                dictUsuario = {
                    "id": usuario.id,
                    "email": usuario.email,
                    "contrasenia": usuario.contrasenia,
                    "rango": usuario.rango
                }
                datosUsuarios.append(dictUsuario)
            
            #Con esto controlo que se haya iniciado sesión correctamente (Si hay un error no pasa por acá)
            if usuario.rango == "Administrador":
                global ADMIN_SESSION_ID
                ADMIN_SESSION_ID = datosUsuarios[0]["id"]
            elif usuario.rango == "Técnico":
                global TECH_SESSION_ID
                TECH_SESSION_ID = datosUsuarios[0]["id"]
            
        return datosUsuarios
    except Exception as error:
        print(f"\n\nERROR: {error}\n\n")
        return [{"Mensaje": "Algo ha fallado..."}]



# Endpoint para verificar el inicio de sesión de un cliente
@app.route("/loginCliente/<email>/<codigo>")
def data_client(email, codigo):
    try:
        clientes = Clientes.query.where(Clientes.email == email, Clientes.codigo_ingreso == codigo).all()
        datosClientes = []

        if len(clientes) > 0:
            for cliente in clientes:
                dictCliente = {
                    "id": cliente.id,
                    "email": cliente.email,
                    "codigo_ingreso": cliente.codigo_ingreso
                }
                datosClientes.append(dictCliente)
            
            #Con esto controlo que se haya iniciado sesión correctamente (Si hay un error no pasa por acá)
            global CLIENT_SESSION_ID
            CLIENT_SESSION_ID = datosClientes[0]["id"]

        return datosClientes
    except Exception as error:
        print(f"\n\nERROR: {error}\n\n")
        return [{"Mensaje": "Algo ha fallado..."}]


########################################################################################################################
########################################################################################################################


# Hace referencia a la página del administrador.
# Se obtienen todos los usuarios.
@app.route("/administrador/<id>")
def administrador(id):
    try:
        data = []
        usuarios = Usuarios.query.where(Usuarios.id != -1).order_by(Usuarios.id).all()
        
        for usuario in usuarios:
            usuarioData = {
                "id": usuario.id,
                "nombre_usuario": usuario.nombre_usuario,
                "email": usuario.email,
                "rango": usuario.rango,
                "fecha_ingreso": usuario.fecha_ingreso
            }
            data.append(usuarioData)
            
        return data
    except Exception as error:
        print(f"\n\nERROR: {error}\n\n")
        return {"Mensaje": "Algo ha fallado..."}



# Endpoint que hace referencia a la página del usuario técnico.
# Se obtienen todos los equipos que administra cierto técnico.
@app.route("/tecnico/<id>")
def tecnico(id):
    try:
        data = {"nombre_usuario": "", "equipos": []}
    
        usuario = Usuarios.query.where(Usuarios.id == id).first()
        equipos = Equipos.query.where(Equipos.id_tecnico == id).join(Clientes).add_columns(
            Clientes.nombre_cliente
        ).order_by(desc(Equipos.fecha_ingreso)).all()

        data["nombre_usuario"] = usuario.nombre_usuario
        
        for (equipo, nombre_cliente) in equipos:
            equipoData = {
                "id": equipo.id,
                "tipo_equipo": equipo.tipo_equipo,
                "marca": equipo.marca,
                "modelo": equipo.modelo,
                "num_serie": equipo.num_serie,
                "estado": equipo.estado,
                "observaciones": equipo.observaciones,
                "id_cliente": equipo.id_cliente,
                "nombre_cliente": nombre_cliente,
                "fecha_ingreso": equipo.fecha_ingreso
            }
            data["equipos"].append(equipoData)
          
        return data
    except Exception as error:
        print(f"\n\nERROR: {error}\n\n")
        return {"Mensaje": "Algo ha fallado..."}



# Endpoint que hace referencia a la página del cliente.
# Se obtienen todos los equipos que cierto cliente llevó a arreglar.
@app.route("/cliente/<id>")
def cliente(id):
    try:
        data = {"nombre_cliente": "", "equipos": []}

        cliente = Clientes.query.where(Clientes.id == id).first()
        equipos = Equipos.query.where(Equipos.id_cliente == id).join(Usuarios).add_columns(
            Usuarios.nombre_usuario
        ).order_by(desc(Equipos.fecha_ingreso)).all()
        
        data["nombre_cliente"] = cliente.nombre_cliente
        
        for (equipo, nombre_tecnico) in equipos:
            equipoData = {
                "id": equipo.id,
                "tipo_equipo": equipo.tipo_equipo,
                "marca": equipo.marca,
                "modelo": equipo.modelo,
                "num_serie": equipo.num_serie,
                "estado": equipo.estado,
                "observaciones": equipo.observaciones,
                "nombre_tecnico": nombre_tecnico,
                "fecha_ingreso": equipo.fecha_ingreso
            }
            data["equipos"].append(equipoData)

        return data
    except Exception as error:
        print(f"\n\nERROR: {error}\n\n")
        return {"Mensaje": "Algo ha fallado..."}


########################################################################################################################
########################################################################################################################


# Endpoint para consultar/agregar/modificar/eliminar a un usuario de la empresa
@app.route("/acciones_usuario/<id>", methods=["GET", "POST", "PUT", "DELETE"])
def acciones_usuario(id):
    try:
        if request.method == "GET": # Para ver la información del usuario
            usuario = Usuarios.query.get(id)
            return {
                "id": usuario.id,
                "nombre_usuario": usuario.nombre_usuario,
                "email": usuario.email,
                "contrasenia": usuario.contrasenia,
                "rango": usuario.rango,
                "fecha_ingreso": usuario.fecha_ingreso
            }
            
        elif request.method == "POST": # Para agregar un nuevo usuario (En este caso no se usa la id del parámetro)
            data = request.json
            nuevo_nombre = data.get("nombre_usuario")
            nuevo_email = data.get("email")
            nueva_contrasenia = data.get("contrasenia")
            nuevo_rango = data.get("rango")
        
            if len(Usuarios.query.where(Usuarios.email == nuevo_email).all()) > 0:
                return {"Mensaje": "El correo ingresado ya existe. Pruebe con otro distinto..."}
            else:
                usuario = Usuarios(nombre_usuario = nuevo_nombre, email = nuevo_email, contrasenia = nueva_contrasenia, rango = nuevo_rango)
                db.session.add(usuario)
                db.session.commit()
                return {"Mensaje": "Usuario agregado con éxito"}
            
        elif request.method == "PUT": # Para actualizar el usuario
            data = request.json
            
            if len(Usuarios.query.where(Usuarios.id != id, Usuarios.email == data.get("email")).all()) > 0:
                return {"Mensaje": "El correo ingresado ya existe. Pruebe con otro distinto..."}
            else:
                usuario = Usuarios.query.get(id)
                usuario.nombre_usuario = data.get("nombre_usuario")
                usuario.email = data.get("email")
                usuario.contrasenia = data.get("contrasenia")
                usuario.rango = data.get("rango")
                db.session.commit()
                return {"Mensaje": "Usuario actualizado con éxito"}
        
        elif request.method == "DELETE": # Para eliminar el usuario
            usuario = db.session.query(Usuarios).filter(Usuarios.id == id).first()
            
            if usuario == None:
                return {"Eliminado": False}
            else:
                equipos = db.session.query(Equipos).filter(Equipos.id_tecnico == id).all()
                
                for equipo in equipos: # En la tabla de usuarios tengo la id -1 que hace referencia al usuario eliminado
                    equipo.id_tecnico = -1
                db.session.commit()
                
                db.session.delete(usuario)
                db.session.commit()
                return {"Eliminado": True}
            
    except Exception as error:
        print(f"\n\nERROR: {error}\n\n")
        return {"Mensaje": "Algo ha fallado..."}


########################################################################################################################
########################################################################################################################


if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=5000, debug=True)