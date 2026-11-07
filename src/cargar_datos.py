"""
Módulo: src.cargar_datos
Descripción: Carga, limpieza y tipado del dataset de clientes hacia SQLite.
"""

import sqlite3
from pathlib import Path
import pandas as pd


def obtener_rutas_proyecto() -> tuple[Path, Path, Path]:
    """Resuelve dinámicamente las rutas absolutas del proyecto."""
    directorio_raiz = Path(__file__).resolve().parent.parent
    
    ruta_csv_raiz = directorio_raiz / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    ruta_csv_data = directorio_raiz / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    ruta_csv = ruta_csv_data if ruta_csv_data.exists() else ruta_csv_raiz

    ruta_bd = directorio_raiz / "telco_churn.db"
    return directorio_raiz, ruta_csv, ruta_bd


def cargar_base_datos(verbose: bool = True) -> Path:
    """Lee el CSV de clientes, limpia los tipos y crea la tabla en SQLite con índices."""
    directorio_raiz, ruta_csv, ruta_bd = obtener_rutas_proyecto()

    if not ruta_csv.exists():
        raise FileNotFoundError(f"No se encontró el archivo CSV en {ruta_csv}")

    if verbose:
        print(f"Leyendo datos desde {ruta_csv.name}...")

    df = pd.read_csv(ruta_csv)

    # Limpieza: TotalCharges contiene espacios en blanco en registros con tenure=0
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0.0)

    conexion = sqlite3.connect(ruta_bd)
    df.to_sql("telco_churn", conexion, if_exists="replace", index=False)

    cursor = conexion.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_contract_tenure ON telco_churn(Contract, tenure);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_churn ON telco_churn(Churn);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_internet_payment ON telco_churn(InternetService, PaymentMethod);")
    conexion.commit()
    conexion.close()

    if verbose:
        print(f"Base de datos {ruta_bd.name} creada correctamente con {len(df):,} registros.")

    return ruta_bd


if __name__ == "__main__":
    cargar_base_datos()
