# TPI- OE: Sistemas de turnos
# Módulo: Servicios de negocio (lógica de turnos)

from csv_manager import guardar_turno, obtener_turnos_por_fecha, leer_turnos
from models import EstadoTurno, Turno
from config import MAX_TURNOS_POR_DIA

class TurnoService:
    """Servicio para gestionar lógica de turnos"""
    
    @staticmethod
    def verificar_disponibilidad(fecha):
        """
        COMPUERTA 1 (BPMN): Verifica disponibilidad
        Retorna: (disponible: bool, estado: EstadoTurno, mensaje: str)
        """
        try:
            turnos_dia = obtener_turnos_por_fecha(fecha)
            disponible = len(turnos_dia) < MAX_TURNOS_POR_DIA
            
            if disponible:
                mensaje = f"✓ Hay turnos disponibles para {fecha} ({len(turnos_dia)}/{MAX_TURNOS_POR_DIA})"
            else:
                mensaje = f"✗ No hay turnos disponibles para {fecha} ({len(turnos_dia)}/{MAX_TURNOS_POR_DIA})"
            
            return disponible, EstadoTurno.VERIFICANDO_DISPONIBILIDAD, mensaje
        except Exception as e:
            return False, EstadoTurno.ERROR, f"Error: {str(e)}"
    
    @staticmethod
    def registrar_turno(nombre, fecha):
        """
        Transición a estado REGISTRADO
        Retorna: (exitoso: bool, estado: EstadoTurno, mensaje: str)
        """
        try:
            turno = Turno(nombre, fecha, "confirmado")
            guardar_turno(nombre, fecha, "confirmado")
            
            mensaje = f"\n✓ Turno registrado exitosamente\n  Nombre: {nombre}\n  Fecha: {fecha}\n"
            return True, EstadoTurno.REGISTRADO, mensaje
        except Exception as e:
            return False, EstadoTurno.ERROR, f"Error al registrar: {str(e)}"
    
    @staticmethod
    def obtener_resumen_turnos(fecha=None):
        """Obtiene resumen de turnos registrados"""
        try:
            turnos = obtener_turnos_por_fecha(fecha) if fecha else []
            return turnos, None
        except Exception as e:
            return [], str(e)
    
    @staticmethod
    def obtener_todos_turnos():
        """Obtiene TODOS los turnos del CSV (sin filtro de fecha)"""
        try:
            turnos = leer_turnos()
            return turnos, None
        except Exception as e:
            return [], str(e)
    
    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas del CSV"""
        try:
            turnos = leer_turnos()
            confirmados = len([t for t in turnos if t.get("estado") == "confirmado"])
            cancelados = len([t for t in turnos if t.get("estado") == "cancelado"])
            total = len(turnos)
            return {
                "total": total,
                "confirmados": confirmados,
                "cancelados": cancelados
            }, None
        except Exception as e:
            return {}, str(e)
