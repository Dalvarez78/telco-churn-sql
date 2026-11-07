"""
Generación de gráficos para el análisis de retención de clientes.
Colores extraídos del CSS del proyecto.
"""

import sqlite3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


# Variables del CSS del portfolio
COLOR_NAVY = "#18203a"
COLOR_MUTED = "#536083"
COLOR_COBALT = "#3054de"
COLOR_CORAL = "#ff7869"
COLOR_LIME = "#c8ff48"
COLOR_PERIWINKLE = "#8296eb"
COLOR_SOFT_BLUE = "#b9d9ff"
COLOR_LAVENDER = "#c9b8ff"
COLOR_GRID = "#18203a18"


def configurar_estilo():
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "sans-serif"]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["figure.facecolor"] = "#ffffff"
    plt.rcParams["axes.facecolor"] = "#ffffff"
    plt.rcParams["axes.edgecolor"] = "#18203a28"
    plt.rcParams["axes.linewidth"] = 0.9


def generar_grafico_1(conexion: sqlite3.Connection, ruta_salida: Path):
    """Gráfico 1: Fuga mensual de ingresos (MRR) por contrato y antigüedad."""
    query = """
    SELECT 
        Contract || ' (' || 
        CASE 
            WHEN tenure <= 6 THEN '0-6m'
            WHEN tenure <= 12 THEN '7-12m'
            WHEN tenure <= 24 THEN '1-2a'
            ELSE '>2a'
        END || ')' AS segmento,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS mrr_perdido,
        ROUND(100.0 * COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) / COUNT(*), 1) AS tasa_churn
    FROM telco_churn
    GROUP BY Contract, 
             CASE 
                 WHEN tenure <= 6 THEN '0-6m'
                 WHEN tenure <= 12 THEN '7-12m'
                 WHEN tenure <= 24 THEN '1-2a'
                 ELSE '>2a'
             END
    ORDER BY mrr_perdido DESC
    LIMIT 7;
    """
    df = pd.read_sql_query(query, conexion)

    fig, ax = plt.subplots(figsize=(10, 5.4), dpi=300)

    colores = [
        COLOR_CORAL if i == 0 else
        COLOR_COBALT if i in [1, 2] else
        COLOR_PERIWINKLE if i == 3 else
        COLOR_SOFT_BLUE
        for i in range(len(df))
    ]

    barras = ax.bar(df["segmento"], df["mrr_perdido"], color=colores, width=0.58, edgecolor=COLOR_NAVY, linewidth=1.1)

    ax.set_ylabel("Fuga Mensual de Ingresos ($ USD)", fontsize=11, fontweight="bold", color=COLOR_NAVY)
    ax.set_title("Fuga de Ingresos (MRR) por Tipo de Contrato y Antigüedad", fontsize=13, fontweight="bold", pad=15, color=COLOR_NAVY)
    ax.grid(axis="y", linestyle="--", alpha=0.5, color=COLOR_MUTED)
    ax.tick_params(colors=COLOR_NAVY, labelsize=9)
    plt.xticks(rotation=18, ha="right")

    for i, (barra, tasa, mrr) in enumerate(zip(barras, df["tasa_churn"], df["mrr_perdido"])):
        altura = barra.get_height()
        ax.annotate(
            f"${mrr:,.0f}\n({tasa}%)",
            xy=(barra.get_x() + barra.get_width() / 2, altura),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color=COLOR_CORAL if i == 0 else COLOR_NAVY
        )

    ax.set_ylim(0, max(df["mrr_perdido"]) * 1.22)
    plt.tight_layout()
    fig.savefig(ruta_salida, dpi=300)
    plt.close(fig)
    print(f"  - {ruta_salida.name} (fuga de ingresos por contrato)")


def generar_grafico_2(conexion: sqlite3.Connection, ruta_salida: Path):
    """Gráfico 2: Churn en clientes de 0 a 6 meses según servicio y método de pago."""
    query = """
    SELECT 
        InternetService || ' + ' || PaymentMethod AS combinacion,
        COUNT(*) AS total,
        COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) AS cancelaciones,
        ROUND(100.0 * COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) / COUNT(*), 1) AS tasa_churn
    FROM telco_churn
    WHERE Contract = 'Month-to-month' AND tenure <= 6
    GROUP BY InternetService, PaymentMethod
    HAVING total >= 25
    ORDER BY tasa_churn ASC;
    """
    df = pd.read_sql_query(query, conexion)

    fig, ax = plt.subplots(figsize=(10.5, 6.0), dpi=300)

    colores = [
        COLOR_CORAL if "Fiber optic + Electronic check" in c else
        COLOR_PERIWINKLE if "Fiber" in c else
        COLOR_SOFT_BLUE if "DSL" in c else
        "#e5e8f0"
        for c in df["combinacion"]
    ]

    barras = ax.barh(df["combinacion"], df["tasa_churn"], color=colores, height=0.65, edgecolor=COLOR_NAVY, linewidth=1.0)

    ax.set_xlabel("Tasa de Abandono (Churn %)", fontsize=11, fontweight="bold", color=COLOR_NAVY)
    ax.set_title("Segmento Crítico (0-6 meses): Churn por Servicio y Método de Pago", fontsize=13, fontweight="bold", pad=15, color=COLOR_NAVY)
    ax.grid(axis="x", linestyle="--", alpha=0.5, color=COLOR_MUTED)
    ax.tick_params(colors=COLOR_NAVY, labelsize=9)

    for barra, total, canc in zip(barras, df["total"], df["cancelaciones"]):
        ancho = barra.get_width()
        es_critico = ancho > 70
        ax.annotate(
            f" {ancho:.1f}% ({canc}/{total} clientes)",
            xy=(ancho, barra.get_y() + barra.get_height() / 2),
            xytext=(4, 0),
            textcoords="offset points",
            va="center",
            fontsize=8.5,
            fontweight="bold" if es_critico else "normal",
            color=COLOR_CORAL if es_critico else COLOR_NAVY
        )

    ax.set_xlim(0, 106)
    plt.tight_layout()
    fig.savefig(ruta_salida, dpi=300)
    plt.close(fig)
    print(f"  - {ruta_salida.name} (churn por servicio y método de pago)")


def generar_grafico_3(conexion: sqlite3.Connection, ruta_salida: Path):
    """Gráfico 3: Impacto de la carencia de soporte técnico y seguridad online."""
    query = """
    SELECT 
        CASE 
            WHEN TechSupport = 'No' AND OnlineSecurity = 'No' THEN 'Sin Soporte ni Seguridad'
            WHEN TechSupport = 'Yes' AND OnlineSecurity = 'No' THEN 'Solo Soporte Técnico'
            WHEN TechSupport = 'No' AND OnlineSecurity = 'Yes' THEN 'Solo Seguridad Online'
            WHEN TechSupport = 'Yes' AND OnlineSecurity = 'Yes' THEN 'Con Ambos Servicios'
            ELSE 'Sin Internet'
        END AS categoria,
        COUNT(*) AS total_clientes,
        COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) AS clientes_cancelados,
        ROUND(100.0 * COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) / COUNT(*), 1) AS tasa_churn
    FROM telco_churn
    WHERE Contract = 'Month-to-month' AND tenure <= 6 AND InternetService != 'No'
    GROUP BY 1
    ORDER BY tasa_churn DESC;
    """
    df = pd.read_sql_query(query, conexion)

    fig, ax = plt.subplots(figsize=(9, 5.0), dpi=300)
    colores = [COLOR_CORAL, COLOR_PERIWINKLE, COLOR_LAVENDER, COLOR_COBALT]
    barras = ax.bar(df["categoria"], df["tasa_churn"], color=colores, width=0.55, edgecolor=COLOR_NAVY, linewidth=1.1)

    ax.set_ylabel("Tasa de Churn (%)", fontsize=11, fontweight="bold", color=COLOR_NAVY)
    ax.set_title("Efecto Protector de Soporte Técnico y Seguridad Online", fontsize=13, fontweight="bold", pad=15, color=COLOR_NAVY)
    ax.grid(axis="y", linestyle="--", alpha=0.5, color=COLOR_MUTED)
    ax.tick_params(colors=COLOR_NAVY, labelsize=9)
    plt.xticks(fontweight="bold")

    for barra, canc, tot in zip(barras, df["clientes_cancelados"], df["total_clientes"]):
        altura = barra.get_height()
        ax.annotate(
            f"{altura:.1f}%\n({canc}/{tot})",
            xy=(barra.get_x() + barra.get_width() / 2, altura),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color=COLOR_NAVY
        )

    ax.set_ylim(0, 85)
    plt.tight_layout()
    fig.savefig(ruta_salida, dpi=300)
    plt.close(fig)
    print(f"  - {ruta_salida.name} (impacto de soporte técnico y seguridad)")


def generar_grafico_4(conexion: sqlite3.Connection, ruta_salida: Path):
    """Gráfico 4: Impacto económico y ROI de la campaña de retención."""
    conceptos = [
        "Fuga Anual\nActual (100%)",
        "Ingreso Anual\nRecuperado (25%)",
        "Coste Campaña\n(6 meses)",
        "Beneficio Neto\n(Año 1)"
    ]
    montos = [596175.60, 149043.90, 11178.29, 137865.61]
    colores = [COLOR_MUTED, COLOR_COBALT, COLOR_CORAL, COLOR_LIME]

    fig, ax = plt.subplots(figsize=(9.2, 5.5), dpi=300)
    barras = ax.bar(conceptos, montos, color=colores, width=0.55, edgecolor=COLOR_NAVY, linewidth=1.2)

    ax.set_ylabel("Valor Económico ($ USD)", fontsize=11, fontweight="bold", color=COLOR_NAVY)
    ax.set_title("Simulación Financiera y Retorno de Inversión (ROI)", fontsize=13, fontweight="bold", pad=15, color=COLOR_NAVY)
    ax.grid(axis="y", linestyle="--", alpha=0.5, color=COLOR_MUTED)
    ax.tick_params(colors=COLOR_NAVY, labelsize=9)

    for i, (barra, monto) in enumerate(zip(barras, montos)):
        altura = barra.get_height()
        texto = f"${monto:,.0f}"
        if i == 3:
            texto += "\n(ROI: +1,233%)"
        ax.annotate(
            texto,
            xy=(barra.get_x() + barra.get_width() / 2, altura),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
            color=COLOR_NAVY
        )

    ax.set_ylim(0, max(montos) * 1.20)
    plt.tight_layout()
    fig.savefig(ruta_salida, dpi=300)
    plt.close(fig)
    print(f"  - {ruta_salida.name} (simulación financiera y ROI)")


def generar_todas_las_visualizaciones(ruta_bd: Path = None, carpeta_salidas: Path = None):
    """Ejecuta la generación de los cuatro gráficos."""
    directorio_raiz = Path(__file__).resolve().parent.parent
    if ruta_bd is None:
        ruta_bd = directorio_raiz / "telco_churn.db"
    if carpeta_salidas is None:
        carpeta_salidas = directorio_raiz / "outputs"

    carpeta_salidas.mkdir(parents=True, exist_ok=True)

    if not ruta_bd.exists():
        raise FileNotFoundError(f"No existe la base de datos en {ruta_bd}.")

    print("Generando gráficos...")

    configurar_estilo()
    conexion = sqlite3.connect(ruta_bd)

    generar_grafico_1(conexion, carpeta_salidas / "grafico_01_mrr_perdido_contrato.png")
    generar_grafico_2(conexion, carpeta_salidas / "grafico_02_segmento_riesgo_pago.png")
    generar_grafico_3(conexion, carpeta_salidas / "grafico_03_soporte_seguridad.png")
    generar_grafico_4(conexion, carpeta_salidas / "grafico_04_simulacion_roi.png")

    conexion.close()
    print("Gráficos guardados en outputs/.\n")


if __name__ == "__main__":
    generar_todas_las_visualizaciones()
