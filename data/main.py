# TPI- OE: Sistemas de turnos
# Alumnos: Brisa Chirino y Gerardo Ocampo
# Módulo: Interfaz de usuario, Flujo BPMN + Máquina de Estados

from turnos import turno_disponible, registrar_turno, EstadoTurno
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
            return nombre_validado, EstadoTurno.VALIDANDO_NOMBRE
        print("  Intente nuevamente.")

def obtener_fecha():
    """Entrada: Solicita y valida la fecha del turno"""
    while True:
        fecha = input("📅 Ingrese la fecha del turno (DD/MM/YYYY): ")
        fecha_validada = validar_fecha(fecha)
        if fecha_validada:
            return fecha_validada, EstadoTurno.VALIDANDO_FECHA
        print("  Intente nuevamente.")

def mostrar_transicion(estado_anterior, estado_nuevo):
    """Muestra la transición entre estados (opcional, para debugging)"""
    pass  # Descomentar si quieres ver las transiciones en consola
    # print(f"  [Estado: {estado_anterior.value} → {estado_nuevo.value}]")

def flujo_bpmn():
    """
    FLUJO BPMN CON MÁQUINA DE ESTADOS
    
    Diagrama:
    INICIO → VALIDANDO_NOMBRE → VALIDANDO_FECHA → VERIFICANDO_DISPONIBILIDAD
             (Compuerta 1: ¿Disponible?)
             ├─ SÍ → REGISTRADO → FIN ✓
             └─ NO → ESPERA_REINTENTOS (Compuerta 2: ¿Reintentar?)
                    ├─ SÍ (< 3) → volver a VALIDANDO_FECHA
                    └─ NO o MAX → CANCELADO → FIN ✗
    """
    print("\n" + "="*50)
    print("  SISTEMA DE GESTIÓN DE TURNOS")
    print("="*50)
    
    # Estado inicial
    estado_actual = EstadoTurno.INICIO
    
    # ENTRADA: Recopilar nombre
    nombre, estado_actual = obtener_nombre()
    mostrar_transicion(EstadoTurno.INICIO, estado_actual)
    
    reintentos = 0
    
    while reintentos < MAX_REINTENTOS:
        # VALIDAR FECHA
        fecha, estado_actual = obtener_fecha()
        mostrar_transicion(EstadoTurno.VALIDANDO_NOMBRE, estado_actual)
        
        # COMPUERTA 1: ¿Disponibilidad?
        disponible, estado_compuerta1 = turno_disponible(fecha)
        mostrar_transicion(estado_actual, estado_compuerta1)
        
        if disponible:
            # SÍ: Registrar turno → REGISTRADO
            exitoso, estado_registro = registrar_turno(nombre, fecha)
            mostrar_transicion(estado_compuerta1, estado_registro)
            print("✓ Proceso finalizado exitosamente.\n")
            return True
        
        else:
            # NO: Compuerta 2 → ESPERA_REINTENTOS
            estado_actual = EstadoTurno.ESPERA_REINTENTOS
            mostrar_transicion(estado_compuerta1, estado_actual)
            
            reintentos += 1
            if reintentos < MAX_REINTENTOS:
                print(f"\n⚠ Ha utilizado {reintentos} de {MAX_REINTENTOS} intentos.")
                respuesta = input("¿Desea intentar con otra fecha? (si/no): ").strip().lower()
                if respuesta != "si":
                    estado_actual = EstadoTurno.CANCELADO
                    print("\n✗ Proceso cancelado por el usuario.\n")
                    return False
                # Volver a VALIDANDO_FECHA
                estado_actual = EstadoTurno.VALIDANDO_FECHA
            else:
                estado_actual = EstadoTurno.CANCELADO
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
