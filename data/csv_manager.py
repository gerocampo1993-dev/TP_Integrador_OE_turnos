# TPI- OE: Sistemas de turnos
#Alumnos: Brisa Chirino y Gerardo Ocampo


import csv

def guardar_turno(nombre, dia):
    with open("data/turnos.csv", "a", newline="") as archivo:
        writer = csv.writer(archivo)
        writer.writerow([nombre, dia])

def leer_turnos():
    turnos = []
    with open("data/turnos.csv", "r") as archivo:
        reader = csv.reader(archivo)
        for fila in reader:
            turnos.append(fila)
    return turnos
