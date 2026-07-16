# Configuración

Este directorio contiene la configuración del Backlog Review Agent.

## Archivos

- `config.example.yaml` — Configuración de ejemplo con valores documentados.
- `config.yaml` — (opcional) Configuración personalizada del entorno local.

## Variables de entorno

Las siguientes variables de entorno son leídas desde un archivo `.env`:

| Variable         | Descripción                     | Obligatoria |
|------------------|---------------------------------|-------------|
| `JIRA_URL`       | URL base de la instancia Jira   | Sí          |
| `JIRA_EMAIL`     | Correo electrónico de autenticación | Sí      |
| `JIRA_API_TOKEN` | Token de API de Jira            | Sí          |
