# TPI- OE: Sistemas de turnos
# Alumnos: Brisa Chirino y Gerardo Ocampo
# Módulo: Gestor de persistencia CSV

import csv
import os
from pathlib import Path

DATOS_DIR = "data"
ARCHIVO_TURNOS = os.path.join(DATOS_DIR, "turnos.csv")
ENCODING = "utf-8"

def inicializar_csv():
    """Crea el archivo CSV con encabezados si no existe"""
    Path(DATOS_DIR).mkdir(exist_ok=True)
    
    if not os.path.exists(ARCHIVO_TURNOS):
        try:
            with open(ARCHIVO_TURNOS, "w", newline="", encoding=ENCODING) as f:
                writer = csv.writer(f)
                writer.writerow(["nombre", "fecha", "estado"])
        except IOError as e:
            raise Exception(f"Error al crear archivo: {e}")

def guardar_turno(nombre, fecha, estado="confirmado"):
    """Guarda un turno en el CSV"""
    if not nombre or not fecha:
        raise ValueError("Nombre y fecha no pueden estar vacíos")
    
    try:
        inicializar_csv()
        with open(ARCHIVO_TURNOS, "a", newline="", encoding=ENCODING) as archivo:
            writer = csv.writer(archivo)
            writer.writerow([nombre, fecha, estado])
    except IOError as e:
        raise Exception(f"Error al guardar turno: {e}")

def leer_turnos():
    """Lee todos los turnos del CSV"""
    try:
        inicializar_csv()
        turnos = []
        with open(ARCHIVO_TURNOS, "r", encoding=ENCODING) as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if fila:
                    turnos.append(fila)
        return turnos
    except IOError as e:
        raise Exception(f"Error al leer turnos: {e}")

def obtener_turnos_por_fecha(fecha):
    """Obtiene todos los turnos confirmados de una fecha específica"""
    turnos = leer_turnos()
    return [t for t in turnos if t["fecha"] == fecha and t["estado"] == "confirmado"]
