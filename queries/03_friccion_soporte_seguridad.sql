-- ============================================================================
-- Consulta 3: Diagnóstico Causal - Carencia de Soporte Técnico y Ciberseguridad
-- Filtro: Contratos mensuales (Month-to-month) con antigüedad <= 6 meses.
-- Objetivo: Evaluar si los clientes que no cuentan con soporte técnico y seguridad
--           sufren mayor propensión al abandono, justificando paquetes de bienvenida.
-- ============================================================================

SELECT 
    CASE 
        WHEN TechSupport = 'Yes' THEN 'Con Soporte Técnico'
        WHEN TechSupport = 'No' THEN 'Sin Soporte Técnico'
        ELSE 'Sin Internet'
    END AS estado_soporte_tecnico,
    CASE 
        WHEN OnlineSecurity = 'Yes' THEN 'Con Seguridad Online'
        WHEN OnlineSecurity = 'No' THEN 'Sin Seguridad Online'
        ELSE 'Sin Internet'
    END AS estado_seguridad_online,
    COUNT(*) AS total_clientes,
    COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) AS clientes_cancelados,
    ROUND(100.0 * COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) / COUNT(*), 1) AS tasa_churn_pct,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS mrr_perdido
FROM telco_churn
WHERE Contract = 'Month-to-month' 
  AND tenure <= 6
GROUP BY 1, 2
ORDER BY clientes_cancelados DESC;

