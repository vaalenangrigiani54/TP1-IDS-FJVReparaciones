# TP1---IDS---CAMEJO
El dia 8/6/2024 se empieza el trabajo.<br>
Nosotros vamos a crear una página web que permita gestionar diferentes equipos que se llevan a arreglar a una empresa. La base de datos nace con un usuario al que se le llama Administrador. Él se encarga de añadir nuevos usuarios (llamados técnicos) capaces de gestionar esos equipos.

TABLAS:
Usuarios: ID | Email | Contraseña | Rango (Administrador/Técnico) | Fecha de ingreso<br>
Clientes: ID | Email | Contraseña | Fecha de ingreso<br>
Equipos: ID | Marca | Modelo | Numero de serie | ID del cliente | ID del técnico | Estado (Nuevo ingreso/En reparación/Reparado/No reparado) | Fecha de ingreso
