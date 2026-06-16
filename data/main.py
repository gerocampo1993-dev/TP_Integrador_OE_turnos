# TPI- OE: Sistemas de turnos
# Alumnos: Brisa Chirino y Gerardo Ocampo
# Módulo: Interfaz de usuario y flujo BPMN

from turnos import turno_disponible, registrar_turno
from datetime import datetime

# Configuración
MAX_REINTENTOS = 3
FORMATOS_FECHA = ["%d/%m/%Y", "%d-%m-%Y"]

def validar_nombre(nombre):
    """Valida que el nombre no esté vacío"""
    nombre = nombre.strip()
    if len(nombre) < 2:
        print("Error: El nombre debe tener al menos 2 caracteres.")
        return None
    if len(nombre) > 50:
        print("Error: El nombre no puede exceder 50 caracteres.")
        return None
    return nombre

def validar_fecha(fecha_str):
    """Valida formato y que no sea fecha pasada"""
    for formato in FORMATOS_FECHA:
        try:
            fecha_obj = datetime.strptime(fecha_str.strip(), formato)
            if fecha_obj.date() < datetime.now().date():
                print("✗ Error: No puedes pedir un turno para una fecha pasada.")
                return None
            return fecha_str.strip()
        except ValueError:
            continue
    print(f"✗ Error: Formato inválido. Usa {' o '.join(FORMATOS_FECHA)}")
    return None

def obtener_nombre():
    """Entrada: Solicita y valida el nombre del usuario"""
    while True:
        nombre = input("\n📝 Ingrese su nombre: ")
        nombre_validado = validar_nombre(nombre)
        if nombre_validado:
            return nombre_validado
        print("  Intente nuevamente.")

def obtener_fecha():
    """Entrada: Solicita y valida la fecha del turno"""
    while True:
        fecha = input("📅 Ingrese la fecha del turno (DD/MM/YYYY): ")
        fecha_validada = validar_fecha(fecha)
        if fecha_validada:
            return fecha_validada
        print("  Intente nuevamente.")

def flujo_bpmn():
    """
    FLUJO BPMN - Proceso de Solicitud de Turno
    
    Inicio → Obtener Datos → Compuerta 1 (¿Disponible?) → 
      - SÍ: Registrar → Fin exitoso
      - NO: Compuerta 2 (¿Reintentar?) →
        - SÍ: Volver a intentar (max 3)
        - NO: Fin cancelado
    """
    print("\n" + "="*50)
    print("  SISTEMA DE GESTIÓN DE TURNOS")
    print("="*50)
    
    # ENTRADA: Recopilar datos
    nombre = obtener_nombre()
    reintentos = 0
    
    while reintentos < MAX_REINTENTOS:
        fecha = obtener_fecha()
        
        # COMPUERTA 1: ¿Hay disponibilidad?
        if turno_disponible(fecha):
            # PROCESO: Registrar turno
            registrar_turno(nombre, fecha)
            print("✓ Proceso finalizado exitosamente.\n")
            return True
        
        else:
            # COMPUERTA 2: ¿Desea reintentar?
            reintentos += 1
            if reintentos < MAX_REINTENTOS:
                print(f"\n⚠ Ha utilizado {reintentos} de {MAX_REINTENTOS} intentos.")
                respuesta = input("¿Desea intentar con otra fecha? (si/no): ").strip().lower()
                if respuesta != "si":
                    print("\n✗ Proceso cancelado por el usuario.\n")
                    return False
            else:
                print(f"\n✗ Máximo de intentos ({MAX_REINTENTOS}) alcanzado.")
                print("✗ Proceso finalizado sin registrar turno.\n")
                return False
    
    return False

if __name__ == "__main__":
    try:
        flujo_bpmn()
    except KeyboardInterrupt:
        print("\n\n✗ Proceso interrumpido por el usuario.\n")
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}\n")
