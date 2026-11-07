"""
Módulo: src.cargar_datos
Descripción: Pipeline de extracción, limpieza, tipado e ingesta de datos
hacia la base de datos relacional SQLite (telco_churn.db), optimizada con índices.
"""

import sqlite3
from pathlib import Path
import pandas as pd


def obtener_rutas_proyecto() -> tuple[Path, Path, Path]:
    """Resuelve dinámicamente las rutas absolutas del proyecto."""
    directorio_raiz = Path(__file__).resolve().parent.parent
    
    # Busca el CSV en la raíz o en data/
    ruta_csv_raiz = directorio_raiz / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    ruta_csv_data = directorio_raiz / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    ruta_csv = ruta_csv_data if ruta_csv_data.exists() else ruta_csv_raiz

    ruta_bd = directorio_raiz / "telco_churn.db"
    return directorio_raiz, ruta_csv, ruta_bd


def cargar_base_datos(verbose: bool = True) -> Path:
    """
    Lee el archivo CSV de clientes, aplica limpieza de datos, tipado estricto
    e indexa la base de datos relacional SQLite.
    
    Returns:
        Path: Ruta a la base de datos SQLite generada.
    """
    directorio_raiz, ruta_csv, ruta_bd = obtener_rutas_proyecto()

    if not ruta_csv.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo CSV en ninguna de las rutas esperadas:\n"
            f"- {ruta_csv}\n"
            f"- {directorio_raiz / 'WA_Fn-UseC_-Telco-Customer-Churn.csv'}"
        )

    if verbose:
        print("=" * 70)
        print("  ETL PIPELINE: INGESTA Y OPTIMIZACIÓN DE DATOS (TELCO CHURN)  ")
        print("=" * 70)
        print(f"▶ 1. Leyendo dataset origen: {ruta_csv.name}...")

    df = pd.read_csv(ruta_csv)
    filas_iniciales = len(df)

    # 1. Limpieza y coerción de tipos de datos
    # TotalCharges contiene espacios en blanco (' ') en clientes nuevos con tenure=0
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0.0)

    # 2. Conexión y persistencia en SQLite
    if verbose:
        print(f"▶ 2. Creando base de datos relacional SQLite en: {ruta_bd.name}...")
    
    conexion = sqlite3.connect(ruta_bd)
    df.to_sql("telco_churn", conexion, if_exists="replace", index=False)

    # 3. Optimización con índices relacionales para consultas de alta velocidad
    cursor = conexion.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_contract_tenure ON telco_churn(Contract, tenure);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_churn ON telco_churn(Churn);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_internet_payment ON telco_churn(InternetService, PaymentMethod);")
    conexion.commit()
    conexion.close()

    # 4. Métricas de validación
    total_clientes = len(df)
    total_churn = (df["Churn"] == "Yes").sum()
    tasa_churn_global = (total_churn / total_clientes) * 100
    mrr_total = df["MonthlyCharges"].sum()
    mrr_en_fuga = df[df["Churn"] == "Yes"]["MonthlyCharges"].sum()

    if verbose:
        print("✔ Pipeline completado exitosamente.")
        print("-" * 70)
        print(f"  • Registros cargados:          {total_clientes:,}")
        print(f"  • Total bajas históricas:      {total_churn:,} ({tasa_churn_global:.1f}%)")
        print(f"  • Facturación Mensual (MRR):   ${mrr_total:,.2f} USD")
        print(f"  • Fuga de Ingresos (Churn MRR): ${mrr_en_fuga:,.2f} USD")
        print(f"  • Índices creados:             idx_contract_tenure, idx_churn, idx_internet_payment")
        print("-" * 70)

    return ruta_bd


if __name__ == "__main__":
    cargar_base_datos()

