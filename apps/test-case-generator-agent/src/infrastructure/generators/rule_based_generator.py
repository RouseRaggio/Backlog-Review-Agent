"""
Infrastructure: RuleBasedTestCaseGenerator

Generador determinista y trazable de casos de prueba basado en evidencia explícita.
Cumple estrictamente con el principio 'NO INVENTAR':
- No asume reglas de negocio ni validaciones no especificadas en la entrada.
- Solo genera casos límite cuando existen números, rangos o umbrales explícitos.
- Solo genera casos negativos cuando existen cláusulas explícitas de restricción/unicidad/obligatoriedad.
"""

from __future__ import annotations

import re
from typing import Optional

from src.domain.entities import (
    AcceptanceCriterion,
    GenerationOptions,
    TestCase,
    UserStory,
)
from src.domain.enums import (
    Category,
    Confidence,
    Priority,
    Status,
    TestCaseType,
)
from src.domain.services import TestCaseGenerator


class RuleBasedTestCaseGenerator(TestCaseGenerator):
    """
    Motor determinista de generación de Casos de Prueba.
    """

    # Patrones para detección de evidencia
    UNIQUENESS_PATTERN = re.compile(
        r"(únic[oa]|unic[oa]|no\s+duplicad[oa]|duplicad[oa]|no\s+repetid[oa]|repetid[oa]|existente)",
        re.IGNORECASE,
    )
    MANDATORY_PATTERN = re.compile(
        r"(obligatori[oa]|requerid[oa]|proporcionando\s+obligatoriamente|campo\s+requerido)",
        re.IGNORECASE,
    )
    BOUNDARY_RANGE_PATTERN = re.compile(
        r"entre\s+(\d+)\s+y\s+(\d+)\s*(caracteres|d[íi]as|meses|a[ñn]os|elementos|unidades|items|usuarios)?",
        re.IGNORECASE,
    )
    BOUNDARY_MIN_PATTERN = re.compile(
        r"m[íi]nimo\s+(\d+)|al\s+menos\s+(\d+)|mayor\s+o\s+igual\s+a\s+(\d+)",
        re.IGNORECASE,
    )
    BOUNDARY_MAX_PATTERN = re.compile(
        r"m[áa]ximo\s+(\d+)|hasta\s+(\d+)|menor\s+o\s+igual\s+a\s+(\d+)",
        re.IGNORECASE,
    )
    SUCCESS_MESSAGE_PATTERN = re.compile(
        r"(mensaje\s+de\s+[ée]xito|notificaci[óo]n\s+de\s+[ée]xito|confirmaci[óo]n|muestra\s+un\s+mensaje)",
        re.IGNORECASE,
    )
    STATE_TRANSITION_PATTERN = re.compile(
        r"(desactivar|activar|eliminar|bloquear|desbloquear|suspender|cancelar)",
        re.IGNORECASE,
    )

    def generate(
        self,
        story: UserStory,
        criteria: list[AcceptanceCriterion],
        options: GenerationOptions,
    ) -> list[TestCase]:
        test_cases: list[TestCase] = []
        counter = 1

        actor_role = story.role or "Usuario"
        precondition_actor = f"El usuario ha iniciado sesión como {actor_role}."

        # -------------------------------------------------------------
        # CASO 1: Sin Criterios de Aceptación (Generación Preliminar)
        # -------------------------------------------------------------
        if not criteria:
            if options.include_positive:
                tc = TestCase(
                    id=self._format_id(story, counter),
                    title=f"Verificar {story.goal.lower() if story.goal else 'funcionalidad de la historia'}",
                    description=f"Validar el flujo principal correspondiente a: '{story.raw_text}'.",
                    type=TestCaseType.POSITIVE,
                    category=Category.FUNCTIONAL,
                    priority=Priority.MEDIUM,
                    preconditions=[precondition_actor],
                    required_data={"datos_base": "Valores estándar permitidos"},
                    steps=[
                        f"1. Acceder al módulo correspondiente para {story.goal.lower() if story.goal else 'la funcionalidad'}.",
                        "2. Ejecutar la acción principal descrita en la historia.",
                        "3. Confirmar la operación.",
                    ],
                    expected_result=f"El sistema permite {story.goal.lower() if story.goal else 'completar la acción'} satisfactoriamente.",
                    requirement_reference=story.issue_key,
                    acceptance_criteria_reference=None,
                    confidence=Confidence.LOW,
                    status=Status.REVIEW_REQUIRED,
                )
                test_cases.append(tc)
            return test_cases

        # -------------------------------------------------------------
        # CASO 2: Con Criterios de Aceptación (Análisis por Criterio)
        # -------------------------------------------------------------
        for criterion in criteria:
            desc = criterion.description.strip()

            # A. Casos Positivos
            if options.include_positive:
                positive_tc = self._generate_positive_case(
                    story=story,
                    criterion=criterion,
                    counter=counter,
                    precondition_actor=precondition_actor,
                )
                if positive_tc:
                    test_cases.append(positive_tc)
                    counter += 1

            # B. Casos Negativos (SOLO con evidencia explícita)
            if options.include_negative:
                negative_cases = self._generate_negative_cases(
                    story=story,
                    criterion=criterion,
                    counter=counter,
                    precondition_actor=precondition_actor,
                )
                for neg_tc in negative_cases:
                    test_cases.append(neg_tc)
                    counter += 1

            # C. Casos de Validación (Mensajes explícitos)
            if options.include_validation:
                validation_tc = self._generate_validation_case(
                    story=story,
                    criterion=criterion,
                    counter=counter,
                    precondition_actor=precondition_actor,
                )
                if validation_tc:
                    test_cases.append(validation_tc)
                    counter += 1

            # D. Casos Límite (Boundary - SOLO con números/rangos explícitos)
            if options.include_boundary:
                boundary_cases = self._generate_boundary_cases(
                    story=story,
                    criterion=criterion,
                    counter=counter,
                    precondition_actor=precondition_actor,
                )
                for b_tc in boundary_cases:
                    test_cases.append(b_tc)
                    counter += 1

        # Filtro de prioridad mínima si se especificó
        return self._filter_by_priority(test_cases, options.min_priority)

    # -----------------------------------------------------------------
    # Generadores Específicos
    # -----------------------------------------------------------------

    def _generate_positive_case(
        self,
        story: UserStory,
        criterion: AcceptanceCriterion,
        counter: int,
        precondition_actor: str,
    ) -> Optional[TestCase]:
        """Genera el escenario positivo directo del criterio."""
        desc = criterion.description.strip()
        fields = self._extract_explicit_fields(desc)

        title = self._create_title_from_desc("Validar que", desc)
        required_data = {f: f"Valor válido para {f}" for f in fields} if fields else {"datos": "Valores válidos según especificación"}

        steps = [
            f"1. Acceder a la interfaz correspondiente al criterio {criterion.id}.",
            f"2. Ingresar la información requerida: {', '.join(fields) if fields else 'datos válidos'}.",
            "3. Ejecutar la acción.",
        ]

        expected = f"La acción se completa exitosamente conforme a: '{desc}'."

        return TestCase(
            id=self._format_id(story, counter),
            title=title,
            description=f"Verificar el comportamiento positivo del criterio {criterion.id}: '{desc}'.",
            type=TestCaseType.POSITIVE,
            category=Category.FUNCTIONAL,
            priority=Priority.HIGH,
            preconditions=[precondition_actor],
            required_data=required_data,
            steps=steps,
            expected_result=expected,
            requirement_reference=story.issue_key,
            acceptance_criteria_reference=criterion.id,
            confidence=Confidence.HIGH,
            status=Status.READY,
        )

    def _generate_negative_cases(
        self,
        story: UserStory,
        criterion: AcceptanceCriterion,
        counter: int,
        precondition_actor: str,
    ) -> list[TestCase]:
        """
        Genera casos negativos ÚNICAMENTE cuando existe evidencia explícita:
        - Regla de unicidad -> Intento con valor duplicado.
        - Obligatoriedad explícita -> Omisión de campo obligatorio.
        - Transición de estado -> Intento en estado inválido (si aplica).
        """
        negative_cases: list[TestCase] = []
        desc = criterion.description.strip()

        # 1. Evidencia de Unicidad
        if self.UNIQUENESS_PATTERN.search(desc):
            field_name = self._extract_unique_field_name(desc)
            tc = TestCase(
                id=self._format_id(story, counter + len(negative_cases)),
                title=f"Validar rechazo de {field_name} duplicado",
                description=f"Verificar que el sistema rechaza la operación si el {field_name} ya existe en el sistema.",
                type=TestCaseType.NEGATIVE,
                category=Category.VALIDATION,
                priority=Priority.CRITICAL,
                preconditions=[
                    precondition_actor,
                    f"Existe un registro previo en el sistema con el {field_name} de prueba.",
                ],
                required_data={field_name: "valor_ya_registrado@ejemplo.com" if "correo" in field_name.lower() or "email" in field_name.lower() else "VALOR_DUPLICADO"},
                steps=[
                    f"1. Intentar registrar una entidad utilizando un {field_name} ya existente.",
                    "2. Confirmar la operación.",
                ],
                expected_result=f"El sistema rechaza la operación e informa que el {field_name} ya se encuentra registrado.",
                requirement_reference=story.issue_key,
                acceptance_criteria_reference=criterion.id,
                confidence=Confidence.HIGH,
                status=Status.READY,
            )
            negative_cases.append(tc)

        # 2. Evidencia de Obligatoriedad
        if self.MANDATORY_PATTERN.search(desc):
            fields = self._extract_explicit_fields(desc)
            for f in fields:
                tc = TestCase(
                    id=self._format_id(story, counter + len(negative_cases)),
                    title=f"Validar rechazo por omisión de campo obligatorio '{f}'",
                    description=f"Verificar que el sistema no permite completar la acción si falta el campo obligatorio '{f}'.",
                    type=TestCaseType.NEGATIVE,
                    category=Category.VALIDATION,
                    priority=Priority.HIGH,
                    preconditions=[precondition_actor],
                    required_data={f: "[VACIO]"},
                    steps=[
                        f"1. Completar los datos omitiendo el campo obligatorio '{f}'.",
                        "2. Intentar guardar o enviar el formulario.",
                    ],
                    expected_result=f"El sistema rechaza la operación y solicita ingresar el campo obligatorio '{f}'.",
                    requirement_reference=story.issue_key,
                    acceptance_criteria_reference=criterion.id,
                    confidence=Confidence.HIGH,
                    status=Status.READY,
                )
                negative_cases.append(tc)

        return negative_cases

    def _generate_validation_case(
        self,
        story: UserStory,
        criterion: AcceptanceCriterion,
        counter: int,
        precondition_actor: str,
    ) -> Optional[TestCase]:
        """Genera caso de validación si el criterio menciona explícitamente un mensaje/notificación."""
        desc = criterion.description.strip()
        if self.SUCCESS_MESSAGE_PATTERN.search(desc):
            return TestCase(
                id=self._format_id(story, counter),
                title="Validar mensaje de confirmación en pantalla",
                description=f"Verificar que el sistema presenta el mensaje de confirmación correspondiente: '{desc}'.",
                type=TestCaseType.VALIDATION,
                category=Category.VALIDATION,
                priority=Priority.MEDIUM,
                preconditions=[precondition_actor],
                required_data={"accion": "Ejecución de acción válida"},
                steps=[
                    "1. Realizar la operación indicada en el criterio.",
                    "2. Observar la retroalimentación visual del sistema.",
                ],
                expected_result=f"El sistema despliega el mensaje de éxito conforme al criterio: '{desc}'.",
                requirement_reference=story.issue_key,
                acceptance_criteria_reference=criterion.id,
                confidence=Confidence.HIGH,
                status=Status.READY,
            )
        return None

    def _generate_boundary_cases(
        self,
        story: UserStory,
        criterion: AcceptanceCriterion,
        counter: int,
        precondition_actor: str,
    ) -> list[TestCase]:
        """
        Genera casos límite ÚNICAMENTE cuando existen números, rangos o umbrales explícitos.
        """
        boundary_cases: list[TestCase] = []
        desc = criterion.description.strip()

        # 1. Rango explícito: entre X e Y
        range_match = self.BOUNDARY_RANGE_PATTERN.search(desc)
        if range_match:
            min_val = int(range_match.group(1))
            max_val = int(range_match.group(2))
            unit = range_match.group(3) or "unidades"

            # Caso 1: Límite Mínimo Válido
            boundary_cases.append(
                TestCase(
                    id=self._format_id(story, counter + len(boundary_cases)),
                    title=f"Validar límite inferior permitido ({min_val} {unit})",
                    description=f"Verificar aceptación con el valor mínimo permitido de {min_val} {unit}.",
                    type=TestCaseType.BOUNDARY,
                    category=Category.BOUNDARY,
                    priority=Priority.HIGH,
                    preconditions=[precondition_actor],
                    required_data={"longitud_o_valor": f"{min_val} {unit}"},
                    steps=[
                        f"1. Ingresar un dato con longitud o valor exactamente igual a {min_val} {unit}.",
                        "2. Enviar el formulario.",
                    ],
                    expected_result=f"El sistema acepta el valor mínimo permitido ({min_val} {unit}).",
                    requirement_reference=story.issue_key,
                    acceptance_criteria_reference=criterion.id,
                    confidence=Confidence.HIGH,
                    status=Status.READY,
                )
            )

            # Caso 2: Límite Máximo Válido
            boundary_cases.append(
                TestCase(
                    id=self._format_id(story, counter + len(boundary_cases)),
                    title=f"Validar límite superior permitido ({max_val} {unit})",
                    description=f"Verificar aceptación con el valor máximo permitido de {max_val} {unit}.",
                    type=TestCaseType.BOUNDARY,
                    category=Category.BOUNDARY,
                    priority=Priority.HIGH,
                    preconditions=[precondition_actor],
                    required_data={"longitud_o_valor": f"{max_val} {unit}"},
                    steps=[
                        f"1. Ingresar un dato con longitud o valor exactamente igual a {max_val} {unit}.",
                        "2. Enviar el formulario.",
                    ],
                    expected_result=f"El sistema acepta el valor máximo permitido ({max_val} {unit}).",
                    requirement_reference=story.issue_key,
                    acceptance_criteria_reference=criterion.id,
                    confidence=Confidence.HIGH,
                    status=Status.READY,
                )
            )

            # Caso 3: Debajo del Mínimo (Inválido)
            if min_val > 0:
                boundary_cases.append(
                    TestCase(
                        id=self._format_id(story, counter + len(boundary_cases)),
                        title=f"Validar rechazo por debajo del límite inferior ({min_val - 1} {unit})",
                        description=f"Verificar rechazo al ingresar un valor por debajo del mínimo ({min_val - 1} {unit}).",
                        type=TestCaseType.BOUNDARY,
                        category=Category.BOUNDARY,
                        priority=Priority.HIGH,
                        preconditions=[precondition_actor],
                        required_data={"longitud_o_valor": f"{min_val - 1} {unit}"},
                        steps=[
                            f"1. Ingresar un dato con longitud o valor igual a {min_val - 1} {unit}.",
                            "2. Intentar guardar la información.",
                        ],
                        expected_result=f"El sistema rechaza el dato por ser menor al mínimo permitido de {min_val} {unit}.",
                        requirement_reference=story.issue_key,
                        acceptance_criteria_reference=criterion.id,
                        confidence=Confidence.HIGH,
                        status=Status.READY,
                    )
                )

            # Caso 4: Encima del Máximo (Inválido)
            boundary_cases.append(
                TestCase(
                    id=self._format_id(story, counter + len(boundary_cases)),
                    title=f"Validar rechazo por encima del límite superior ({max_val + 1} {unit})",
                    description=f"Verificar rechazo al ingresar un valor que supera el máximo ({max_val + 1} {unit}).",
                    type=TestCaseType.BOUNDARY,
                    category=Category.BOUNDARY,
                    priority=Priority.HIGH,
                    preconditions=[precondition_actor],
                    required_data={"longitud_o_valor": f"{max_val + 1} {unit}"},
                    steps=[
                        f"1. Ingresar un dato con longitud o valor igual a {max_val + 1} {unit}.",
                        "2. Intentar guardar la información.",
                    ],
                    expected_result=f"El sistema rechaza el dato por superar el límite máximo permitido de {max_val} {unit}.",
                    requirement_reference=story.issue_key,
                    acceptance_criteria_reference=criterion.id,
                    confidence=Confidence.HIGH,
                    status=Status.READY,
                )
            )

        return boundary_cases

    # -----------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------

    @staticmethod
    def _format_id(story: UserStory, num: int) -> str:
        key = story.issue_key or story.project_key or "TC"
        return f"TC-{key}-{num:03d}"

    @staticmethod
    def _create_title_from_desc(prefix: str, desc: str) -> str:
        # Acortar para título limpio
        cleaned = re.sub(r"^(el\s+sistema\s+|el\s+administrador\s+|el\s+usuario\s+)", "", desc, flags=re.IGNORECASE).strip()
        cleaned = cleaned[0].upper() + cleaned[1:] if cleaned else desc
        if len(cleaned) > 70:
            cleaned = cleaned[:67] + "..."
        return cleaned

    @staticmethod
    def _extract_explicit_fields(text: str) -> list[str]:
        """Extrae campos explícitamente enumerados tras palabras clave como 'proporcionando', 'ingresando'."""
        match = re.search(r"(?:proporcionando|ingresando|con|debe\s+tener|incluye)\s+([^.]+)", text, re.IGNORECASE)
        if not match:
            return []
        raw_fields = match.group(1)
        raw_fields = re.split(r",|\sy\s|\se\s", raw_fields)
        return [f.strip() for f in raw_fields if f.strip() and len(f.strip()) < 35]

    @staticmethod
    def _extract_unique_field_name(text: str) -> str:
        match = re.search(r"(correo\s+electr[óo]nico|email|c[óo]digo|identificaci[óo]n|nombre\s+de\s+usuario|documento|c[ée]dula|nit|tel[ée]fono)", text, re.IGNORECASE)
        if match:
            return match.group(1).lower()
        return "campo con restricción de unicidad"

    @staticmethod
    def _filter_by_priority(cases: list[TestCase], min_priority: Priority) -> list[TestCase]:
        priority_weights = {
            Priority.LOW: 1,
            Priority.MEDIUM: 2,
            Priority.HIGH: 3,
            Priority.CRITICAL: 4,
        }
        min_weight = priority_weights.get(min_priority, 1)
        return [tc for tc in cases if priority_weights.get(tc.priority, 1) >= min_weight]
