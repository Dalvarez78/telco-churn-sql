-- ============================================================================
-- Consulta 1: Tasa de Abandono e Impacto Económico por Contrato y Antigüedad
-- Objetivo: Determinar qué combinación de permanencia contractual y meses
--           de antigüedad concentra la mayor fuga recurrente mensual (MRR).
-- ============================================================================

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
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS ingresos_mensuales_perdidos,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END) / 
          (SELECT SUM(MonthlyCharges) FROM telco_churn WHERE Churn = 'Yes'), 1) AS pct_del_total_fuga
FROM telco_churn
GROUP BY 1, 2
ORDER BY ingresos_mensuales_perdidos DESC;

