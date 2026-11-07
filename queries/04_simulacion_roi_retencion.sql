-- ============================================================================
-- Consulta 4: Simulación de Negocio, Impacto Financiero y ROI de Retención
-- Objetivo: Proyectar el retorno sobre la inversión (ROI) de la campaña de
--           retención propuesta (15% de descuento durante 6 meses al migrar
--           a contrato de permanencia anual con domiciliación de pago).
-- ============================================================================

WITH metricas_segmento_critico AS (
    SELECT 
        COUNT(*) AS clientes_totales_cohorte,
        COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) AS clientes_fugados,
        SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END) AS mrr_perdido_mensual,
        AVG(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE NULL END) AS cuota_mensual_promedio
    FROM telco_churn
    WHERE Contract = 'Month-to-month' 
      AND tenure <= 6
)
SELECT 
    clientes_fugados AS clientes_perdidos_historicos,
    ROUND(mrr_perdido_mensual, 2) AS mrr_perdido_mensual,
    ROUND(mrr_perdido_mensual * 12, 2) AS fuga_ingresos_anuales,
    
    -- Hipótesis de Retención: Meta alcanzable del 25% de rescate de clientes
    CAST(ROUND(clientes_fugados * 0.25) AS INT) AS meta_clientes_rescatados_25pct,
    ROUND(mrr_perdido_mensual * 0.25 * 12, 2) AS ingreso_anual_protegido,
    
    -- Coste de inversión de la campaña: 15% de descuento durante 6 meses sobre los clientes retenidos
    ROUND((clientes_fugados * 0.25) * (cuota_mensual_promedio * 0.15) * 6, 2) AS coste_inversion_campana,
    
    -- Beneficio Neto estimado para la compañía en el Año 1
    ROUND((mrr_perdido_mensual * 0.25 * 12) - 
          ((clientes_fugados * 0.25) * (cuota_mensual_promedio * 0.15) * 6), 2) AS beneficio_neto_anual_recuperado,
          
    -- Retorno sobre la Inversión (ROI %)
    ROUND((((mrr_perdido_mensual * 0.25 * 12) - 
            ((clientes_fugados * 0.25) * (cuota_mensual_promedio * 0.15) * 6)) / 
           ((clientes_fugados * 0.25) * (cuota_mensual_promedio * 0.15) * 6)) * 100, 1) AS roi_campana_pct
FROM metricas_segmento_critico;
