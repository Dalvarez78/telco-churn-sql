# 📉 Análisis Estratégico de Retención de Clientes (Telco Customer Churn con SQL)

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0+-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![SQL](https://img.shields.io/badge/SQL-Advanced%20CTEs%20%26%20Aggregations-E38C00.svg?logo=postgresql&logoColor=white)](https://en.wikipedia.org/wiki/SQL)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Seaborn & Matplotlib](https://img.shields.io/badge/DataViz-Matplotlib%20%7C%20Seaborn-2B2D42.svg)](https://seaborn.pydata.org/)
[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-green.svg)](LICENSE)

En este proyecto analizo el comportamiento y la telemetría de **7,043 clientes** de una compañía de telecomunicaciones con el objetivo de **identificar los segmentos críticos que concentran la fuga recurrente de ingresos (MRR)**, aislar las causas operativas del abandono y diseñar un plan cuantitativo de retención temprana con simulación financiera de retorno de inversión (ROI).

---

## 📌 1. Planteamiento del Problema y Pregunta Central

En los modelos de negocio por suscripción, el coste de adquisición de clientes (CAC) supera con creces el coste de retención. Cuando un cliente se da de baja prematuramente, se destruye el valor del ciclo de vida del cliente (*Customer Lifetime Value - LTV*) y las inversiones iniciales de instalación y captación quedan sin amortizar.

* **Conjunto de Datos:** Telemetría de 7,043 clientes con 21 variables sobre servicios de internet, soporte, modalidad de contrato, métodos de facturación y bajas.
* **Pregunta Central de Negocio:**
  > *¿Qué combinación de permanencia contractual y antigüedad concentra las mayores pérdidas mensuales de ingresos por abandono (MRR), qué factores operativos y de servicio la aceleran, y cuál es el impacto financiero neto de una campaña de retención proactiva?*

---

## 📊 2. Cuadro de Mando Ejecutivo (KPIs Principales)

| Métrica Clave | Valor Observado | Impacto en el Negocio |
| :--- | :--- | :--- |
| **Pérdida Total de Ingresos (MRR)** | **$139,130.85 USD / mes** | Representa **$1,669,570.20 USD anuales** en ingresos destruidos. |
| **Foco Crítico de Concentración** | **Month-to-month $\le$ 6 meses** | Concentra el **35.7% de toda la fuga económica** de la empresa ($49,681.30 USD/mes). |
| **Tasa de Abandono en el Foco** | **55.2% de churn** | Más de la mitad de los clientes nuevos sin permanencia cancelan en el primer semestre. |
| **Segmento Más Vulnerable** | **Fibra Óptica + Cheque Electrónico** | Alcanza un **75.5% de abandono** (332 cancelaciones en 440 clientes). |
| **Factor Protector Causal** | **Soporte Técnico + Seguridad Online** | Clientes sin estos servicios sufren **69.0% de churn** vs 39.6% cuando cuentan con ellos. |
| **ROI Proyectado de Retención** | **+1,233.3%** | Rescatar solo al 25% de los clientes en riesgo genera **$137,865.61 USD de beneficio neto** en el Año 1. |

---

## 📈 3. Visualizaciones y Hallazgos Principales

### 🔍 1. Fuga de Ingresos por Tipo de Contrato y Antigüedad
Al evaluar la distribución de la pérdida económica, compruebo que la modalidad contractual es la variable determinante del abandono. Mientras que los contratos de 1 y 2 años presentan deserciones mínimas (menores al 12% y 3%), los contratos mes a mes (**Month-to-month**) concentran casi la totalidad de las cancelaciones. Dentro de este grupo, **los primeros 6 meses representan la zona crítica**, costándole a la empresa casi **$50,000 USD mensuales**.

![Fuga Mensual por Contrato y Antigüedad](outputs/grafico_01_mrr_perdido_contrato.png)

---

### 🔍 2. Fricción en el Canal de Pago y Sensibilidad al Precio
Al diseccionar el segmento crítico (0 a 6 meses sin permanencia), analizo el cruce entre conectividad y método de cobro:
- **Fibra Óptica:** Presenta una cuota mensual más elevada (~$80-$90 USD/mes).
- **Cheque Electrónico (`Electronic check`):** Es un método manual no domiciliado que exige al usuario una gestión activa cada mes. La combinación de tarifa alta y fricción de pago dispara el abandono al **75.5%**.

![Segmento Crítico por Servicio y Pago](outputs/grafico_02_segmento_riesgo_pago.png)

---

### 🔍 3. Diagnóstico Causal: La Carencia de Asistencia y Seguridad
De los 780 clientes que cancelaron en el segmento crítico, **593 usuarios (el 76%) carecían de Soporte Técnico y de Seguridad Online**. La falta de acompañamiento técnico inicial acelera la frustración ante problemas de configuración y facilita la baja prematura.

![Efecto Protector de Soporte y Seguridad](outputs/grafico_03_soporte_seguridad.png)

---

### 🔍 4. Simulación Financiera y Retorno de Inversión (+1,233% ROI)
Diseñé un modelo financiero en SQL (usando CTEs) para proyectar el impacto económico de una campaña de retención proactiva en el tercer mes, asumiendo una tasa de efectividad conservadora del 25%:

- **Ingresos Anuales Protegidos (25% clientes rescatados):** $149,043.90 USD.
- **Inversión en la Campaña (15% descuento x 6 meses):** $11,178.29 USD.
- **Beneficio Neto Año 1:** **$137,865.61 USD**.
- **Retorno sobre la Inversión (ROI):** **+1,233.3%**.

![Simulación ROI](outputs/grafico_04_simulacion_roi.png)

---

## 🎯 4. Estrategia de Retención Propuesta

Con base en la evidencia cuantitativa, desarrollo una estrategia estructurada en tres fases:

1. **Disparador Automatizado (Día 75 / Mes 3):**
   - Configuración de una alerta en el CRM para clientes de fibra óptica en contratos mensuales que pagan por cheque electrónico y llevan entre 60 y 75 días en la compañía.
2. **Oferta Comercial Condicionada:**
   - Oferta de un **15% de descuento durante 6 meses**, vinculada obligatoriamente a:
     - Migración a un **contrato de permanencia anual (One-year contract)**.
     - Domiciliación del cobro mediante **tarjeta bancaria o débito automático en cuenta**.
3. **Onboarding de Alto Valor:**
   - Incorporación bonificada durante los primeros 3 meses del servicio de **Soporte Técnico y Seguridad Web** para blindar la experiencia durante la fase de instalación.

---

## 📁 5. Estructura del Proyecto

El repositorio está organizado de forma modular, separando la ingeniería de datos, las consultas analíticas y los reportes:

```text
telco-churn-sql/
│
├── .gitignore                                 # Exclusiones para Python, SQLite y Jupyter
├── LICENSE                                    # Licencia abierta MIT
├── README.md                                  # Documentación técnica y ejecutiva
├── INFORME_EJECUTIVO.md                       # Informe estratégico detallado del análisis
├── requirements.txt                           # Dependencias del proyecto
├── contexto_del_proyecto_sql.md               # Contexto y requerimientos de partida
│
├── data/
│   ├── WA_Fn-UseC_-Telco-Customer-Churn.csv   # Dataset de 7,043 clientes
│   └── telco_churn.db                         # Base de datos relacional SQLite indexada
│
├── queries/                                   # Consultas SQL analíticas comentadas
│   ├── 01_tasa_churn_contrato_antiguedad.sql  # Consulta 1: Tasa de abandono y MRR perdido
│   ├── 02_segmento_critico_riesgo.sql         # Consulta 2: Segmento de mayor riesgo
│   ├── 03_friccion_soporte_seguridad.sql      # Consulta 3: Diagnóstico causal (soporte y seguridad)
│   └── 04_simulacion_roi_retencion.sql        # Consulta 4: Modelo financiero y ROI con CTEs
│
├── src/                                       # Código fuente modular en Python
│   ├── __init__.py                            # Inicializador del paquete
│   ├── cargar_datos.py                        # Pipeline ETL: Limpieza, tipado e índices SQLite
│   ├── ejecutar_analisis.py                   # Ejecución SQL automatizada y exportación de métricas
│   └── generar_visualizaciones.py             # Generación de visualizaciones ejecutivas (300 DPI)
│
├── outputs/                                   # Artefactos y métricas generadas
│   ├── 01_tasa_churn_contrato_antiguedad.csv
│   ├── 02_segmento_critico_riesgo.csv
│   ├── 03_friccion_soporte_seguridad.csv
│   ├── 04_simulacion_roi_retencion.csv
│   ├── grafico_01_mrr_perdido_contrato.png
│   ├── grafico_02_segmento_riesgo_pago.png
│   ├── grafico_03_soporte_seguridad.png
│   ├── grafico_04_simulacion_roi.png
│   └── informe_de_analisis.md                 # Informe consolidado exportado
│
├── analisis_sql.ipynb                         # Cuaderno Jupyter paso a paso con SQL interactivo
├── cargar_datos.py                            # Wrapper de ejecución rápida en la raíz
├── ejecutar_analisis.py                       # Wrapper de ejecución rápida en la raíz
├── load_data.py                               # Wrapper de compatibilidad
└── run_analysis.py                            # Wrapper de compatibilidad
```

---

## 🛠️ 6. Instalación y Reproducción Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/Dalvarez78/telco-churn-sql.git
cd telco-churn-sql
```

### 2. Configurar entorno virtual e instalar librerías
```bash
# En Windows (PowerShell)
python -m venv .venv
.venv\Scripts\activate

# En Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Ejecutar el pipeline analítico completo
El análisis completo se reproduce con dos comandos:

```bash
# Paso 1: Ingesta, limpieza y creación de índices en SQLite
python cargar_datos.py

# Paso 2: Ejecución de consultas SQL, exportación de CSVs y generación de gráficos
python ejecutar_analisis.py
```

*Para explorar el análisis interactivo celda por celda en Jupyter:*
```bash
jupyter notebook analisis_sql.ipynb
```

---

## 📄 7. Documentación Complementaria

* Consulta el [INFORME_EJECUTIVO.md](INFORME_EJECUTIVO.md) para un desglose detallado de las implicaciones comerciales, análisis cuantitativo y metodología.
* Revisa el cuaderno interactivo [analisis_sql.ipynb](analisis_sql.ipynb) para ver cada consulta SQL con sus tablas y visualizaciones asociadas.

---

## 👤 Autor

* **David Álvarez** — [GitHub (@Dalvarez78)](https://github.com/Dalvarez78)
* **Licencia:** Distribuido bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.
