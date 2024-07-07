from flask import Flask, request
from flask_cors import CORS
from sqlalchemy import desc
from database import *
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://admin:admin@localhost:5432/fjvrep"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)


#======================================================================================================================================================#


# Estas variables globales van a servir como control para que no se salteen la parte de login
ADMIN_SESSION_ID = 0
TECH_SESSION_ID = 0
CLIENT_SESSION_ID = 0

# Estas variable global sirve como control para no cambiar manualmente los query params de la id de información del usuario/cliente/equipo
USER_INFO_ID = 0
CLIENT_INFO_ID = 0
DEVICE_INFO_ID = 0




# Endpoint auxiliar para resetear las variables globales cuando se cierra sesión
@app.route("/reset_session")
def reset_session():
    global ADMIN_SESSION_ID, TECH_SESSION_ID, CLIENT_SESSION_ID, USER_INFO_ID, CLIENT_INFO_ID, DEVICE_INFO_ID
    ADMIN_SESSION_ID = 0
    TECH_SESSION_ID = 0
    CLIENT_SESSION_ID = 0
    USER_INFO_ID = 0
    CLIENT_INFO_ID = 0
    DEVICE_INFO_ID = 0
    return {"Mensaje": "SESSION RESET"}



# Endpoint auxiliar para verificar si el usuario inició sesión o no
# Se debe hacer fetch() al mismo en todas las páginas
@app.route("/verify_session/<id>/<rango>")
def verify_session(id, rango):
    global ADMIN_SESSION_ID, TECH_SESSION_ID, CLIENT_SESSION_ID
    response = {"Logged": False}
    
    try: # Hago esto porque si se pone texto manualmente en el query-param, debe pasar y hacer como que no inició sesión (que es lo lógico)
        if int(id) > 0:
            if rango == "administrador":
                if int(id) == ADMIN_SESSION_ID:
                    response["Logged"] = True
            elif rango == "tecnico":
                if int(id) == TECH_SESSION_ID:
                    response["Logged"] = True
            elif rango == "cliente":
                if int(id) == CLIENT_SESSION_ID:
                    response["Logged"] = True
    except: # La funcion int() no pudo convertir a entero una cadena de caracteres pasada en id
        pass
    
    return response



# Endpoint auxiliar para verificar que no se cambien los query params de la id de información de un usuario/cliente/equipo
# Se debe hacer fetch() al mismo en todas las páginas que muestren información
@app.route("/verify_InfoID/<id>/<opcion>")
def verify_InfoID(id, opcion):
    global USER_INFO_ID, CLIENT_INFO_ID, DEVICE_INFO_ID
    response = {"ChangedParameter": True, "UserInfoID": USER_INFO_ID, "ClientInfoID": CLIENT_INFO_ID, "DeviceInfoID": DEVICE_INFO_ID}
    
    try: # Acá es lo mismo que en el endpoint anterior. Se debe evitar que se escriba texto
        if opcion == "usuario":
            if int(id) == USER_INFO_ID and int(id) > 0:
                response["ChangedParameter"] = False
        elif opcion == "cliente":
            if int(id) == CLIENT_INFO_ID and int(id) > 0:
                response["ChangedParameter"] = False
        elif opcion == "equipo":
            if int(id) == DEVICE_INFO_ID and int(id) > 0:
                response["ChangedParameter"] = False
    except:
        pass
    
    return response



# Por otra parte se necesita un endpoint auxiliar más para setear esa variable global que hace la verificación en el endpoint anterior
# Este endpoint se invoca desde las páginas que pueden dirigir a las de información/editar del usuario/cliente/equipo
@app.route("/set_InfoID/<int:id>/<opcion>")
def set_InfoID(id, opcion):
    global USER_INFO_ID, CLIENT_INFO_ID, DEVICE_INFO_ID
    
    if opcion == "usuario":
        USER_INFO_ID = id
    elif opcion == "cliente":
        CLIENT_INFO_ID = id
    elif opcion == "equipo":
        DEVICE_INFO_ID = id
    
    return {"Mensaje": "INFO ID SET"}


#======================================================================================================================================================#


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





# Hace referencia a la página del administrador.
# Se obtienen todos los usuarios.
@app.route("/administrador/<int:id>")
def administrador(id):
    global USER_INFO_ID
    USER_INFO_ID = 0
    
    try:
        data = {"session_username": "", "usuarios": ["Acá va primero mi usuario"]} # Reservo la primera posición en la lista para el usuario de la sesión
        usuarios = Usuarios.query.where(Usuarios.id != -1).order_by(Usuarios.id).all()
        
        for usuario in usuarios:
            fechaAux = usuario.fecha_ingreso
            fecha = {"dia": fechaAux.day, "mes": fechaAux.month, "anio": fechaAux.year, "horas": fechaAux.hour, "minutos": fechaAux.minute}
            
            usuarioData = {
                "id": usuario.id,
                "nombre_usuario": usuario.nombre_usuario,
                "email": usuario.email,
                "rango": usuario.rango,
                "fecha_ingreso": fecha
            }
            
            if usuario.id == id:
                data["session_username"] = usuario.nombre_usuario
                data["usuarios"][0] = usuarioData # Aquí es donde lo inserto en la primera posición
            else:
                data["usuarios"].append(usuarioData)
            
        return data
    except Exception as error:
        print(f"\n\nERROR: {error}\n\n")
        return {"Mensaje": "Algo ha fallado..."}



# Endpoint que hace referencia a la página del usuario técnico.
# Se obtienen todos los equipos que administra cierto técnico.
@app.route("/tecnico/<id>/<statusFilter>")
def tecnico(id, statusFilter):
    global CLIENT_INFO_ID, DEVICE_INFO_ID
    CLIENT_INFO_ID = 0
    DEVICE_INFO_ID = 0
    
    try:
        data = {"session_username": "", "equipos": []}
    
        usuario = Usuarios.query.where(Usuarios.id == id).first()
        if statusFilter == "all":
            equipos = Equipos.query.where(Equipos.id_tecnico == id).join(Clientes).add_columns(
                Clientes.nombre_cliente
            ).order_by(desc(Equipos.fecha_ingreso)).all()
        elif statusFilter == "En revisión":
            equipos = Equipos.query.where(Equipos.id_tecnico == id, Equipos.estado == "En revisión/reparación").join(Clientes).add_columns(
                Clientes.nombre_cliente
            ).order_by(desc(Equipos.fecha_ingreso)).all()
        else:
            equipos = Equipos.query.where(Equipos.id_tecnico == id, Equipos.estado == statusFilter).join(Clientes).add_columns(
                Clientes.nombre_cliente
            ).order_by(desc(Equipos.fecha_ingreso)).all()

        data["session_username"] = usuario.nombre_usuario
        
        for (equipo, nombre_cliente) in equipos:
            fechaAux = equipo.fecha_ingreso
            fecha = {"dia": fechaAux.day, "mes": fechaAux.month, "anio": fechaAux.year, "horas": fechaAux.hour, "minutos": fechaAux.minute}
            
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
                "fecha_ingreso": fecha
            }
            data["equipos"].append(equipoData)
          
        return data
    except Exception as error:
        print(f"\n\nERROR: {error}\n\n")
        return {"Mensaje": "Algo ha fallado..."}



# Endpoint que hace referencia a la página del cliente.
# Se obtienen todos los equipos que cierto cliente llevó a arreglar.
@app.route("/cliente/<id>/<statusFilter>")
def cliente(id, statusFilter):
    global DEVICE_INFO_ID
    DEVICE_INFO_ID = 0
    
    try:
        data = {"session_clientname": "", "equipos": []}

        cliente = Clientes.query.where(Clientes.id == id).first()
        if statusFilter == "all":
            equipos = Equipos.query.where(Equipos.id_cliente == id).join(Usuarios).add_columns(
                Usuarios.nombre_usuario
            ).order_by(desc(Equipos.fecha_ingreso)).all()
        elif statusFilter == "En revisión":
            equipos = Equipos.query.where(Equipos.id_cliente == id, Equipos.estado == "En revisión/reparación").join(Usuarios).add_columns(
                Usuarios.nombre_usuario
            ).order_by(desc(Equipos.fecha_ingreso)).all()
        else:
            equipos = Equipos.query.where(Equipos.id_cliente == id, Equipos.estado == statusFilter).join(Usuarios).add_columns(
                Usuarios.nombre_usuario
            ).order_by(desc(Equipos.fecha_ingreso)).all()
        
        data["session_clientname"] = cliente.nombre_cliente
        
        for (equipo, nombre_tecnico) in equipos:
            fechaAux = equipo.fecha_ingreso
            fecha = {"dia": fechaAux.day, "mes": fechaAux.month, "anio": fechaAux.year, "horas": fechaAux.hour, "minutos": fechaAux.minute}
            
            equipoData = {
                "id": equipo.id,
                "tipo_equipo": equipo.tipo_equipo,
                "marca": equipo.marca,
                "modelo": equipo.modelo,
                "num_serie": equipo.num_serie,
                "estado": equipo.estado,
                "observaciones": equipo.observaciones,
                "nombre_tecnico": nombre_tecnico,
                "fecha_ingreso": fecha
            }
            data["equipos"].append(equipoData)

        return data
    except Exception as error:
        print(f"\n\nERROR: {error}\n\n")
        return {"Mensaje": "Algo ha fallado..."}



# Endpoint que hace referencia a la página que muestra la lista de todos los clientes
@app.route("/listaClientes/<ordenamiento>", methods=["GET"])
def listaClientes(ordenamiento):
    data = []
    
    try: # Estos strings son estáticos pero sirven como referencia
        if ordenamiento == "nombre A-Z":
            clientesQuery = Clientes.query.order_by(Clientes.nombre_cliente)
        elif ordenamiento == "nombre Z-A":
            clientesQuery = Clientes.query.order_by(desc(Clientes.nombre_cliente))
        elif ordenamiento == "fecha antiguos":
            clientesQuery = Clientes.query.order_by(Clientes.fecha_inscripcion)
        elif ordenamiento == "fecha recientes":
            clientesQuery = Clientes.query.order_by(desc(Clientes.fecha_inscripcion))
        
        for cliente in clientesQuery:
            fechaAux = cliente.fecha_inscripcion
            fecha = {"dia": fechaAux.day, "mes": fechaAux.month, "anio": fechaAux.year, "horas": fechaAux.hour, "minutos": fechaAux.minute}

            clienteData = {
                "id": cliente.id,
                "nombre_cliente": cliente.nombre_cliente,
                "email": cliente.email,
                "codigo_ingreso": cliente.codigo_ingreso,
                "fecha_inscripcion": fecha
            }
            data.append(clienteData)
        
        return data
    except Exception as error:
        print(f"\n\nERROR: {error}\n\n")
        return {"Mensaje": "Algo ha fallado..."}





# Los siguientes endpoints, a diferencia de los otros, obtienen informaciones de UN SOLO USUARIO, no de todos


# Endpoint para consultar/agregar/modificar/eliminar a un usuario de la empresa
@app.route("/acciones_usuario/<id>", methods=["GET", "POST", "PUT", "DELETE"])
def acciones_usuario(id):
    try:
        if request.method == "GET": # Para ver la información del usuario
            usuario = Usuarios.query.get(id)
            
            fechaAux = usuario.fecha_ingreso
            fecha = {"dia": fechaAux.day, "mes": fechaAux.month, "anio": fechaAux.year, "horas": fechaAux.hour, "minutos": fechaAux.minute}
            
            return {
                "id": usuario.id,
                "nombre_usuario": usuario.nombre_usuario,
                "email": usuario.email,
                "contrasenia": usuario.contrasenia,
                "rango": usuario.rango,
                "fecha_ingreso": fecha
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



# Endpoint para consultar/agregar/modificar a un cliente
@app.route("/acciones_cliente/<id>", methods=["GET", "POST", "PUT", "DELETE"])
def acciones_cliente(id):
    try:
        if request.method == "GET": # Para ver la información del cliente
            cliente = Clientes.query.get(id)
            
            fechaAux = cliente.fecha_inscripcion
            fecha = {"dia": fechaAux.day, "mes": fechaAux.month, "anio": fechaAux.year, "horas": fechaAux.hour, "minutos": fechaAux.minute}
            
            return {
                "id": cliente.id,
                "nombre_cliente": cliente.nombre_cliente,
                "email": cliente.email,
                "codigo_ingreso": cliente.codigo_ingreso,
                "fecha_inscripcion": fecha
            }
        
        elif request.method == "POST": # Para agregar un nuevo cliente (En este caso no se usa la id del parámetro)
            data = request.json
            nuevo_nombre = data.get("nombre_cliente")
            nuevo_email = data.get("email")
            nuevo_codigoIngreso = random.randrange(10000000, 99999999)
            
            if len(Clientes.query.where(Clientes.email == nuevo_email).all()) > 0:
                return {"Mensaje": "El correo ingresado ya existe. Pruebe con otro distinto..."}
            else:
                # Si de pura casualidad se genera un número aleatorio que ya existe en la base de datos, se cambia. (Esto igual se vuelve muy lento cuando hay decenas de millones de inscriptos)
                # Para ello primero necesito obtener todos los códigos
                clienteQuery = Clientes.query.all()
                codigos = [cliente.codigo_ingreso for cliente in clienteQuery]
                if len(codigos) >= 50000000: # Doy un poco de margen para que no sea tan lento. No pueden haber más de 50 millones de clientes
                    return {"Mensaje": "FATAL", "MensajeCodigo": f"Base de datos colapsada"}
                elif len(codigos) > 0:
                    while nuevo_codigoIngreso in codigos:
                        nuevo_codigoIngreso = random.randrange(10000000, 99999999)
                
                cliente = Clientes(
                    nombre_cliente = nuevo_nombre,
                    email = nuevo_email,
                    codigo_ingreso = nuevo_codigoIngreso
                )
                db.session.add(cliente)
                db.session.commit()
                
                return {"Mensaje": "SUCCESS", "MensajeCodigo": f"Cliente agregado con éxito. Su código de ingreso es {nuevo_codigoIngreso}"}
        
        elif request.method == "PUT":
            data = request.json
            
            cliente = Clientes.query.get(id)
            cliente.nombre_cliente = data.get("nombre_cliente")
            cliente.email = data.get("email")
            db.session.commit()
            
            return {"Mensaje": "Cliente actualizado con éxito"}
        
        elif request.method == "DELETE":
            cliente = db.session.query(Clientes).filter(Clientes.id == id).first()
            
            if cliente == None:
                return {"Eliminado": False}
            else: # Si se elimina un cliente, también se deben eliminar todos los equipos con la id de ese cliente
                equipos = db.session.query(Equipos).filter(Equipos.id_cliente == id).all()
                
                for equipo in equipos:
                    db.session.delete(equipo)
                db.session.commit()
                
                db.session.delete(cliente)
                db.session.commit()
                return {"Eliminado": True}
        
    except Exception as error:
        print(f"\n\nERROR: {error}\n\n")
        return {"Mensaje": "Algo ha fallado..."}



# Endpoint para consultar/agregar/modificar a un equipo
@app.route("/acciones_equipo/<id>", methods=["GET", "POST", "PUT"])
def acciones_equipo(id):
    try:
        if request.method == "GET": # Para ver la información del equipo
            equipoQuery = Equipos.query.where(Equipos.id == id).join(Clientes).add_columns(
                Clientes.nombre_cliente,
                Clientes.email
            ).join(Usuarios).add_column(
                Usuarios.nombre_usuario
            ).first()
            
            # EquipoQuery es una tupla de 4 elementos, debido a la relación con las otras dos tablas
            equipo = equipoQuery[0]
            nombre_cliente = equipoQuery[1]
            email_cliente = equipoQuery[2]
            nombre_usuario = equipoQuery[3]
            
            fechaAux = equipo.fecha_ingreso
            fecha = {"dia": fechaAux.day, "mes": fechaAux.month, "anio": fechaAux.year, "horas": fechaAux.hour, "minutos": fechaAux.minute}
            
            return {
                "id": equipo.id,
                "tipo_equipo": equipo.tipo_equipo,
                "marca": equipo.marca,
                "modelo": equipo.modelo,
                "num_serie": equipo.num_serie,
                "estado": equipo.estado,
                "observaciones": equipo.observaciones,
                "nombre_cliente": nombre_cliente,
                "email_cliente": email_cliente,
                "nombre_tecnico": nombre_usuario,
                "fecha_ingreso": fecha
            }
            
        elif request.method == "POST": # Para agregar un nuevo equipo (En este caso no se usa la id del parámetro)
            data = request.json
            
            nuevo_email_cliente = data.get("email_cliente")
            nuevo_tipo_equipo = data.get("tipo_equipo")
            nueva_marca = data.get("marca")
            nuevo_modelo = data.get("modelo")
            nuevo_num_serie = data.get("num_serie")
            id_tecnico = data.get("id_tecnico")

            if len(Clientes.query.where(Clientes.email == nuevo_email_cliente).all()) == 0:
                return {"Mensaje": "El email del cliente ingresado no existe..."}
            else:
                id_cliente = Clientes.query.where(Clientes.email == nuevo_email_cliente).first().id
                
                equipo = Equipos(
                    tipo_equipo = nuevo_tipo_equipo,
                    marca = nueva_marca,
                    modelo = nuevo_modelo,
                    num_serie = nuevo_num_serie,
                    estado = "Nuevo Ingreso",
                    observaciones = "-",
                    id_cliente = id_cliente,
                    id_tecnico = id_tecnico,
                )
                db.session.add(equipo)
                db.session.commit()
                
                return {"Mensaje": "Equipo agregado con éxito"}
            
        elif request.method == "PUT":
            data = request.json
            
            email_cliente = data.get("email_cliente")
            tipo_equipo = data.get("tipo_equipo")
            marca = data.get("marca")
            modelo = data.get("modelo")
            num_serie = data.get("num_serie")
            estado = data.get("estado")
            observaciones = data.get("observaciones")
            
            if len(Clientes.query.where(Clientes.email == email_cliente).all()) == 0:
                return {"Mensaje": "El email del cliente ingresado no existe..."}
            elif estado == "Nuevo Ingreso" and observaciones != "-":
                return {"Mensaje": "No puedes agregar observaciones si el equipo está en nuevo ingreso..."}
            else:
                id_cliente = Clientes.query.where(Clientes.email == email_cliente).first().id
                equipo = Equipos.query.where(Equipos.id == id).first()
                equipo.tipo_equipo = tipo_equipo
                equipo.marca = marca
                equipo.modelo = modelo
                equipo.num_serie = num_serie
                equipo.estado = estado
                equipo.observaciones = observaciones
                equipo.id_cliente = id_cliente
                db.session.commit()
                return {"Mensaje": "Equipo actualizado con éxito"}

    except Exception as error:
        print(f"\n\nERROR: {error}\n\n")
        return {"Mensaje": "Algo ha fallado..."}


#======================================================================================================================================================#


# Arranque del backend y la base de datos
if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=5000, debug=True)