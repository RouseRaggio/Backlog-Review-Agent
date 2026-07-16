## ADDED Requirements

### Requirement: Conexión a Jira Cloud
El sistema SHALL conectarse a Jira Cloud utilizando autenticación por token API.
El sistema SHALL permitir configurar la URL del sitio, el email y el token API.
El sistema SHALL validar la conexión antes de ejecutar cualquier consulta.

#### Scenario: Conexión exitosa
- **WHEN** se proporcionan credenciales válidas (URL, email, token)
- **THEN** el sistema establece conexión exitosa con Jira Cloud

#### Scenario: Credenciales inválidas
- **WHEN** se proporcionan credenciales inválidas
- **THEN** el sistema lanza un error de autenticación con mensaje descriptivo

#### Scenario: Timeout de conexión
- **WHEN** Jira Cloud no responde dentro del tiempo límite
- **THEN** el sistema lanza un error de timeout con mensaje descriptivo

### Requirement: Ejecución de consultas JQL
El sistema SHALL ejecutar consultas JQL contra Jira Cloud y retornar los resultados paginados.
El sistema SHALL soportar paginación automática para recuperar todos los resultados.
El sistema SHALL permitir configurar el tamaño de página.

#### Scenario: Consulta JQL exitosa
- **WHEN** se ejecuta una consulta JQL válida
- **THEN** el sistema retorna la lista completa de issues que coinciden con la consulta

#### Scenario: Consulta JQL sin resultados
- **WHEN** la consulta JQL no coincide con ningún issue
- **THEN** el sistema retorna una lista vacía

#### Scenario: Paginación automática
- **WHEN** la consulta JQL retorna más issues que el tamaño de página configurado
- **THEN** el sistema recupera automáticamente todas las páginas hasta obtener el conjunto completo

### Requirement: Manejo de errores de conexión
El sistema SHALL reintentar la conexión ante errores transitorios (timeout, 429, 5xx).
El sistema SHALL registrar errores de conexión con nivel de detalle configurable.

#### Scenario: Reintento ante error 429
- **WHEN** Jira responde con HTTP 429 (too many requests)
- **THEN** el sistema espera el tiempo indicado en el header Retry-After y reintenta

#### Scenario: Error permanente
- **WHEN** Jira responde con HTTP 401 o 403
- **THEN** el sistema lanza un error de autenticación sin reintentar
