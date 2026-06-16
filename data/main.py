# TPI- OE: Sistemas de turnos
#Alumnos: Brisa Chirino y Gerardo Ocampo

from turnos import turno_disponible, registrar_turno
from datetime import datetime

def validar_fecha(fecha_str):
    """Valida que la fecha tenga formato correcto (DD/MM/YYYY o DD-MM-YYYY)"""
    formatos = ["%d/%m/%Y", "%d-%m-%Y"]
    for formato in formatos:
        try:
            fecha_obj = datetime.strptime(fecha_str, formato)
            # Verificar que no sea una fecha pasada
            if fecha_obj.date() < datetime.now().date():
                print("Error: No puedes pedir un turno para una fecha pasada.")
                return False
            return True
        except ValueError:
            continue
    print("Error: Formato de fecha inválido. Usa DD/MM/YYYY o DD-MM-YYYY")
    return False

def pedir_turno():
    nombre = input("Ingrese su nombre: ")
    
    # Validar fecha
    while True:
        dia = input("Ingrese el día del turno (DD/MM/YYYY): ")
        if validar_fecha(dia):
            break

    # Compuerta 1
    if turno_disponible(dia):
        registrar_turno(nombre, dia)
    else:
        print("No hay turnos disponibles ese día.")
        # Compuerta 2
        otro = input("¿Desea otro día? (si/no): ")
        if otro.lower() == "si":
            pedir_turno()
        else:
            print("Proceso finalizado sin turno.")

if __name__ == "__main__":
    pedir_turno()
