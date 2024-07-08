# TP1 - INTRODUCCIÓN AL DESARROLLO DE SOFTWARE
*Integrantes: Facundo Matías Cardogna, Jesús Miguel Fernández, Valentín Angrigiani*<br><br>
---
Nuestro proyecto esta orientado a cualquier empresa destinada a la reparación de dispositivos, la idea de la aplicación es facilitar la gestion de la empresa tanto para gerente como para trabajadores, aparte de esto tambien se tiene en cuenta la interfaz de cliente, la cual tiene una interacción casi directa con cada técnico de la empresa. Este es un software web basado en un registro de dispositivos, clientes y usuarios

---
### ¿Que ofrece nuestro proyecto?
**Para jefes, gerentes o encargados de area esta hecha la interfaz de administrador que permite:**
 - La posibilidad agregar nuevos técnicos u otros administradores
 - Editar la informacion de un técnico o administrador
 - Eliminar a algun técnico o administrador
 - Ver la lista de técnicos y administradores actuales
 - Subir o bajar de rango a algun administrador o técnico

**Para técnicos, empleados y colaboradores esta hecha la interfaz de técnico que permite:**
 - Tener un control de los equipos que tiene cada técnico
 - Ver la información del equipo y el cliente que lo trae
 - Tener una interacción con el cliente mediante las observaciones y el estado del equipo
 - Registrar un nuevo cliente para que este pueda tener acceso a la plataforma y llevar un registro de sus equipos
 - Editar la informacion del cliente
 - Agregar/Editar/Eliminar informacion del equipo que se va transmitiendo al cliente
 - Ver la lista de todos los clientes con distintas clases de ordenamiento
 - Ver todos los equipos que tiene para reparar. Estos se pueden clasificar segun sus estados

**Para clientes esta hecha la interfaz de cliente que permite:**
 - Ver la lista de todos sus equipos registrados en la empresa
 - Ver la informacion completa de cada equipo junto al estado del equipo y las observaciones generadas por el técnico

Ademas de todo eso le dimos importancia a la seguridad del software y por lo tanto para poder entrar en cada pagina tienes que iniciar sesión como tal rol y no se puede acceder a paginas que no esten autorizadas para el usuario en sesión

---
### Si es primera vez que vas a usar nuestro software web tienes que seguir estos pasos: (Si ya has hecho esto puedes saltear a la siguiente sección)
1. Instalar postgresql, crear una base de datos y un usuario con los siguientes comandos:<br>
`sudo apt install postgresql`<br>
`sudo -u postgres createuser --createdb --pwprompt admin` (luego escribe la contraseña: admin)<br>
`sudo -u postgres createdb --owner=user fjvrep` br>

3. Instalar python3 <br>
`sudo apt install python3`

4. Copiar el repositorio en el directorio que desees <br>
`git clone git@github.com:vaalenangrigiani54/TP1-IDS-FJVReparaciones.git` <br>

5. Una vez que estes ubicado en el directorio donde copiaste el repositorio, instalar las dependencias del proyecto  en un entorno virtual<br>
`pip install virtualenv` <br>
`virtualenv venv` <br>
`source venv/bin/activate` <br>
`pip install -r backend/requirements.txt` <br>

6. Abre dos terminales, en la terminal donde tienes activado el virtualenv inicia el app.py en el directorio backend y un servidor http en el directorio frontend <br>
`python3 backend/app.py` (en la terminal donde tienes activado el virtualenv)<br>
`python3 -m http.server` (en la otra terminal donde abriste en el directorio frontend)<br>

7. Una vez levantados los servidores, abrir tu navegador, entrar a la página [http://localhost:8000/main/loginUsuario](http://localhost:8000/main/loginUsuario) e iniciar sesión con el siguiente usuario:<br>
   `Email: admin`<br>
   `Contraseña: admin`<br>
Se debe hacer esto porque el usuario 'admin' es el que va a crear al primer administrador con datos reales. Dirigirse al botón "Agregar un nuevo usuario" y llenar todos los campos con los datos del nuevo usuario.
Una vez hecho eso, el usuario 'admin' se va y se debe volver a iniciar sesión con el nuevo usuario creado.<br>

¡Eso es todo! Ya puedes usar nuestro software web dirigiéndote a [http://localhost:8000/main](http://localhost:8000/main)
---
### Cada vez que vayas a usar nuestro software web tienes que seguir estos pasos:

1. Ir al directorio donde tienes el repositorio del proyecto <br>

2. Iniciar el entorno virtual donde tienes las dependencias del proyecto <br>
  `source venv/bin/activate` <br>

3. Abre dos terminales, en la terminal donde tienes activado el virtualenv inicia el app.py en el directorio backend y un servidor http en el directorio frontend <br>
  `python3 backend/app.py`  (en la terminal donde tienes activado el virtualenv) <br>
  `python3 -m http.server` (en la otra terminal donde abriste en el directorio frontend)<br>

Ya puedes usar nuestro software web abriendo tu navegador y entrando en [http://localhost:8000/main](http://localhost:8000/main)

---
