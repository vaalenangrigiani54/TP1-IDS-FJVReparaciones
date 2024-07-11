/**
 * @brief Función para verificar el inicio de sesión de un usuario/cliente
 * @pre Una cadena de caracteres previamente asignada
 * @returns Diccionario con la clave "SessionID" la cual da la ID del usuario que realmente inició sesión
 * @throws Diccionario con la clave "ERROR" y el mensaje
*/
async function get_loggedID(range) {
    try {
        return (await fetch(`http://127.0.0.1:5000/get_sessionID/${range}`)).json()
    } catch {
        return {"ERROR": "Hubo un problema con el servidor. Vuelva a intentarlo más tarde..."}
    }
}



/**
 * @brief Función para verificar la ID de información/edición de un usuario/equipo/cliente
 * @pre Una cadena de caracteres previamente asignada
 * @returns Diccionario con la clave "InfoID" la cual da la ID del usuario/cliente/equipo que se está mostrando
 * @throws Diccionario con la clave "ERROR" y el mensaje
*/
async function get_infoID(option) {
    try {
        return (await fetch(`http://127.0.0.1:5000/get_infoID/${option}`)).json()
    } catch {
        return {"ERROR": "Hubo un problema con el servidor. Vuelva a intentarlo más tarde..."}
    }
}



/**
 * @brief Función auxiliar para validar el email
 * @pre Una cadena de caracteres previamente declarada y asignada
 * @post Retorna un valor de verdad diciendo si hay un sólo caracter de @ o no
*/
function validate_email(email) {
    caracteres = email.split("")
    cantidad_arrobas = 0

    for (let i = 0; i < caracteres.length; i++) {
        if (caracteres[i] == '@') {
            cantidad_arrobas++
        }
    }

    return cantidad_arrobas == 1
}



/**
 * @brief Función auxiliar para que quede bien la fecha  
 * @pre Un diccionario que tenga como claves ("dia", "mes", "anio", "horas", "minutos") y sus valores sean números enteros.
 * @post Retorna un string con la fecha en la forma DD/MM/YYYY - HH:MM
*/
function format_date(date) {
    return `${two_digits(date["dia"])}/${two_digits(date["mes"])}/${date["anio"]} - ${two_digits(date["horas"])}:${two_digits(date["minutos"])}`
}



/** 
 * @brief Función auxiliar para formatear números a 2 dígitos
 * @pre Un número entero mayor o igual que 0 y menor o igual que 9 (Igual se puede poner cualquier número)
 * @post Retorna, en formato String, el mismo número pero con un 0 a la izquierda
*/
function two_digits(number) {
    if (number >= 0 && number <= 9) {
        return "0" + number
    } else {
        return number
    }
}