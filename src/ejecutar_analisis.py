"""
Módulo: src.ejecutar_analisis
Descripción: Ejecución de consultas SQL sobre SQLite, exportación de resultados
y generación de gráficos e informes.
"""

import sqlite3
from pathlib import Path
import pandas as pd
from src.generar_visualizaciones import generar_todas_las_visualizaciones


def formatear_valor(valor) -> str:
    """Formatea valores numéricos para tablas en markdown."""
    if pd.isna(valor):
        return ""
    if isinstance(valor, float):
        if valor.is_integer():
            return f"{int(valor):,}"
        return f"{valor:,.2f}"
    if isinstance(valor, int):
        return f"{valor:,}"
    return str(valor)


def convertir_a_tabla_markdown(df: pd.DataFrame) -> str:
    """Convierte un DataFrame a formato tabla Markdown."""
    columnas = [str(col) for col in df.columns]
    filas = [[formatear_valor(val) for val in fila] for fila in df.itertuples(index=False)]

    anchos = [max(len(c), max((len(f[i]) for f in filas), default=0)) for i, c in enumerate(columnas)]

    cabecera = "| " + " | ".join(c.ljust(anchos[i]) for i, c in enumerate(columnas)) + " |"
    separador = "| " + " | ".join("-" * anchos[i] for i in range(len(columnas))) + " |"
    lineas_filas = [
        "| " + " | ".join(val.ljust(anchos[i]) for i, val in enumerate(fila)) + " |" for fila in filas
    ]

    return "\n".join([cabecera, separador] + lineas_filas)


def ejecutar_analisis():
    """Ejecuta las consultas SQL y genera los reportes."""
    directorio_raiz = Path(__file__).resolve().parent.parent
    ruta_bd = directorio_raiz / "telco_churn.db"
    carpeta_consultas = directorio_raiz / "queries"
    carpeta_salidas = directorio_raiz / "outputs"

    carpeta_salidas.mkdir(parents=True, exist_ok=True)

    if not ruta_bd.exists():
        print(f"Error: No se encontró {ruta_bd.name}. Ejecuta antes cargar_datos.py.")
        return

    print("Ejecutando consultas SQL...")
    conexion = sqlite3.connect(ruta_bd)

    consultas = [
        (
            "01_tasa_churn_contrato_antiguedad.sql",
            "Consulta 1: Tasa de Abandono y Fuga de Ingresos por Contrato y Antigüedad"
        ),
        (
            "02_segmento_critico_riesgo.sql",
            "Consulta 2: Segmento Crítico (Nuevos Clientes 0-6 Meses sin Permanencia)"
        ),
        (
            "03_friccion_soporte_seguridad.sql",
            "Consulta 3: Diagnóstico Causal - Carencia de Soporte Técnico y Ciberseguridad"
        ),
        (
            "04_simulacion_roi_retencion.sql",
            "Consulta 4: Simulación de Negocio, Impacto Financiero y ROI de Retención"
        ),
    ]

    resultados = {}

    for nombre_archivo, titulo in consultas:
        ruta_sql = carpeta_consultas / nombre_archivo
        
        if not ruta_sql.exists():
            nombre_legacy = nombre_archivo.replace("01_tasa_churn_contrato_antiguedad.sql", "consulta_1_contrato_antiguedad.sql")
            nombre_legacy = nombre_legacy.replace("02_segmento_critico_riesgo.sql", "consulta_2_segmento_riesgo.sql")
            ruta_sql = carpeta_consultas / nombre_legacy

        if not ruta_sql.exists():
            continue

        print(f"\n{titulo}:")
        codigo_sql = ruta_sql.read_text(encoding="utf-8")
        df = pd.read_sql_query(codigo_sql, conexion)
        resultados[nombre_archivo] = df

        ruta_csv = carpeta_salidas / f"{Path(nombre_archivo).stem}.csv"
        df.to_csv(ruta_csv, index=False, encoding="utf-8")

        print(df.to_string(index=False))

    conexion.close()
    print()

    # Generación de gráficos
    generar_todas_las_visualizaciones(ruta_bd, carpeta_salidas)

    # Redacción del informe
    generar_informe_markdown(carpeta_salidas, resultados)
    print("Informe generado en outputs/informe_de_analisis.md\n")


def generar_informe_markdown(carpeta_salidas: Path, resultados: dict):
    """Escribe el informe consolidado en Markdown."""
    ruta_informe = carpeta_salidas / "informe_de_analisis.md"

    with open(ruta_informe, "w", encoding="utf-8") as archivo:
        archivo.write("# Informe Ejecutivo: Análisis Estratégico de Retención y Fuga de Ingresos\n\n")
        archivo.write("> **Autor:** David Álvarez  \n")
        archivo.write("> **Especialidad:** Análisis de Datos & Estrategia Cuantitativa  \n")
        archivo.write("> **Objetivo:** *Identificar el foco principal de pérdida de ingresos recurrentes (MRR) por abandono de clientes en telecomunicaciones y modelar una estrategia cuantitativa de retención.*\n\n")
        archivo.write("---\n\n")

        archivo.write("## 1. Contexto de Negocio y Pregunta Central\n\n")
        archivo.write("En este análisis examino el comportamiento de **7,043 clientes** de telecomunicaciones mediante SQL relacional y Python para responder a una necesidad comercial crítica:\n\n")
        archivo.write("* **Pregunta Central:** ¿Qué combinación de tipo de contrato y antigüedad concentra la mayor fuga mensual de ingresos (MRR), qué factores operativos la causan y cuál es el impacto financiero neto de una campaña de retención proactiva?\n\n")

        archivo.write("### Indicadores Clave del Negocio (KPIs)\n")
        archivo.write("- **Fuga Total de Ingresos (MRR):** $139,130.85 USD / mes ($1,669,570.20 USD anualizados).\n")
        archivo.write("- **Foco de Mayor Riesgo:** Clientes con contrato mensual y 0-6 meses de antigüedad concentran **$49,681.30 USD/mes** (el 35.7% de todas las pérdidas de la compañía).\n")
        archivo.write("- **Tasa de Abandono en el Foco:** **55.2%** de abandono temprano (780 bajas en 1,413 clientes nuevos).\n")
        archivo.write("- **Segmento Más Crítico:** Fibra Óptica + Cheque Electrónico alcanza un **75.5% de abandono**.\n")
        archivo.write("- **Factor Causal:** El 76% de los clientes cancelados en este segmento carecía de soporte técnico y seguridad online.\n")
        archivo.write("- **Retorno de Inversión (ROI Proyectado):** **+1,233.3%** rescatando al 25% de los clientes en riesgo.\n\n")

        archivo.write("---\n\n")

        # Sección 1
        archivo.write("## 2. Fuga de Ingresos por Tipo de Contrato y Antigüedad\n\n")
        archivo.write("Analizo el impacto económico mensual según el tipo de permanencia y el rango de meses del cliente:\n\n")
        
        df1 = resultados.get("01_tasa_churn_contrato_antiguedad.sql")
        if df1 is not None:
            archivo.write(convertir_a_tabla_markdown(df1) + "\n\n")

        archivo.write("![Fuga Mensual de Ingresos](grafico_01_mrr_perdido_contrato.png)\n\n")
        archivo.write("### Conclusiones de este Paso:\n")
        archivo.write("- **Concentración Crítica:** Más de un tercio de las pérdidas de dinero de la compañía proviene de usuarios sin permanencia en su primer semestre.\n")
        archivo.write("- **Efecto Blindaje de la Permanencia:** En contratos anuales y bianuales, el abandono cae por debajo del 12% y 3% respectivamente.\n\n")

        archivo.write("---\n\n")

        # Sección 2
        archivo.write("## 3. Radiografía del Segmento Crítico: Servicios y Canal de Pago\n\n")
        archivo.write("Aislando exclusivamente la cohorte vulnerable (contrato mes a mes y $\\le$ 6 meses), profundizo en el cruce de conectividad y método de facturación:\n\n")

        df2 = resultados.get("02_segmento_critico_riesgo.sql")
        if df2 is not None:
            archivo.write(convertir_a_tabla_markdown(df2) + "\n\n")

        archivo.write("![Segmento Crítico por Servicio y Pago](grafico_02_segmento_riesgo_pago.png)\n\n")
        archivo.write("### Conclusiones de este Paso:\n")
        archivo.write("- **Impacto de la Tarifa de Fibra:** La fibra óptica tiene tarifas más altas (~$80-$90 USD/mes), incrementando la sensibilidad al precio.\n")
        archivo.write("- **Fricción del Cheque Electrónico (`Electronic check`):** Al no ser automático, cada mes el usuario debe tomar la decisión consciente de abonar la factura, facilitando la cancelación (abandono del 75.5%).\n\n")

        archivo.write("---\n\n")

        # Sección 3
        archivo.write("## 4. Diagnóstico Causal: La Carencia de Asistencia Técnica y Ciberseguridad\n\n")
        archivo.write("Al evaluar la adopción de servicios complementarios en este grupo vulnerable, identifico la causa operativa de fondo:\n\n")

        df3 = resultados.get("03_friccion_soporte_seguridad.sql")
        if df3 is not None:
            archivo.write(convertir_a_tabla_markdown(df3) + "\n\n")

        archivo.write("![Efecto Protector de Soporte y Seguridad](grafico_03_soporte_seguridad.png)\n\n")
        archivo.write("### Conclusiones de este Paso:\n")
        archivo.write("- **Vulnerabilidad Técnica Inicial:** De los 780 clientes fugados, **593 usuarios (el 76%) no contaban con Soporte Técnico ni Seguridad Online**.\n")
        archivo.write("- Quienes carecen de soporte sufren un **69.0% de churn**, mientras que quienes tienen ambos servicios ven reducida la tasa a casi la mitad.\n\n")

        archivo.write("---\n\n")

        # Sección 4
        archivo.write("## 5. Modelo Financiero y Retorno sobre la Inversión (ROI)\n\n")
        archivo.write("Simulación financiera con CTEs evaluando el rescate del 25% de los clientes en riesgo:\n\n")

        df4 = resultados.get("04_simulacion_roi_retencion.sql")
        if df4 is not None:
            archivo.write(convertir_a_tabla_markdown(df4) + "\n\n")

        archivo.write("![Simulación Financiera y ROI](grafico_04_simulacion_roi.png)\n\n")

        archivo.write("### Plan de Acción Propuesto:\n")
        archivo.write("1. **Disparador Automatizado (Día 75 / Mes 3):** Identifico en el CRM a los usuarios de fibra óptica en contrato mensual que pagan con cheque electrónico y no tienen soporte técnico.\n")
        archivo.write("2. **Incentivo Vinculado:** Ofrezco un **15% de descuento durante 6 meses** condicionado a dos condiciones comerciales:\n")
        archivo.write("   - Aceptación de un **contrato de permanencia anual (One-year contract)**.\n")
        archivo.write("   - Domiciliación del cobro mediante **tarjeta bancaria o cuenta bancaria automática**.\n")
        archivo.write("3. **Kit de Onboarding y Fidelización:** Incluyo durante los primeros 3 meses el servicio de **Soporte Técnico y Seguridad Web** sin coste adicional.\n")
        archivo.write("4. **Rentabilidad Neta:** Con una meta de rescatar al 25% de los clientes en riesgo, protejo **$149,043.90 USD/año**, invirtiendo $11,178.29 USD en descuentos, lo que genera un **beneficio neto de $137,865.61 USD** y un **ROI del +1,233.3%**.\n")
