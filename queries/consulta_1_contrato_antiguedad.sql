-- ==============================================================================
-- Consulta 1: Tasa de Abandono e Impacto Económico por Contrato y Antigüedad
-- Autor: Estudiante de Análisis de Datos
-- Objetivo: Analizo dónde se concentra la mayor pérdida mensual de ingresos según
-- el tipo de contrato y la permanencia del cliente en la empresa.
-- ==============================================================================

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

