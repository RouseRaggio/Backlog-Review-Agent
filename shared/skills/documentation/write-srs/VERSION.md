# IEEE 29148 - Guía para la Elaboración de un Software Requirements Specification (SRS)

> **Propósito**
>
> Este documento resume las prácticas recomendadas inspiradas en el estándar IEEE 29148 para la elaboración de un Software Requirements Specification (SRS). Su objetivo es servir como guía para los agentes de IA de la plataforma AI-QA-Agents al momento de redactar especificaciones de requisitos de software.

---

# Objetivo del SRS

Un Software Requirements Specification (SRS) describe **qué necesita el negocio** y **qué debe hacer el sistema**, sin definir cómo será implementado.

El SRS es la fuente oficial de requisitos para:

- Product Owners
- Business Analysts
- Arquitectos
- Desarrolladores
- QA
- Stakeholders

Debe ser suficientemente completo para permitir el diseño de la solución sin necesidad de realizar preguntas adicionales sobre el negocio.

---

# Qué debe contener un SRS

Como mínimo el documento debe incluir:

1. Introducción
2. Propósito
3. Alcance
4. Contexto del negocio
5. Problema actual
6. Objetivos del sistema
7. Stakeholders
8. Actores
9. Descripción general
10. Requisitos funcionales
11. Requisitos no funcionales
12. Reglas de negocio
13. Casos de uso
14. Restricciones
15. Supuestos
16. Dependencias
17. Riesgos
18. Entradas
19. Salidas
20. Criterios de aceptación
21. Métricas
22. Glosario

---

# Qué NO debe contener un SRS

El SRS NO debe incluir información de implementación.

No debe mencionar:

- Lenguajes de programación
- Frameworks
- Librerías
- APIs
- Bases de datos
- Arquitectura
- Patrones de diseño
- Microservicios
- Docker
- Kubernetes
- Clases
- Interfaces
- Repositorios
- Servicios

Toda esta información pertenece al Software Design Description (SDD).

---

# Características de un buen requisito

Todo requisito debe ser:

## Correcto

Debe representar una necesidad real del negocio.

---

## Completo

Debe contener toda la información necesaria para comprender el requisito.

---

## Consistente

No debe contradecir otros requisitos.

---

## No ambiguo

Debe tener una única interpretación posible.

Evitar palabras como:

- quizás
- probablemente
- normalmente
- aproximadamente
- generalmente

---

## Verificable

Debe poder comprobarse mediante pruebas o inspección.

Ejemplo:

Correcto

> El sistema deberá generar un reporte PDF.

Incorrecto

> El sistema generará un reporte atractivo.

---

## Necesario

Cada requisito debe aportar valor al negocio.

---

## Factible

Debe poder implementarse dentro de las restricciones del proyecto.

---

## Trazable

Debe poder relacionarse con:

- Objetivos
- Casos de uso
- Reglas de negocio
- Pruebas

---

# Redacción recomendada

Utilizar siempre lenguaje imperativo.

Ejemplos

Correcto

> El sistema deberá permitir seleccionar un proyecto.

Correcto

> El sistema deberá validar la prioridad del Issue.

Incorrecto

> El sistema podría seleccionar un proyecto.

Incorrecto

> Sería conveniente validar la prioridad.

---

# Requisitos Funcionales

Los requisitos funcionales describen los servicios o comportamientos que el sistema debe ofrecer.

Ejemplo

RF-001

El sistema deberá permitir seleccionar un proyecto de Jira para iniciar una auditoría.

---

RF-002

El sistema deberá analizar automáticamente todos los elementos del backlog.

---

# Requisitos No Funcionales

Los requisitos no funcionales describen atributos de calidad del sistema.

Pueden clasificarse en:

- Rendimiento
- Seguridad
- Disponibilidad
- Escalabilidad
- Mantenibilidad
- Configuración
- Observabilidad
- Compatibilidad
- Portabilidad
- Usabilidad

Ejemplo

RNF-001

El sistema deberá procesar un backlog de hasta 1000 Issues en menos de cinco minutos.

---

# Reglas de Negocio

Las reglas de negocio representan políticas o restricciones propias de la organización.

Ejemplo

RN-001

Toda Historia de Usuario deberá pertenecer a una Epic.

RN-002

Todo Bug deberá incluir pasos para reproducir el problema.

---

# Casos de Uso

Cada caso de uso debe contener:

- Nombre
- Objetivo
- Actor
- Precondiciones
- Flujo principal
- Flujos alternativos
- Excepciones
- Postcondiciones

---

# Buenas prácticas

Antes de finalizar el SRS verificar:

- Existe un propósito claro.
- El problema del negocio está definido.
- Todos los Stakeholders fueron identificados.
- Los requisitos están numerados.
- No existen duplicados.
- No existen contradicciones.
- Todos los requisitos son verificables.
- No hay ambigüedades.
- No se describe la implementación.
- Existe trazabilidad entre objetivos y requisitos.

---

# Errores comunes

No confundir:

SRS

↓

Qué necesita el negocio.

---

SDD

↓

Cómo será construido el sistema.

---

Código

↓

Cómo funciona la implementación.

---

# Relación con Specification-Driven Development

El flujo recomendado es:

Problema del Negocio

↓

SRS

↓

Aprobación

↓

SDD

↓

Implementación

↓

Pruebas

---

# Convenciones de Numeración

Requisitos Funcionales

RF-001

RF-002

RF-003

...

---

Requisitos No Funcionales

RNF-001

RNF-002

RNF-003

...

---

Reglas de Negocio

RN-001

RN-002

RN-003

...

---

Casos de Uso

CU-001

CU-002

CU-003

...

---

# Objetivo Final

El SRS debe permitir que un Arquitecto de Software diseñe completamente el sistema sin necesidad de solicitar información adicional sobre el negocio.

Si el Arquitecto necesita hacer preguntas para comprender el problema, el SRS aún no está completo.