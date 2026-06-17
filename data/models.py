# TPI- OE: Sistemas de turnos
# Módulo: Modelos de datos

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class EstadoTurno(Enum):
    """Estados posibles en el flujo de solicitud de turno"""
    INICIO = "inicio"
    VALIDANDO_NOMBRE = "validando_nombre"
    VALIDANDO_FECHA = "validando_fecha"
    VERIFICANDO_DISPONIBILIDAD = "verificando_disponibilidad"
    REGISTRADO = "registrado"
    ESPERA_REINTENTOS = "espera_reintentos"
    CANCELADO = "cancelado"
    ERROR = "error"

@dataclass
class Turno:
    """Modelo de datos para un turno"""
    nombre: str
    fecha: str
    estado: str = "confirmado"
    
    def __str__(self):
        return f"{self.nombre} - {self.fecha} ({self.estado})"
    
    def to_csv_row(self):
        """Convierte el turno a formato CSV"""
        return [self.nombre, self.fecha, self.estado]
    
    @staticmethod
    def from_csv_row(row):
        """Crea un turno desde una fila CSV"""
        if isinstance(row, dict):
            return Turno(row["nombre"], row["fecha"], row["estado"])
        return Turno(row[0], row[1], row[2] if len(row) > 2 else "confirmado")

@dataclass
class SolicitudTurno:
    """Modelo para una solicitud de turno en progreso"""
    nombre: str
    fecha: str
    estado: EstadoTurno
    reintentos: int = 0
    
    def incrementar_reintentos(self):
        self.reintentos += 1
        return self.reintentos
