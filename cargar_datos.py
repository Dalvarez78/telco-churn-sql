"""
Punto de entrada principal para la ingesta y preparación de datos.
Ejecuta el pipeline optimizado desde src/cargar_datos.py.
"""
import sys
from pathlib import Path

# Añadimos la raíz al PYTHONPATH para importación directa
directorio_raiz = Path(__file__).resolve().parent
if str(directorio_raiz) not in sys.path:
    sys.path.insert(0, str(directorio_raiz))

from src.cargar_datos import cargar_base_datos

if __name__ == "__main__":
    cargar_base_datos()
