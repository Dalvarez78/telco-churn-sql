-- ============================================================================
-- Consulta 2: Profundización en el Segmento Crítico de Mayor Riesgo
-- Filtro: Contratos mensuales (Month-to-month) con antigüedad <= 6 meses.
-- Objetivo: Identificar qué servicios de internet y métodos de pago impulsan
--           el mayor volumen y porcentaje de cancelación en clientes nuevos.
-- ============================================================================

SELECT 
    InternetService AS servicio_internet,
    PaymentMethod AS metodo_pago,
    COUNT(*) AS total_clientes,
    COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) AS cancelaciones,
    ROUND(100.0 * COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) / COUNT(*), 1) AS tasa_churn_pct,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS mrr_perdido_segmento,
    ROUND(AVG(MonthlyCharges), 2) AS cuota_mensual_promedio
FROM telco_churn
WHERE Contract = 'Month-to-month' 
  AND tenure <= 6
GROUP BY 1, 2
ORDER BY cancelaciones DESC, tasa_churn_pct DESC;

