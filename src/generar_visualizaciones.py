"""
Módulo: src.generar_visualizaciones
Descripción: Genera gráficos de alta resolución (300 DPI) para el portfolio
de Lovable, GitHub README y reportes ejecutivos para reclutadores.
"""

import sqlite3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def configurar_estilo_graficos():
    """Aplica una estética profesional, limpia y ejecutiva."""
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    plt.rcParams["font.family"] = "sans-serif"
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams["axes.edgecolor"] = "#cccccc"
    plt.rcParams["axes.linewidth"] = 0.8


def generar_grafico_1(conexion: sqlite3.Connection, ruta_salida: Path):
    """Gráfico 1: Pérdida mensual de ingresos (MRR) y tasa de churn por contrato y antigüedad."""
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

    fig, ax1 = plt.subplots(figsize=(10, 5.5), dpi=300)

    # Colores: destacar el grupo de mayor riesgo en coral
    colores = ["#d90429" if i == 0 else "#2b2d42" for i in range(len(df))]
    barras = ax1.bar(df["segmento"], df["mrr_perdido"], color=colores, width=0.6, alpha=0.9)

    ax1.set_ylabel("Fuga Mensual de Ingresos ($ USD / mes)", fontsize=11, fontweight="bold", color="#1f2937")
    ax1.set_title("Fuga de Ingresos (MRR) por Tipo de Contrato y Antigüedad", fontsize=13, fontweight="bold", pad=15)
    ax1.grid(axis="y", linestyle="--", alpha=0.6)
    plt.xticks(rotation=20, ha="right", fontsize=9)

    # Etiquetas con montos y porcentaje de churn
    for i, (barra, tasa, mrr) in enumerate(zip(barras, df["tasa_churn"], df["mrr_perdido"])):
        altura = barra.get_height()
        ax1.annotate(
            f"${mrr:,.0f}\n({tasa}%)",
            xy=(barra.get_x() + barra.get_width() / 2, altura),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold" if i == 0 else "normal",
            color="#d90429" if i == 0 else "#374151"
        )

    ax1.set_ylim(0, max(df["mrr_perdido"]) * 1.22)
    plt.tight_layout()
    fig.savefig(ruta_salida, dpi=300)
    plt.close(fig)
    print(f"  ✔ Gráfico 1 guardado: {ruta_salida.name}")


def generar_grafico_2(conexion: sqlite3.Connection, ruta_salida: Path):
    """Gráfico 2: Tasa de churn en clientes de 0 a 6 meses según servicio y pago."""
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

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    # Resaltar en rojo los casos más críticos
    colores = ["#d90429" if "Fiber optic + Electronic check" in c else "#457b9d" if "Fiber" in c else "#a8dadc" for c in df["combinacion"]]
    barras = ax.barh(df["combinacion"], df["tasa_churn"], color=colores, height=0.65)

    ax.set_xlabel("Tasa de Abandono (Churn %)", fontsize=11, fontweight="bold", color="#1f2937")
    ax.set_title("Segmento Crítico (0-6 meses sin permanencia): Churn por Servicio y Pago", fontsize=13, fontweight="bold", pad=15)
    ax.grid(axis="x", linestyle="--", alpha=0.6)

    for barra, total, canc in zip(barras, df["total"], df["cancelaciones"]):
        ancho = barra.get_width()
        ax.annotate(
            f" {ancho:.1f}% ({canc}/{total} clientes)",
            xy=(ancho, barra.get_y() + barra.get_height() / 2),
            xytext=(3, 0),
            textcoords="offset points",
            va="center",
            fontsize=8.5,
            fontweight="bold" if ancho > 70 else "normal",
            color="#d90429" if ancho > 70 else "#1f2937"
        )

    ax.set_xlim(0, 105)
    plt.tight_layout()
    fig.savefig(ruta_salida, dpi=300)
    plt.close(fig)
    print(f"  ✔ Gráfico 2 guardado: {ruta_salida.name}")


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

    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    colores = ["#d90429", "#e76f51", "#2a9d8f", "#264653"]
    barras = ax.bar(df["categoria"], df["tasa_churn"], color=colores, width=0.55)

    ax.set_ylabel("Tasa de Churn (%)", fontsize=11, fontweight="bold")
    ax.set_title("Efecto Protector de Servicios de Soporte y Seguridad (Nuevos Clientes)", fontsize=13, fontweight="bold", pad=15)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    plt.xticks(fontsize=9, fontweight="bold")

    for barra, canc, tot in zip(barras, df["clientes_cancelados"], df["total_clientes"]):
        altura = barra.get_height()
        ax.annotate(
            f"{altura:.1f}%\n({canc}/{tot})",
            xy=(barra.get_x() + barra.get_width() / 2, altura),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold"
        )

    ax.set_ylim(0, 85)
    plt.tight_layout()
    fig.savefig(ruta_salida, dpi=300)
    plt.close(fig)
    print(f"  ✔ Gráfico 3 guardado: {ruta_salida.name}")


def generar_grafico_4(conexion: sqlite3.Connection, ruta_salida: Path):
    """Gráfico 4: Impacto económico y ROI de la campaña de retención."""
    # Valores proyectados desde la consulta 4
    conceptos = [
        "Fuga Anual\nActual (100%)",
        "Ingreso Anual\nRecuperado (25%)",
        "Coste de Inversión\nCampaña (6 meses)",
        "Beneficio Neto\nRecuperado (Año 1)"
    ]
    montos = [596175.60, 149043.90, 11178.29, 137865.61]
    colores = ["#6c757d", "#2a9d8f", "#e76f51", "#1d3557"]

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    barras = ax.bar(conceptos, montos, color=colores, width=0.55)

    ax.set_ylabel("Valor Económico ($ USD)", fontsize=11, fontweight="bold")
    ax.set_title("Simulación Financiera y ROI de la Campaña de Retención", fontsize=13, fontweight="bold", pad=15)
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    for i, (barra, monto) in enumerate(zip(barras, montos)):
        altura = barra.get_height()
        texto = f"${monto:,.0f}"
        if i == 3:
            texto += "\n(ROI: +1,233%)"
        ax.annotate(
            texto,
            xy=(barra.get_x() + barra.get_width() / 2, altura),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color=colores[i]
        )

    ax.set_ylim(0, max(montos) * 1.18)
    plt.tight_layout()
    fig.savefig(ruta_salida, dpi=300)
    plt.close(fig)
    print(f"  ✔ Gráfico 4 guardado: {ruta_salida.name}")


def generar_todas_las_visualizaciones(ruta_bd: Path = None, carpeta_salidas: Path = None):
    """Ejecuta la generación completa de gráficos ejecutivos."""
    directorio_raiz = Path(__file__).resolve().parent.parent
    if ruta_bd is None:
        ruta_bd = directorio_raiz / "telco_churn.db"
    if carpeta_salidas is None:
        carpeta_salidas = directorio_raiz / "outputs"

    carpeta_salidas.mkdir(parents=True, exist_ok=True)

    if not ruta_bd.exists():
        raise FileNotFoundError(f"No existe la base de datos en {ruta_bd}. Ejecuta primero cargar_datos.py.")

    print("=" * 70)
    print(" GENERACIÓN DE VISUALIZACIONES PARA RECRUITERS & PORTFOLIO LOVABLE ")
    print("=" * 70)

    configurar_estilo_graficos()
    conexion = sqlite3.connect(ruta_bd)

    generar_grafico_1(conexion, carpeta_salidas / "grafico_01_mrr_perdido_contrato.png")
    generar_grafico_2(conexion, carpeta_salidas / "grafico_02_segmento_riesgo_pago.png")
    generar_grafico_3(conexion, carpeta_salidas / "grafico_03_soporte_seguridad.png")
    generar_grafico_4(conexion, carpeta_salidas / "grafico_04_simulacion_roi.png")

    conexion.close()
    print("✔ Todas las visualizaciones se exportaron en alta definición (outputs/).\n")


if __name__ == "__main__":
    generar_todas_las_visualizaciones()

