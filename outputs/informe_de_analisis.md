# Informe Ejecutivo: Análisis Estratégico de Retención y Fuga de Ingresos

> **Autor:** David Álvarez  
> **Especialidad:** Análisis de Datos & Ingeniería Analítica  
> **Objetivo:** *Identificar con precisión quirúrgica el foco principal de pérdida de ingresos recurrentes (MRR) por abandono de clientes en telecomunicaciones y modelar una estrategia cuantitativa de retención de alto retorno.*

---

## 1. Contexto de Negocio y Pregunta Central

En la industria de suscripciones, retener a un cliente existente es considerablemente más rentable que adquirir uno nuevo. En este análisis examino el comportamiento de **7,043 clientes** de telecomunicaciones mediante SQL relacional y Python para responder a una necesidad comercial crítica:

* **Pregunta Central:** ¿Qué combinación de tipo de contrato y antigüedad concentra la mayor fuga mensual de ingresos (MRR), qué factores operativos la causan y cuál es el impacto financiero neto de una campaña de retención proactiva?

### Indicadores Clave del Negocio (KPIs)
- **Fuga Total de Ingresos (MRR):** $139,130.85 USD / mes ($1,669,570.20 USD anualizados).
- **Foco de Mayor Riesgo:** Clientes con contrato mensual y 0-6 meses de antigüedad concentran **$49,681.30 USD/mes** (el 35.7% de todas las pérdidas de la compañía).
- **Tasa de Abandono en el Foco:** **55.2%** de abandono temprano (780 bajas en 1,413 clientes nuevos).
- **Segmento Más Crítico:** Fibra Óptica + Cheque Electrónico alcanza un **75.5% de abandono**.
- **Factor Causal:** El 76% de los clientes cancelados en este segmento carecía de soporte técnico y seguridad online.
- **Retorno de Inversión (ROI Proyectado):** **+1,233.3%** rescatando al 25% de los clientes en riesgo.

---

## 2. Fuga de Ingresos por Tipo de Contrato y Antigüedad

Analizo el impacto económico mensual según el tipo de permanencia y el rango de permanencia en meses del cliente:

| tipo_contrato  | rango_antiguedad | total_clientes | clientes_cancelados | tasa_churn_pct | ingresos_mensuales_perdidos | pct_del_total_fuga |
| -------------- | ---------------- | -------------- | ------------------- | -------------- | --------------------------- | ------------------ |
| Month-to-month | 0-6 meses        | 1,413          | 780                 | 55.20          | 49,681.30                   | 35.70              |
| Month-to-month | Más de 2 años    | 1,144          | 353                 | 30.90          | 30,565.35                   | 22                 |
| Month-to-month | 1-2 años         | 737            | 278                 | 37.70          | 21,980.30                   | 15.80              |
| Month-to-month | 7-12 meses       | 581            | 244                 | 42             | 18,620.15                   | 13.40              |
| One year       | Más de 2 años    | 1,152          | 137                 | 11.90          | 12,364.30                   | 8.90               |
| Two year       | Más de 2 años    | 1,537          | 48                  | 3.10           | 4,165.30                    | 3                  |
| One year       | 1-2 años         | 197            | 16                  | 8.10           | 1,101.35                    | 0.80               |
| One year       | 7-12 meses       | 85             | 9                   | 10.60          | 438                         | 0.30               |
| One year       | 0-6 meses        | 39             | 4                   | 10.30          | 214.80                      | 0.20               |
| Two year       | 0-6 meses        | 29             | 0                   | 0              | 0                           | 0                  |
| Two year       | 1-2 años         | 90             | 0                   | 0              | 0                           | 0                  |
| Two year       | 7-12 meses       | 39             | 0                   | 0              | 0                           | 0                  |

![Fuga Mensual de Ingresos](grafico_01_mrr_perdido_contrato.png)

### Conclusiones de este Paso:
- **Concentración Crítica:** Más de un tercio de las pérdidas de dinero de la compañía proviene de usuarios sin permanencia en su primer semestre.
- **Efecto Blindaje de la Permanencia:** En contratos anuales y bianuales, el abandono cae por debajo del 12% y 3% respectivamente, demostrando que asegurar la permanencia es el mecanismo de retención más sólido.

---

## 3. Radiografía del Segmento Crítico: Servicios y Canal de Pago

Aislando exclusivamente la cohorte vulnerable (contrato mes a mes y $\le$ 6 meses), profundizo en el cruce de conectividad y método de facturación:

| servicio_internet | metodo_pago               | total_clientes | cancelaciones | tasa_churn_pct | mrr_perdido_segmento | cuota_mensual_promedio |
| ----------------- | ------------------------- | -------------- | ------------- | -------------- | -------------------- | ---------------------- |
| Fiber optic       | Electronic check          | 440            | 332           | 75.50          | 26,920.80            | 80.80                  |
| DSL               | Electronic check          | 209            | 119           | 56.90          | 5,213.10             | 45.63                  |
| DSL               | Mailed check              | 192            | 87            | 45.30          | 3,964.40             | 45.97                  |
| Fiber optic       | Mailed check              | 96             | 60            | 62.50          | 4,731.40             | 79.36                  |
| No                | Mailed check              | 216            | 57            | 26.40          | 1,144.85             | 20.26                  |
| Fiber optic       | Bank transfer (automatic) | 41             | 38            | 92.70          | 3,098.65             | 81.59                  |
| Fiber optic       | Credit card (automatic)   | 42             | 29            | 69             | 2,399.30             | 80.81                  |
| DSL               | Credit card (automatic)   | 52             | 21            | 40.40          | 1,006.15             | 49.71                  |
| DSL               | Bank transfer (automatic) | 42             | 18            | 42.90          | 816                  | 48.84                  |
| No                | Electronic check          | 31             | 9             | 29             | 179.35               | 20.05                  |
| No                | Bank transfer (automatic) | 27             | 7             | 25.90          | 146.75               | 20.24                  |
| No                | Credit card (automatic)   | 25             | 3             | 12             | 60.55                | 20.11                  |

![Segmento Crítico por Servicio y Pago](grafico_02_segmento_riesgo_pago.png)

### Conclusiones de este Paso:
- **Impacto de la Tarifa de Fibra:** La fibra óptica tiene tarifas más altas (~$80-$90 USD/mes), lo que incrementa la sensibilidad al precio en los primeros meses.
- **Fricción del Cheque Electrónico (`Electronic check`):** Al no ser automático, cada mes el usuario debe tomar la decisión consciente de abonar la factura, lo que propicia la cancelación inmediata. El resultado: un **75.5% de abandono** (332 bajas en 440 clientes).

---

## 4. Diagnóstico Causal: La Carencia de Asistencia Técnica y Ciberseguridad

Al evaluar la adopción de servicios complementarios en este grupo vulnerable, identifico la causa operativa de fondo:

| estado_soporte_tecnico | estado_seguridad_online | total_clientes | clientes_cancelados | tasa_churn_pct | mrr_perdido |
| ---------------------- | ----------------------- | -------------- | ------------------- | -------------- | ----------- |
| Sin Soporte Técnico    | Sin Seguridad Online    | 860            | 593                 | 69             | 40,638.40   |
| Sin Internet           | Sin Internet            | 299            | 76                  | 25.40          | 1,531.50    |
| Con Soporte Técnico    | Sin Seguridad Online    | 116            | 56                  | 48.30          | 4,004.80    |
| Sin Soporte Técnico    | Con Seguridad Online    | 106            | 42                  | 39.60          | 2,684.50    |
| Con Soporte Técnico    | Con Seguridad Online    | 32             | 13                  | 40.60          | 822.10      |

![Efecto Protector de Soporte y Seguridad](grafico_03_soporte_seguridad.png)

### Conclusiones de este Paso:
- **Vulnerabilidad Técnica Inicial:** De los 780 clientes fugados, **593 usuarios (el 76%) no contaban con Soporte Técnico ni Seguridad Online**.
- Quienes carecen de soporte sufren un **69.0% de churn**, mientras que quienes tienen ambos servicios ven reducida la tasa a casi la mitad.

---

## 5. Modelo Financiero y Retorno sobre la Inversión (ROI)

Para sustentar la propuesta ante la dirección, construyo una simulación financiera con CTEs evaluando el rescate del 25% de los clientes en riesgo:

| clientes_perdidos_historicos | mrr_perdido_mensual | fuga_ingresos_anuales | meta_clientes_rescatados_25pct | ingreso_anual_protegido | coste_inversion_campana | beneficio_neto_anual_recuperado | roi_campana_pct |
| ---------------------------- | ------------------- | --------------------- | ------------------------------ | ----------------------- | ----------------------- | ------------------------------- | --------------- |
| 780                          | 49,681.30           | 596,175.60            | 195                            | 149,043.90              | 11,178.29               | 137,865.61                      | 1,233.30        |

![Simulación Financiera y ROI](grafico_04_simulacion_roi.png)

### Mi Propuesta de Acción (The Retention Strategy):
1. **Disparador Automatizado (Día 75 / Mes 3):** Identifico en el CRM a los usuarios de fibra óptica en contrato mensual que pagan con cheque electrónico y no tienen soporte técnico.
2. **Incentivo Vinculado:** Ofrezco un **15% de descuento durante 6 meses** condicionado a dos condiciones comerciales:
   - Aceptación de un **contrato de permanencia anual (One-year contract)**.
   - Domiciliación del cobro mediante **tarjeta bancaria o cuenta bancaria automática** (eliminando la fricción mensual del cheque electrónico).
3. **Kit de Onboarding y Fidelización:** Incluyo durante los primeros 3 meses el servicio de **Soporte Técnico y Seguridad Web** sin coste adicional para reducir la fricción de instalación.
4. **Rentabilidad Neta:** Con una meta prudente de rescatar solo a 1 de cada 4 clientes en riesgo (25%), protejo **$149,043.90 USD/año**, invirtiendo apenas $11,178.29 USD en descuentos, lo que genera un **beneficio neto de $137,865.61 USD** y un **ROI del +1,233.3%**.
