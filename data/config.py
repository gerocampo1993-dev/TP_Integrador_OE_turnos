# TPI- OE: Sistemas de turnos
# Módulo: Configuración centralizada

import os
from pathlib import Path

# Directorios
DATOS_DIR = "data"
Path(DATOS_DIR).mkdir(exist_ok=True)

# Archivos
ARCHIVO_TURNOS = os.path.join(DATOS_DIR, "turnos.csv")

# Codificación
ENCODING = "utf-8"

# Lógica de negocio
MAX_TURNOS_POR_DIA = 5
MAX_REINTENTOS = 3

# Formatos permitidos
FORMATOS_FECHA = ["%d/%m/%Y", "%d-%m-%Y"]

# Validaciones
MIN_NOMBRE = 2
MAX_NOMBRE = 50

# Estados disponibles
ESTADO_CONFIRMADO = "confirmado"
ESTADO_CANCELADO = "cancelado"
