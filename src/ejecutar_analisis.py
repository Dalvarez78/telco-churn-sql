"""
Módulo: src.ejecutar_analisis
Descripción: Motor analítico automatizado. Ejecuta todas las consultas SQL
sobre SQLite, genera datasets limpios en CSV, produce visualizaciones
ejecutivas de alto impacto y redacta el informe en Markdown para recruiters.
"""

import sqlite3
from pathlib import Path
import pandas as pd
from src.generar_visualizaciones import generar_todas_las_visualizaciones


def formatear_valor(valor) -> str:
    """Formatea valores numéricos para visualización ejecutiva."""
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
    """Convierte un DataFrame de pandas a una tabla Markdown limpia y legible."""
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
    """Ejecuta el pipeline analítico completo."""
    directorio_raiz = Path(__file__).resolve().parent.parent
    ruta_bd = directorio_raiz / "telco_churn.db"
    carpeta_consultas = directorio_raiz / "queries"
    carpeta_salidas = directorio_raiz / "outputs"

    carpeta_salidas.mkdir(parents=True, exist_ok=True)

    if not ruta_bd.exists():
        print(f"❌ Error: No se encontró la base de datos en {ruta_bd}.")
        print("💡 Ejecuta primero: python cargar_datos.py")
        return

    print("=" * 75)
    print("  ANÁLISIS ESTRATÉGICO DE RETENCIÓN DE CLIENTES (TELCO CHURN CON SQL)  ")
    print("=" * 75)

    conexion = sqlite3.connect(ruta_bd)

    # Lista de consultas ordenadas por secuencia lógica de negocio
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
        
        # Respaldo de compatibilidad con nombres anteriores si no existe el nuevo
        if not ruta_sql.exists():
            nombre_legacy = nombre_archivo.replace("01_tasa_churn_contrato_antiguedad.sql", "consulta_1_contrato_antiguedad.sql")
            nombre_legacy = nombre_legacy.replace("02_segmento_critico_riesgo.sql", "consulta_2_segmento_riesgo.sql")
            ruta_sql = carpeta_consultas / nombre_legacy

        if not ruta_sql.exists():
            print(f"⚠️ Aviso: No se encontró el archivo de consulta {nombre_archivo}")
            continue

        print(f"\n▶ Ejecutando: {titulo}")
        print(f"  [Archivo SQL]: queries/{nombre_archivo}")

        codigo_sql = ruta_sql.read_text(encoding="utf-8")
        df = pd.read_sql_query(codigo_sql, conexion)
        resultados[nombre_archivo] = df

        # Exportación de resultados a CSV limpio
        ruta_csv = carpeta_salidas / f"{Path(nombre_archivo).stem}.csv"
        df.to_csv(ruta_csv, index=False, encoding="utf-8")
        print(f"  [Exportado CSV]: outputs/{ruta_csv.name}")

        # Mostrar tabla formateada en consola
        print("-" * 75)
        print(df.to_string(index=False))
        print("-" * 75)

    conexion.close()

    # Generación de gráficos ejecutivos de alta calidad
    generar_todas_las_visualizaciones(ruta_bd, carpeta_salidas)

    # Redacción del informe consolidado en Markdown
    generar_informe_markdown(carpeta_salidas, resultados)

    print("=" * 75)
    print("✔ ANÁLISIS COMPLETADO EXITOSAMENTE")
    print(f"  • CSVs exportados en:            outputs/")
    print(f"  • Gráficos generados en:         outputs/")
    print(f"  • Informe ejecutivo guardado en: outputs/informe_de_analisis.md")
    print("=" * 75)


def generar_informe_markdown(carpeta_salidas: Path, resultados: dict):
    """Escribe un informe de negocio exhaustivo orientado a recruiters y stakeholders."""
    ruta_informe = carpeta_salidas / "informe_de_analisis.md"

    with open(ruta_informe, "w", encoding="utf-8") as archivo:
        archivo.write("# Informe Ejecutivo de Retención: Telco Customer Churn\n\n")
        archivo.write("> **Declaración del Rol:** *Ayudo a los equipos de Marketing, Producto y Retención a blindar el flujo de ingresos recurrentes (MRR) identificando segmentos críticos de fuga de clientes mediante análisis avanzado en SQL.*\n\n")
        archivo.write("---\n\n")

        archivo.write("## 1. Resumen Ejecutivo y Pregunta de Negocio\n\n")
        archivo.write("En la industria de telecomunicaciones, el coste de adquisición de clientes (CAC) supera con creces el coste de retención. En este estudio analizo la telemetría de **7,043 clientes**, identificando la fuga de ingresos (*churn*) y diseñando una estrategia cuantitativa de alto impacto.\n\n")
        archivo.write("* **Pregunta Central:** ¿Qué combinación de contrato y antigüedad concentra la mayor fuga mensual de ingresos, cuáles son los factores causales que la aceleran y qué retorno sobre la inversión (ROI) ofrece una campaña de retención temprana?\n\n")

        archivo.write("### Principales Indicadores Clave (KPIs)\n")
        archivo.write("- **Fuga Total de Ingresos (MRR):** $139,130.85 USD / mes ($1,669,570.20 USD anualizados).\n")
        archivo.write("- **Foco Crítico:** Contratos mes a mes de 0 a 6 meses concentran **$49,681.30 USD/mes** (35.7% de la pérdida total).\n")
        archivo.write("- **Tasa de Abandono en el Foco:** **55.2%** de abandono temprano (780 de 1,413 clientes cancelan en el primer semestre).\n")
        archivo.write("- **Nicho Más Crítico:** Fibra Óptica + Cheque Electrónico alcanza **75.5% de churn**.\n")
        archivo.write("- **ROI Proyectado de Retención:** **+1,233%** rescatando solo al 25% de los clientes en riesgo.\n\n")

        archivo.write("---\n\n")

        # Sección 1
        archivo.write("## 2. Fuga de Ingresos por Tipo de Contrato y Antigüedad\n\n")
        archivo.write("Evaluación del impacto financiero directo según la permanencia pactada y los meses de relación comercial con la empresa.\n\n")
        
        df1 = resultados.get("01_tasa_churn_contrato_antiguedad.sql")
        if df1 is not None:
            archivo.write(convertir_a_tabla_markdown(df1) + "\n\n")

        archivo.write("![Fuga Mensual de Ingresos](grafico_01_mrr_perdido_contrato.png)\n\n")
        archivo.write("### Hallazgos de la Consulta 1:\n")
        archivo.write("- **Concentración del Riesgo:** El 55.2% de los clientes en contratos mensuales se dan de baja en los primeros 6 meses.\n")
        archivo.write("- **Efecto Blindaje:** Los contratos de 1 y 2 años muestran tasas de churn inferiores al 12% y 3% respectivamente, demostrando que la permanencia contractual es el mayor escudo de retención.\n\n")

        archivo.write("---\n\n")

        # Sección 2
        archivo.write("## 3. Radiografía del Segmento Crítico: Servicios y Fricción de Pago\n\n")
        archivo.write("Filtrando exclusivamente la cohorte más vulnerable (contrato mes a mes, antigüedad $\\le$ 6 meses), analizamos la intersección de servicios de conectividad y canales de recaudación.\n\n")

        df2 = resultados.get("02_segmento_critico_riesgo.sql")
        if df2 is not None:
            archivo.write(convertir_a_tabla_markdown(df2) + "\n\n")

        archivo.write("![Segmento Crítico por Servicio y Pago](grafico_02_segmento_riesgo_pago.png)\n\n")
        archivo.write("### Hallazgos de la Consulta 2:\n")
        archivo.write("- **Fibra Óptica:** Tiene una cuota mensual más elevada (~$80-$90 USD/mes), lo que incrementa la sensibilidad al precio en los primeros meses.\n")
        archivo.write("- **Cheque Electrónico (`Electronic check`):** Es un método de pago manual no automatizado. Cada mes el cliente experimenta 'fricción de pago', evaluando conscientemente si renovar o cancelar. Esto dispara el abandono al **75.5%** (332 cancelaciones en 440 clientes).\n\n")

        archivo.write("---\n\n")

        # Sección 3
        archivo.write("## 4. Diagnóstico Causal: La Carencia de Soporte Técnico y Seguridad Online\n\n")
        archivo.write("¿Por qué se van tan rápido los clientes de fibra óptica? El análisis de servicios complementarios revela una causa operativa directa:\n\n")

        df3 = resultados.get("03_friccion_soporte_seguridad.sql")
        if df3 is not None:
            archivo.write(convertir_a_tabla_markdown(df3) + "\n\n")

        archivo.write("![Efecto Protector de Soporte y Seguridad](grafico_03_soporte_seguridad.png)\n\n")
        archivo.write("### Hallazgos de la Consulta 3:\n")
        archivo.write("- **Desamparo Técnico:** De los 780 cancelados en el segmento crítico, **593 clientes (el 76%) no contaban con Soporte Técnico ni Seguridad Online**.\n")
        archivo.write("- **Tasa de Abandono Sin Soporte:** Alcanza un dramático **69.0%**, frente a un 39.6% cuando cuentan con protección y asistencia técnica.\n\n")

        archivo.write("---\n\n")

        # Sección 4
        archivo.write("## 5. Simulación de Negocio y Retorno sobre la Inversión (ROI)\n\n")
        archivo.write("Para presentar a la dirección general, construimos un modelo financiero proyectando el impacto de una campaña automatizada de retención en el tercer mes.\n\n")

        df4 = resultados.get("04_simulacion_roi_retencion.sql")
        if df4 is not None:
            archivo.write(convertir_a_tabla_markdown(df4) + "\n\n")

        archivo.write("![Simulación Financiera y ROI](grafico_04_simulacion_roi.png)\n\n")

        archivo.write("### Propuesta Estratégica (The Retention Playbook):\n")
        archivo.write("1. **Disparador Automatizado (Día 75 / Mes 3):** Identificar a los usuarios de fibra óptica en contrato mensual que pagan por cheque electrónico y carecen de soporte técnico.\n")
        archivo.write("2. **Oferta Comercial de Retención:** Ofrecer un **15% de descuento en la factura durante 6 meses** condicionado a dos factores innegociables:\n")
        archivo.write("   - Migración a contrato con **permanencia anual** (One-year contract).\n")
        archivo.write("   - Domiciliación del pago vía **tarjeta bancaria o cuenta automática** (eliminando la fricción del cheque electrónico).\n")
        archivo.write("3. **Onboarding con Valor Agregado:** Incluir sin coste adicional durante 3 meses el paquete de **Soporte Técnico y Seguridad Web**.\n")
        archivo.write("4. **Impacto Financiero Proyectado:** Rescatando únicamente a 1 de cada 4 clientes en riesgo (25%), la compañía protege **$149,043.90 USD/año**, incurriendo en una inversión comercial de tan solo $11,178.29 USD en descuentos, arrojando un **beneficio neto de $137,865.61 USD** y un **ROI del +1,233%**.\n")

