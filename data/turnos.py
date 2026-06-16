# TPI- OE: Sistemas de turnos
#Alumnos: Brisa Chirino y Gerardo Ocampo


from csv_manager import guardar_turno, leer_turnos

def turno_disponible(dia):
    turnos = leer_turnos()
    # Máximo 5 turnos por día (ejemplo simple)
    cantidad = sum(1 for t in turnos if t[1] == dia)
    return cantidad < 5

def registrar_turno(nombre, dia):
    guardar_turno(nombre, dia)
    print(f"Turno registrado para {nombre} el día {dia}")
