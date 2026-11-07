"""
Wrapper de compatibilidad para la ejecución completa del análisis.
"""
import sys
from pathlib import Path

directorio_raiz = Path(__file__).resolve().parent
if str(directorio_raiz) not in sys.path:
    sys.path.insert(0, str(directorio_raiz))

from src.ejecutar_analisis import ejecutar_analisis

if __name__ == "__main__":
    ejecutar_analisis()
