# TP1 - INTRODUCCIÓN AL DESARROLLO DE SOFTWARE
*Integrantes: Facundo Matías Cardogna, Jesús Miguel Fernández, Valentín Angrigiani*<br><br>
**El dia 8/6/2024 se empieza el trabajo.**<br>
Nosotros vamos a crear una página web que permita gestionar diferentes equipos que se llevan a arreglar a la empresa de reparaciones "FJV".<br>
La base de datos nace con un usuario al que se le llama Administrador. Él se encarga de añadir nuevos usuarios (llamados técnicos) capaces de gestionar esos equipos. A su vez, los técnicos van registrando los clientes y los equipos que van arreglando y les da estados: Si recien llegó, si esta en reparación, y si lo pudo reparar o no.<br>
Por otra parte, el cliente, si tiene una cuenta registrada en la página web, puede iniciar sesión y ver los estados de el/los equipo/s que él mandó a arreglar.

TABLAS:<br>
Usuarios: ID | Email | Contraseña | Rango (Administrador/Técnico) | Fecha de ingreso<br>
Clientes: ID | Nombre | Email | Código de ingreso (8 dígitos) | Fecha de inscripción<br>
Equipos: ID | Marca | Modelo | Numero de serie | ID del cliente | ID del técnico | Estado (Nuevo ingreso/En reparación/Reparado/No reparado) | Fecha de ingreso

Para crear la base de datos usamos postgreesql usamos los comandos:<br>
sudo apt install postgresql<br>
sudo -u postgres createuser --createdb --pwprompt usuario<br>
sudo -u postgres createdb --owner=usuario nombre_base_de_datos<br>

Y luego, para acceder a la base de datos con el usuario, usamos el comando:<br>
sudo -u usuario psql nombre_base_de_datos

creamos tablas y las definimos en el archivo database.py 
relacionamos esto con el backend con el archivo app.py

vamos ahora a definir los endpoints que va a tener el backend
