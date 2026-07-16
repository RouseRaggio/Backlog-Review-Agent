## ADDED Requirements

### Requirement: Generación de reporte HTML
El sistema SHALL generar un reporte HTML autocontenido (sin dependencias externas de red).
El reporte SHALL incluir: BQS general, desglose por regla, desglose por issue, lista de issues con reglas falladas.
El reporte SHALL incluir resumen ejecutivo con BQS, total de issues evaluados, reglas aplicadas y fecha del análisis.

#### Scenario: Generación de reporte exitosa
- **WHEN** se completa la evaluación de calidad
- **THEN** el sistema genera un archivo HTML en la ruta configurada

#### Scenario: Reporte con datos vacíos
- **WHEN** no hay issues para evaluar
- **THEN** el reporte muestra un mensaje indicando que no hay datos

### Requirement: Visualización del reporte
El reporte SHALL mostrar el BQS con indicador visual de color según umbral.
El reporte SHALL mostrar tabla de issues con su puntuación individual y reglas falladas.
El reporte SHALL mostrar gráfico de barras con puntuación por regla.
El reporte SHALL ser responsivo y legible en navegadores modernos.

#### Scenario: Visualización de BQS
- **WHEN** se genera el reporte con BQS 85
- **THEN** el BQS se muestra con indicador visual verde y el valor numérico

#### Scenario: Tabla de issues
- **WHEN** se genera el reporte con 10 issues evaluados
- **THEN** el reporte muestra una tabla con los 10 issues, su puntuación y reglas falladas
