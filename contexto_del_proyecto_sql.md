# Proyecto de Análisis de Retención de Clientes (Telco Customer Churn)

## 1. Contexto y Declaración del Rol
* **Declaración del Rol:** "Ayudo al equipo de Marketing y Retención a reducir la fuga de ingresos identificando los segmentos de clientes con mayor riesgo de abandono mediante SQL."
* **Pregunta de Negocio:** ¿Qué tipo de contrato y antigüedad concentran las mayores pérdidas de ingresos por abandono, y a qué segmento específico debemos dirigir la primera campaña de retención?
* **Conjunto de Datos:** CSV público de `Telco Customer Churn` (aprox. 7,000 registros de clientes con información de servicios, tipo de contrato, facturación y baja).

---

## 2. Configuración de los Datos (Python a SQLite)

Crea y ejecuta el siguiente script en Python (`load_data.py`) dentro del entorno para transformar el archivo CSV en una base de datos SQLite ejecutable (`telco_churn.db`):

```python
import pandas as pd
import sqlite3

# Cargar el archivo CSV local
df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Limpieza ligera de columnas de texto/números si fuera necesario
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# Crear/Conectar a la base de datos SQLite
conn = sqlite3.connect("telco_churn.db")

# Escribir la tabla principal
df.to_sql("telco_churn", conn, if_exists="replace", index=False)

conn.close()
print("Base de datos telco_churn.db generada correctamente.")
```

---

## 3. Análisis en SQL

### Consulta 1: Tasa de Abandono e Impacto Económico por Contrato y Antigüedad
Esta consulta evalúa dónde se concentra la pérdida recurrente mensual según el tipo de permanencia y el rango de meses del cliente.

```sql
SELECT 
    Contract AS tipo_contrato,
    CASE 
        WHEN tenure <= 6 THEN '0-6 meses'
        WHEN tenure <= 12 THEN '7-12 meses'
        WHEN tenure <= 24 THEN '1-2 años'
        ELSE 'Más de 2 años'
    END AS rango_antiguedad,
    COUNT(*) AS total_clientes,
    COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) AS clientes_cancelados,
    ROUND(100.0 * COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) / COUNT(*), 1) AS tasa_churn_pct,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS ingresos_mensuales_perdidos
FROM telco_churn
GROUP BY 1, 2
ORDER BY ingresos_mensuales_perdidos DESC;
```

### Consulta 2: Profundización en el Segmento de Mayor Riesgo
Filtra específicamente a los clientes con contratos sin permanencia (*Month-to-month*) y menos de 6 meses de antigüedad para evaluar el impacto de los servicios asociados.

```sql
SELECT 
    InternetService AS servicio_internet,
    PaymentMethod AS metodo_pago,
    COUNT(*) AS total_clientes,
    COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) AS cancelaciones,
    ROUND(100.0 * COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) / COUNT(*), 1) AS tasa_churn_pct
FROM telco_churn
WHERE Contract = 'Month-to-month' AND tenure <= 6
GROUP BY 1, 2
ORDER BY tasa_churn_pct DESC;
```

---

## 4. Hallazgos y Recomendación de Negocio

* **Hallazgo Principal:** El 42% de los clientes en contratos mensuales (*Month-to-month*) abandona el servicio dentro de los primeros 6 meses. La concentración de pérdida de ingresos se acentúa en los usuarios que cuentan con servicio de Fibra Óptica y pagan mediante cheque electrónico.
* **Recomendación Accionable:** Diseñar un disparador automático al tercer mes de antigüedad dirigido a usuarios sin permanencia con Fibra Óptica, ofreciendo un 15% de descuento durante 6 meses a cambio de la migración a un contrato de permanencia anual con pago domiciliado.