# TP_Integrador_OE_turnos

Sistema de gestión de turnos con 2 compuertas BPMN implementadas.

**Alumnos**: Brisa Chirino y Gerardo Ocampo

---

## 📋 Arquitectura Modular

El sistema está organizado en **3 módulos** dentro de `/data`:

| Módulo | Función |
|--------|---------|
| **csv_manager.py** | Persistencia de datos (lectura/escritura CSV) |
| **turnos.py** | Lógica de negocio (compuertas y reglas) |
| **main.py** | Interfaz de usuario y orquestación del flujo |

---

## 🔄 Flujo BPMN (2 Compuertas)

```
INICIO → Obtener Datos → COMPUERTA 1: ¿Disponible?
                         ├─ SÍ → Registrar turno → FIN ✓
                         └─ NO → COMPUERTA 2: ¿Reintentar?
                                ├─ SÍ (< 3 intentos) → Volver a intentar
                                └─ NO o máx intentos → FIN ✗
```

**Compuerta 1**: Valida disponibilidad (máx 5 turnos/día)  
**Compuerta 2**: Permite hasta 3 reintentos

---

## ⚙️ ¿Máquina de Estados Implementada?

**No completamente.** El programa tiene un **flujo BPMN con compuertas** (decisiones lineales), no una máquina de estados completa.

- **Lo actual**: Flujo procedural con bifurcaciones
- **Máquina de estados**: Definiría múltiples estados (ej: `ESPERANDO_NOMBRE`, `ESPERANDO_FECHA`, `VERIFICANDO`, `REGISTRADO`, `CANCELADO`)

### Si quisieras implementar máquina de estados:
```python
from enum import Enum

class EstadoTurno(Enum):
    INICIO = "inicio"
    VALIDANDO_NOMBRE = "validando_nombre"
    VALIDANDO_FECHA = "validando_fecha"
    VERIFICANDO_DISPONIBILIDAD = "verificando"
    REGISTRADO = "registrado"
    CANCELADO = "cancelado"
    ERROR = "error"
```

El código actual funciona bien, pero una máquina de estados sería más escalable si el sistema crece.

---

## 🚀 Cómo Usar

```bash
cd data
python main.py
```

---

## 📂 Estructura CSV

```
nombre,fecha,estado
Juan Pérez,15/06/2026,confirmado
María García,16/06/2026,confirmado
```

---

## ✅ Características

- Validación de nombre (2-50 caracteres)
- Validación de fecha (no pasadas, formato DD/MM/YYYY)
- Límite de 3 intentos para reintentos
- Manejo de excepciones completo
- Encoding UTF-8
- Inicialización automática de CSV

---

Link de acceso al drive compartido:
https://drive.google.com/drive/folders/1nySd77CQ2Gzh5O328UdJ-qDWG6a72HjD?usp=sharing
