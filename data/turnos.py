# TPI- OE: Sistemas de turnos
# Alumnos: Brisa Chirino y Gerardo Ocampo
# Módulo: Lógica de negocio de turnos

from csv_manager import guardar_turno, obtener_turnos_por_fecha

MAX_TURNOS_POR_DIA = 5

def turno_disponible(fecha):
    """
    COMPUERTA 1 (BPMN): Verifica disponibilidad de turnos
    Retorna: True si hay espacio, False si está lleno
    """
    try:
        turnos_dia = obtener_turnos_por_fecha(fecha)
        disponible = len(turnos_dia) < MAX_TURNOS_POR_DIA
        
        if disponible:
            print(f"✓ Hay turnos disponibles para {fecha} ({len(turnos_dia)}/{MAX_TURNOS_POR_DIA})")
        else:
            print(f"✗ No hay turnos disponibles para {fecha} ({len(turnos_dia)}/{MAX_TURNOS_POR_DIA})")
        
        return disponible
    except Exception as e:
        print(f"Error al verificar disponibilidad: {e}")
        return False

def registrar_turno(nombre, fecha):
    """Registra un turno en la base de datos"""
    try:
        guardar_turno(nombre, fecha, "confirmado")
        print(f"\n✓ Turno registrado exitosamente")
        print(f"  Nombre: {nombre}")
        print(f"  Fecha: {fecha}\n")
        return True
    except Exception as e:
        print(f"Error al registrar turno: {e}")
        return False
