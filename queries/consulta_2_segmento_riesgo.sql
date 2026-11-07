-- ==============================================================================
-- Consulta 2: Profundización en el Segmento de Mayor Riesgo
-- Autor: Estudiante de Análisis de Datos
-- Objetivo: Filtro el grupo más crítico que identifiqué (clientes mes a mes con
-- menos de 6 meses) y cruzo su tipo de internet y método de pago para hallar el foco.
-- ==============================================================================

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

