//Función auxiliar para validar el email
/*
    Pre: Una cadena de caracteres previamente declarada y asignada
    Post: Retorna un valor de verdad diciendo si hay un sólo caracter de @ o no
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



// Función auxiliar para que quede bien la fecha
/*
    Pre: Un diccionario que tenga como claves ("dia", "mes", "anio", "horas", "minutos") y sus valores sean números enteros.
    Post: Retorna un string con la fecha en la forma DD/MM/YYYY - HH:MM
*/
function format_date(date) {
    return `${two_digits(date["dia"])}/${two_digits(date["mes"])}/${date["anio"]} - ${two_digits(date["horas"])}:${two_digits(date["minutos"])}`
}



// Función auxiliar para formatear números a 2 dígitos
/*
    Pre: Un número entero mayor o igual que 0 y menor o igual que 9 (Igual se puede poner cualquier número)
    Post: Retorna, en formato String, el mismo número pero con un 0 a la izquierda
*/
function two_digits(number) {
    if (number >= 0 && number <= 9) {
        return "0" + number
    } else {
        return number
    }
}