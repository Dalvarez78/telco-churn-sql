"""
Wrapper de compatibilidad para el script de carga de datos.
"""
import sys
from pathlib import Path

directorio_raiz = Path(__file__).resolve().parent
if str(directorio_raiz) not in sys.path:
    sys.path.insert(0, str(directorio_raiz))

from src.cargar_datos import cargar_base_datos

if __name__ == "__main__":
    cargar_base_datos()
