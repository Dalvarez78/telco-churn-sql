"""
Punto de entrada principal para el análisis SQL y exportación de reportes.
Ejecuta el pipeline completo desde src/ejecutar_analisis.py.
"""
import sys
from pathlib import Path

# Añadimos la raíz al PYTHONPATH para importación directa
directorio_raiz = Path(__file__).resolve().parent
if str(directorio_raiz) not in sys.path:
    sys.path.insert(0, str(directorio_raiz))

from src.ejecutar_analisis import ejecutar_analisis

if __name__ == "__main__":
    ejecutar_analisis()
