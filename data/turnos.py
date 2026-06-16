# TPI- OE: Sistemas de turnos
# Alumnos: Brisa Chirino y Gerardo Ocampo
# Módulo: Lógica de negocio de turnos + Máquina de Estados

from enum import Enum
from csv_manager import guardar_turno, obtener_turnos_por_fecha

MAX_TURNOS_POR_DIA = 5

class EstadoTurno(Enum):
    """Estados posibles en el flujo de solicitud de turno"""
    INICIO = "inicio"
    VALIDANDO_NOMBRE = "validando_nombre"
    VALIDANDO_FECHA = "validando_fecha"
    VERIFICANDO_DISPONIBILIDAD = "verificando_disponibilidad"  # COMPUERTA 1
    REGISTRADO = "registrado"
    ESPERA_REINTENTOS = "espera_reintentos"  # COMPUERTA 2
    CANCELADO = "cancelado"
    ERROR = "error"

def turno_disponible(fecha):
    """
    COMPUERTA 1 (BPMN) + Transición a Estado
    Verifica disponibilidad de turnos
    Retorna: (disponible: bool, estado: EstadoTurno)
    """
    try:
        turnos_dia = obtener_turnos_por_fecha(fecha)
        disponible = len(turnos_dia) < MAX_TURNOS_POR_DIA
        
        if disponible:
            print(f"✓ Hay turnos disponibles para {fecha} ({len(turnos_dia)}/{MAX_TURNOS_POR_DIA})")
            return disponible, EstadoTurno.VERIFICANDO_DISPONIBILIDAD
        else:
            print(f"✗ No hay turnos disponibles para {fecha} ({len(turnos_dia)}/{MAX_TURNOS_POR_DIA})")
            return disponible, EstadoTurno.ESPERA_REINTENTOS
    except Exception as e:
        print(f"Error al verificar disponibilidad: {e}")
        return False, EstadoTurno.ERROR

def registrar_turno(nombre, fecha):
    """
    Transición a estado REGISTRADO
    Registra un turno en la base de datos
    """
    try:
        guardar_turno(nombre, fecha, "confirmado")
        print(f"\n✓ Turno registrado exitosamente")
        print(f"  Nombre: {nombre}")
        print(f"  Fecha: {fecha}\n")
        return True, EstadoTurno.REGISTRADO
    except Exception as e:
        print(f"Error al registrar turno: {e}")
        return False, EstadoTurno.ERROR
