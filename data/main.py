# TPI- OE: Sistemas de turnos
#Alumnos: Brisa Chirino y Gerardo Ocampo

from turnos import turno_disponible, registrar_turno

def pedir_turno():
    nombre = input("Ingrese su nombre: ")
    dia = input("Ingrese el día del turno: ")

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
