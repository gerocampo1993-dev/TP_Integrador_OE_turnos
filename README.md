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

## ⚙️ Máquina de Estados Implementada ✅

**SÍ, está totalmente implementada.** La máquina de estados funciona **junto con el BPMN**, sin romper el flujo:

### Estados Definidos

```python
class EstadoTurno(Enum):
    INICIO = "inicio"
    VALIDANDO_NOMBRE = "validando_nombre"
    VALIDANDO_FECHA = "validando_fecha"
    VERIFICANDO_DISPONIBILIDAD = "verificando_disponibilidad"  # COMPUERTA 1
    REGISTRADO = "registrado"
    ESPERA_REINTENTOS = "espera_reintentos"  # COMPUERTA 2
    CANCELADO = "cancelado"
    ERROR = "error"
```

### Diagrama de Transiciones

```
    ┌─ INICIO
    │
    ├─ VALIDANDO_NOMBRE (Entrada: nombre)
    │
    ├─ VALIDANDO_FECHA (Entrada: fecha)
    │
    ├─ VERIFICANDO_DISPONIBILIDAD (COMPUERTA 1)
    │  ├─ ¿Disponible? SÍ
    │  │  └─ REGISTRADO → FIN ✓
    │  │
    │  └─ ¿Disponible? NO
    │     └─ ESPERA_REINTENTOS (COMPUERTA 2)
    │        ├─ ¿Reintentar SÍ? (< 3)
    │        │  └─ VALIDANDO_FECHA (loop)
    │        │
    │        └─ ¿Reintentar NO? o máx intentos
    │           └─ CANCELADO → FIN ✗
    │
    └─ ERROR (excepción)
```

### Cómo Funciona

1. **Cada función retorna un tupla**: `(resultado, estado_nuevo)`
2. **El estado se actualiza constantemente** según el progreso del flujo
3. **Las transiciones son explícitas**: se registra cada cambio de estado
4. **BPMN + Máquina de Estados**: complementan, no compiten

### Ejemplo de Transición en Código

```python
# El programa rastrear el estado
nombre, estado_actual = obtener_nombre()  # → VALIDANDO_NOMBRE
mostrar_transicion(EstadoTurno.INICIO, estado_actual)

fecha, estado_actual = obtener_fecha()  # → VALIDANDO_FECHA
disponible, estado_compuerta1 = turno_disponible(fecha)  # → VERIFICANDO_DISPONIBILIDAD

if disponible:
    exitoso, estado_registro = registrar_turno(nombre, fecha)  # → REGISTRADO
else:
    estado_actual = EstadoTurno.ESPERA_REINTENTOS
```

### Ventajas de esta Implementación

- ✅ Trazabilidad total del proceso
- ✅ Fácil de debuguear (se ve en qué estado está)
- ✅ Escalable: agregar nuevos estados es trivial
- ✅ Reutilizable: la máquina de estados es independiente del BPMN
- ✅ Documentación automática: los estados explican el flujo

### Desactivar Transiciones en Consola

La función `mostrar_transicion()` está desactivada por defecto. Para ver cada transición en consola, descomenta esta línea en `main.py`:

```python
# mostrar_transicion(estado_anterior, estado_nuevo)  # Descomentar para debugging
```

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
