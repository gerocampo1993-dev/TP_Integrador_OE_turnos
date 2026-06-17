# TPI- OE: Sistemas de turnos
# Módulo: Interfaz de Usuario (UI/Menu)

from datetime import datetime
from config import FORMATOS_FECHA, MIN_NOMBRE, MAX_NOMBRE

class MenuPrincipal:
    """Interfaz mejorada con menú chatbot"""
    
    @staticmethod
    def mostrar_bienvenida():
        """Muestra pantalla de bienvenida"""
        print("\n" + "="*60)
        print("  🎫 SISTEMA DE GESTIÓN DE TURNOS".center(60))
        print("  Organización Empresarial - TPI".center(60))
        print("="*60 + "\n")
    
    @staticmethod
    def mostrar_menu_principal():
        """Muestra menú principal con opciones"""
        print("\n" + "-"*60)
        print("  MENÚ PRINCIPAL".center(60))
        print("-"*60)
        print("""
  1️⃣  Solicitar un turno
  2️⃣  Ver turnos disponibles
  3️⃣  Ver mis datos
  4️⃣  Cancelar turno
  5️⃣  Ayuda
  6️⃣  Salir
  
  Escriba el número de la opción deseada:
        """)
    
    @staticmethod
    def obtener_opcion_menu():
        """Obtiene y valida la opción del menú"""
        while True:
            opcion = input("➜ Seleccione opción (1-6): ").strip()
            if opcion in ["1", "2", "3", "4", "5", "6"]:
                return opcion
            print("❌ Opción inválida. Intente nuevamente.")
    
    @staticmethod
    def validar_nombre(nombre):
        """Valida entrada de nombre"""
        nombre = nombre.strip()
        if len(nombre) < MIN_NOMBRE:
            print(f"❌ Error: El nombre debe tener al menos {MIN_NOMBRE} caracteres.")
            return None
        if len(nombre) > MAX_NOMBRE:
            print(f"❌ Error: El nombre no puede exceder {MAX_NOMBRE} caracteres.")
            return None
        return nombre
    
    @staticmethod
    def validar_fecha(fecha_str):
        """Valida entrada de fecha"""
        for formato in FORMATOS_FECHA:
            try:
                fecha_obj = datetime.strptime(fecha_str.strip(), formato)
                if fecha_obj.date() < datetime.now().date():
                    print("❌ Error: No puedes pedir un turno para una fecha pasada.")
                    return None
                return fecha_str.strip()
            except ValueError:
                continue
        print(f"❌ Error: Formato inválido. Usa {' o '.join(FORMATOS_FECHA)}")
        return None
    
    @staticmethod
    def obtener_nombre():
        """Loop para obtener nombre válido"""
        while True:
            nombre = input("\n📝 Ingrese su nombre: ").strip()
            nombre_validado = MenuPrincipal.validar_nombre(nombre)
            if nombre_validado:
                return nombre_validado
            print("  Intente nuevamente.")
    
    @staticmethod
    def obtener_fecha():
        """Loop para obtener fecha válida"""
        while True:
            fecha = input("📅 Ingrese la fecha del turno (DD/MM/YYYY): ").strip()
            fecha_validada = MenuPrincipal.validar_fecha(fecha)
            if fecha_validada:
                return fecha_validada
            print("  Intente nuevamente.")
    
    @staticmethod
    def mostrar_mensaje_exito(mensaje):
        """Muestra mensaje de éxito"""
        print(f"\n✅ {mensaje}\n")
    
    @staticmethod
    def mostrar_mensaje_error(mensaje):
        """Muestra mensaje de error"""
        print(f"\n❌ {mensaje}\n")
    
    @staticmethod
    def mostrar_mensaje_info(mensaje):
        """Muestra mensaje informativo"""
        print(f"\nℹ️  {mensaje}\n")
    
    @staticmethod
    def mostrar_ayuda():
        """Muestra pantalla de ayuda"""
        print("\n" + "="*60)
        print("  AYUDA DEL SISTEMA".center(60))
        print("="*60)
        print("""
  ¿CÓMO FUNCIONA?
  
  1. SOLICITAR TURNO
     - Ingrese su nombre
     - Ingrese la fecha deseada (DD/MM/YYYY)
     - El sistema verifica disponibilidad
     - Si hay espacio, su turno se registra
     - Puede reintentar hasta 3 veces
  
  2. FORMATOS ACEPTADOS
     - Fechas: DD/MM/YYYY o DD-MM-YYYY
     - Ejemplo: 20/06/2026 o 20-06-2026
  
  3. LÍMITES DEL SISTEMA
     - Máximo 5 turnos por día
     - Máximo 3 intentos de reintentos
     - Nombre: 2-50 caracteres
  
  4. CONTACTO
     - Para más información, consulte con administración
        """)
        print("="*60 + "\n")
    
    @staticmethod
    def pausa():
        """Pausa para que el usuario vea el mensaje"""
        input("\nPresione ENTER para continuar...")
