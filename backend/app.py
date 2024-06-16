from flask import Flask, redirect
from flask_cors import CORS
from database import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://vaalen782:2147483647@localhost:5432/tp1_ids"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

# Estas variables globales van a servir como control para que no se salten la parte de login
USER_SESSION_ID = 0
CLIENT_SESSION_ID = 0


# Cada vez que se reinicia la página hay que reiniciarlas
@app.route("/reset_session")
def home():
    global USER_SESSION_ID, CLIENT_SESSION_ID
    USER_SESSION_ID = 0
    CLIENT_SESSION_ID = 0
    return []


@app.route("/loginUsuario/<email>,<contrasenia>")
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
            
            #Con esto controlo que se ha iniciado sesión correctamente (Si hay un error no pasa por acá)
            global USER_SESSION_ID
            USER_SESSION_ID = datosUsuarios[0]["id"]
            
        return datosUsuarios
    except:
        return [{"Mensaje": "Algo ha fallado..."}]

@app.route("/loginCliente/<email>,<codigo>")
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
            
            #Con esto controlo que se ha iniciado sesión correctamente (Si hay un error no pasa por acá)
            global CLIENT_SESSION_ID
            CLIENT_SESSION_ID = datosClientes[0]["id"]

        return datosClientes
    except:
        return [{"Mensaje": "Algo ha fallado..."}]


@app.route("/administrador/<id>")
def administrador(id):
    data = {"usuarios": [], "equipos": []}
    global USER_SESSION_ID
    
    # Si la ID es distinta a la cual ya se habia iniciado sesión, se debe redirigir a la página main/loginUsuario (en el javascript)
    if int(id) == USER_SESSION_ID:
        usuarios = Usuarios.query.all()
        equipos = Equipos.query.join(Usuarios).add_columns(
            Usuarios.nombre_usuario
        ).join(Clientes).add_column(
            Clientes.nombre_cliente
        ).all()
        
        for usuario in usuarios:
            usuarioData = {
                "id": usuario.id,
                "nombre_usuario": usuario.nombre_usuario,
                "email": usuario.email,
                "rango": usuario.rango,
                "fecha_ingreso": usuario.fecha_ingreso.isoformat()
            }
            data["usuarios"].append(usuarioData)
        
        for (equipo, nombre_usuario, nombre_cliente) in equipos:
            equipoData = {
                "id": equipo.id,
                "tipo_equipo": equipo.tipo_equipo,
                "marca": equipo.marca,
                "modelo": equipo.modelo,
                "num_serie": equipo.num_serie,
                "estado": equipo.estado,
                "observaciones": equipo.observaciones,
                "nombre_cliente": nombre_cliente,
                "nombre_tecnico": nombre_usuario,
                "fecha_ingreso": equipo.fecha_ingreso.isoformat()
            }
            data["equipos"].append(equipoData)
        
    return data


@app.route("/tecnico/<id>")
def tecnico(id):
    data = {"nombre_usuario": "", "equipos": []}
    global USER_SESSION_ID
    
    if int(id) == USER_SESSION_ID:
        usuario = Usuarios.query.where(Usuarios.id == id).first()
        equipos = Equipos.query.where(Equipos.id_tecnico == id).join(Clientes).add_columns(
            Clientes.nombre_cliente
        ).all()

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
                "nombre_cliente": nombre_cliente,
                "fecha_ingreso": equipo.fecha_ingreso
            }
            data["equipos"].append(equipoData)
        
    return data


@app.route("/cliente/<id>")
def cliente(id):
    data = {"nombre_cliente": "", "equipos": []}
    global CLIENT_SESSION_ID
    
    # Si la id es distinta a la cual ya se habia iniciado sesión, se debe redirigir a la página main/loginCliente
    if int(id) == CLIENT_SESSION_ID:
        cliente = Clientes.query.where(Clientes.id == id).first()
        equipos = Equipos.query.where(Equipos.id_cliente == id).join(Usuarios).add_columns(
            Usuarios.nombre_usuario
        ).all()
        
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


if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=5000, debug=True)