# TPI- OE: Sistemas de turnos
# Alumnos: Brisa Chirino y Gerardo Ocampo
# Módulo: Interfaz CLI - Punto de entrada principal

from ui import MenuPrincipal
from services import TurnoService
from models import EstadoTurno
from config import MAX_REINTENTOS

def flujo_solicitar_turno():
    """Flujo BPMN para solicitar turno con máquina de estados"""
    estado_actual = EstadoTurno.INICIO
    
    # VALIDANDO_NOMBRE
    nombre = MenuPrincipal.obtener_nombre()
    estado_actual = EstadoTurno.VALIDANDO_NOMBRE
    
    reintentos = 0
    
    while reintentos < MAX_REINTENTOS:
        # VALIDANDO_FECHA
        fecha = MenuPrincipal.obtener_fecha()
        estado_actual = EstadoTurno.VALIDANDO_FECHA
        
        # COMPUERTA 1: Verificar disponibilidad
        disponible, estado_compuerta, mensaje = TurnoService.verificar_disponibilidad(fecha)
        MenuPrincipal.mostrar_mensaje_info(mensaje)
        
        if disponible:
            # REGISTRADO
            exitoso, estado_registro, mensaje = TurnoService.registrar_turno(nombre, fecha)
            MenuPrincipal.mostrar_mensaje_exito(mensaje)
            MenuPrincipal.pausa()
            return True
        
        else:
            # COMPUERTA 2: Reintentos
            estado_actual = EstadoTurno.ESPERA_REINTENTOS
            reintentos += 1
            
            if reintentos < MAX_REINTENTOS:
                MenuPrincipal.mostrar_mensaje_info(f"Ha utilizado {reintentos} de {MAX_REINTENTOS} intentos.")
                respuesta = input("¿Desea intentar con otra fecha? (si/no): ").strip().lower()
                if respuesta != "si":
                    estado_actual = EstadoTurno.CANCELADO
                    MenuPrincipal.mostrar_mensaje_error("Proceso cancelado por el usuario.")
                    MenuPrincipal.pausa()
                    return False
            else:
                estado_actual = EstadoTurno.CANCELADO
                MenuPrincipal.mostrar_mensaje_error(f"Máximo de intentos ({MAX_REINTENTOS}) alcanzado.")
                MenuPrincipal.pausa()
                return False
    
    return False

def flujo_ver_turnos():
    """Muestra turnos disponibles"""
    fecha = MenuPrincipal.obtener_fecha()
    turnos, error = TurnoService.obtener_resumen_turnos(fecha)
    
    if error:
        MenuPrincipal.mostrar_mensaje_error(f"Error: {error}")
    elif not turnos:
        MenuPrincipal.mostrar_mensaje_info(f"No hay turnos registrados para {fecha}")
    else:
        print(f"\n📋 Turnos registrados para {fecha}:")
        for i, turno in enumerate(turnos, 1):
            print(f"   {i}. {turno['nombre']} - {turno['estado']}")
        print()
    
    MenuPrincipal.pausa()

def menu_principal():
    """Loop principal del menú"""
    MenuPrincipal.mostrar_bienvenida()
    
    # SINCRONIZACIÓN INICIAL: Cargar datos del CSV
    turnos, _ = TurnoService.obtener_todos_turnos()
    estadisticas, _ = TurnoService.obtener_estadisticas()
    MenuPrincipal.mostrar_sincronizacion_inicial(turnos, estadisticas)
    
    while True:
        MenuPrincipal.mostrar_menu_principal()
        opcion = MenuPrincipal.obtener_opcion_menu()
        
        if opcion == "1":
            flujo_solicitar_turno()
        elif opcion == "2":
            flujo_ver_turnos()
        elif opcion == "3":
            MenuPrincipal.mostrar_mensaje_info("Opción en desarrollo")
            MenuPrincipal.pausa()
        elif opcion == "4":
            MenuPrincipal.mostrar_mensaje_info("Opción en desarrollo")
            MenuPrincipal.pausa()
        elif opcion == "5":
            MenuPrincipal.mostrar_ayuda()
            MenuPrincipal.pausa()
        elif opcion == "6":
            # OPCIÓN SALIR CON SINCRONIZACIÓN
            turnos, _ = TurnoService.obtener_todos_turnos()
            estadisticas, _ = TurnoService.obtener_estadisticas()
            MenuPrincipal.mostrar_resumen_antes_salir(turnos, estadisticas)
            
            confirmacion = input("¿Seguro que desea salir? (si/no): ").strip().lower()
            if confirmacion == "si":
                print("\n✓ Todos los cambios han sido guardados en turnos.csv")
                print("👋 ¡Hasta luego!\n")
                break
            else:
                print("\n✓ Retornando al menú...\n")

if __name__ == "__main__":
    try:
        menu_principal()
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}\n")
