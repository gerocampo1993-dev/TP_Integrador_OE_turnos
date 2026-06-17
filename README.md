# TP_Integrador_OE_turnos

Sistema de gestión de turnos con arquitectura modular, 2 compuertas BPMN y máquina de estados. Escalable a Telegram/WhatsApp.

**Alumnos**: Brisa Chirino y Gerardo Ocampo

---

## 📁 Estructura Modular (Arquitectura MVC)

```
data/
├── config.py              # Configuración centralizada (constantes)
├── models.py              # Modelos de datos (EstadoTurno, Turno)
├── services.py            # Lógica de negocio (TurnoService)
├── csv_manager.py         # Persistencia (gestión de CSV)
├── ui.py                  # Interfaz de usuario (MenuPrincipal)
├── main.py                # Punto de entrada CLI
├── bot_telegram.py        # Template para bot Telegram (futuro)
├── turnos.py              # Compatibilidad (legacy)
└── turnos.csv             # Base de datos (auto-generado)
```

### Responsabilidades

| Módulo | Responsabilidad |
|--------|-----------------|
| **config.py** | Constantes y configuración centralizada |
| **models.py** | Clases de datos (dataclasses + Enums) |
| **services.py** | Lógica de negocio (verificación, registro) |
| **csv_manager.py** | Persistencia en archivos |
| **ui.py** | Interfaz con usuario (menú, inputs, outputs) |
| **main.py** | Orquestación del flujo y punto de entrada |
| **bot_telegram.py** | Adaptador para Telegram (template) |

---

## 🎮 Menú Principal Mejorado

```
==============================================================
         🎫 SISTEMA DE GESTIÓN DE TURNOS
      Organización Empresarial - TPI
==============================================================

  MENÚ PRINCIPAL
  
  1️⃣  Solicitar un turno
  2️⃣  Ver turnos disponibles
  3️⃣  Ver mis datos
  4️⃣  Cancelar turno
  5️⃣  Ayuda
  6️⃣  Salir
```

**Características del menú:**
- ✅ Interfaz chatbot-like intuitiva
- ✅ Emojis para mejor UX
- ✅ Validación de opciones
- ✅ Loop principal robusto
- ✅ Manejo de excepciones

---

## 🔄 Flujo BPMN + Máquina de Estados

### Diagrama Completo

```
     INICIO
        ↓
 VALIDANDO_NOMBRE (usuario ingresa nombre)
        ↓
 VALIDANDO_FECHA (usuario ingresa fecha)
        ↓
 VERIFICANDO_DISPONIBILIDAD ← COMPUERTA 1
        ↙              ↘
    SÍ (disponible)   NO (lleno)
      ↓                   ↓
 REGISTRADO         ESPERA_REINTENTOS ← COMPUERTA 2
      ↓                   ↙         ↘
   FIN ✓         SÍ (< 3)      NO o MAX
                    ↓               ↓
              (volver a FECHA)  CANCELADO
                                   ↓
                                 FIN ✗
```

### Máquina de Estados

```python
class EstadoTurno(Enum):
    INICIO
    VALIDANDO_NOMBRE
    VALIDANDO_FECHA
    VERIFICANDO_DISPONIBILIDAD  # COMPUERTA 1
    REGISTRADO
    ESPERA_REINTENTOS           # COMPUERTA 2
    CANCELADO
    ERROR
```

**Las transiciones son explícitas y trackeables.**

---

## 🚀 Cómo Usar - CLI

```bash
cd data
python main.py
```

**Ejemplo de sesión:**
```
==============================================================
         🎫 SISTEMA DE GESTIÓN DE TURNOS
==============================================================

  1️⃣  Solicitar un turno
  2️⃣  Ver turnos disponibles
  ...

➜ Seleccione opción (1-6): 1

📝 Ingrese su nombre: Juan Pérez
📅 Ingrese la fecha del turno (DD/MM/YYYY): 20/06/2026
ℹ️  ✓ Hay turnos disponibles para 20/06/2026 (2/5)

✅ ✓ Turno registrado exitosamente
  Nombre: Juan Pérez
  Fecha: 20/06/2026
```

---

## 📱 Escalabilidad: Telegram / WhatsApp

### ✅ Es Escalable

El diseño modular permite integración con bots de forma **100% escalable**:

#### Arquitectura de Integración

```
┌─────────────────┐
│  Usuario (Chat) │
└────────┬────────┘
         │
    ┌────▼─────────────────────┐
    │  Telegram/WhatsApp API   │
    │  (python-telegram-bot)   │
    └────┬─────────────────────┘
         │
    ┌────▼──────────────────────────┐
    │ bot_telegram.py / bot_whatsapp│
    │ (Adaptador de entrada)        │
    └────┬──────────────────────────┘
         │
    ┌────▼──────────────────────────┐
    │  services.py                 │ ← Lógica sin cambios
    │  (TurnoService)              │
    └────┬──────────────────────────┘
         │
    ┌────▼──────────────────────────┐
    │  csv_manager.py              │ ← BD sin cambios
    └──────────────────────────────┘
```

### Cómo Funciona

1. **Telegram/WhatsApp envía mensaje** → `bot_telegram.py` recibe
2. **Bot parsea comando** → Llama `TurnoService.verificar_disponibilidad()`
3. **Services ejecuta lógica** → Sin saber si es CLI o Bot
4. **Respuesta formateada** → Se devuelve al chat

**Código de ejemplo (Telegram):**

```python
from services import TurnoService

async def solicitar_turno_telegram(update: Update, context):
    # Usuario ingresa: /solicitar
    # Bot pide nombre
    nombre = await get_user_input(update, "¿Tu nombre?")
    
    # Bot pide fecha
    fecha = await get_user_input(update, "¿Fecha deseada?")
    
    # Usa la MISMA lógica que CLI
    disponible, estado, mensaje = TurnoService.verificar_disponibilidad(fecha)
    
    # Envía mensaje al chat
    await update.message.reply_text(mensaje)
```

### Librerías Recomendadas

| Plataforma | Librería | Instalación |
|-----------|----------|-------------|
| **Telegram** | `python-telegram-bot` | `pip install python-telegram-bot` |
| **WhatsApp** | `Twilio` | `pip install twilio` |
| **Discord** | `discord.py` | `pip install discord.py` |

### Ventajas de este Diseño

- ✅ **Sin duplicación de código**: Lógica reutilizable
- ✅ **Desacoplamiento**: UI independiente de servicios
- ✅ **Testeable**: Cada módulo se prueba independientemente
- ✅ **Mantenible**: Cambios en lógica no afectan bot
- ✅ **Escalable**: Agregar nuevas plataformas es trivial

---

## ⚙️ Máquina de Estados Implementada ✅

**SÍ, está totalmente implementada.** La máquina de estados funciona **junto con el BPMN**, sin romper el flujo:

### Transiciones Explícitas

Cada función retorna un tupla: `(resultado, estado_nuevo, mensaje)`

```python
# Ejemplo en main.py
disponible, estado_compuerta, mensaje = TurnoService.verificar_disponibilidad(fecha)

if disponible:
    exitoso, estado_registro, mensaje = TurnoService.registrar_turno(nombre, fecha)
else:
    estado_actual = EstadoTurno.ESPERA_REINTENTOS
```

### Ventajas

- ✅ Trazabilidad total del proceso
- ✅ Fácil debugging
- ✅ Independencia de plataforma (CLI, Telegram, etc)
- ✅ Documentación automática del flujo

---

## 📂 Estructura CSV

```
nombre,fecha,estado
Juan Pérez,20/06/2026,confirmado
María García,21/06/2026,confirmado
Carlos López,20/06/2026,confirmado
```

---

## ✅ Características

**Validaciones:**
- ✓ Nombre: 2-50 caracteres
- ✓ Fecha: DD/MM/YYYY o DD-MM-YYYY
- ✓ No fechas pasadas
- ✓ Máximo 5 turnos/día
- ✓ Máximo 3 intentos de reintentos

**Robustez:**
- ✓ Manejo completo de excepciones
- ✓ Encoding UTF-8
- ✓ Inicialización automática de CSV
- ✓ Mensajes claros al usuario

**Arquitectura:**
- ✓ Modularidad total (MVC)
- ✓ Máquina de estados
- ✓ Desacoplamiento de UI y lógica
- ✓ Listo para escalabilidad

---

## 🔧 Desarrollo Futuro

- [ ] Implementar opciones 3, 4 en el menú
- [ ] Bot de Telegram
- [ ] Bot de WhatsApp (Twilio)
- [ ] API REST (FastAPI/Flask)
- [ ] Frontend web (React/Vue)
- [ ] Base de datos (SQLite/PostgreSQL)
- [ ] Autenticación de usuarios
- [ ] Sistema de notificaciones

---

## 📚 Documentación

Ver `bot_telegram.py` para template de integración con Telegram.

---

Link de acceso al drive compartido:
https://drive.google.com/drive/folders/1nySd77CQ2Gzh5O328UdJ-qDWG6a72HjD?usp=sharing
