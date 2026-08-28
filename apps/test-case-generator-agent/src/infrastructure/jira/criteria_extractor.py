"""
Infrastructure: CriteriaExtractor

Extrae de forma separada y robusta:
1. Criterios de Aceptación (Acceptance Criteria -> list[AcceptanceCriterion])
2. Pruebas QA (QA Tests -> list[str])
3. Definición de Terminado (Definition of Done -> list[str])

Soporta campos personalizados dinámicos de Jira (ej. customfield_10614, customfield_10615)
y secciones estructuradas dentro de la descripción (ADF / Markdown).
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any, Optional
from src.domain.entities import AcceptanceCriterion


class CriteriaExtractor:
    """
    Extractor especializado de secciones y campos de Jira.
    """

    CRITERIA_HEADER_PATTERN = re.compile(
        r"^\s*(?:#{1,6}\s*)?(?:criterios?\s+de\s+aceptaci[óo]n|acceptance\s+criteria|condiciones?\s+de\s+aceptaci[óo]n)\s*:?",
        re.MULTILINE | re.IGNORECASE,
    )

    QA_TESTS_HEADER_PATTERN = re.compile(
        r"^\s*(?:#{1,6}\s*)?(?:pruebas?\s+(?:de\s+)?qa|qa\s+tests?|escenarios?\s+de\s+prueba|casos?\s+de\s+prueba\s+qa)\s*:?",
        re.MULTILINE | re.IGNORECASE,
    )

    DOD_HEADER_PATTERN = re.compile(
        r"^\s*(?:#{1,6}\s*)?(?:definici[óo]n\s+de\s+terminado|definition\s+of\s+done|dod)\s*:?",
        re.MULTILINE | re.IGNORECASE,
    )

    SECTION_BREAK_PATTERN = re.compile(
        r"\n\s*(?:#{1,6}\s*)?(?:criterios?\s+de\s+aceptaci[óo]n|acceptance\s+criteria|pruebas?\s+(?:de\s+)?qa|qa\s+tests?|definici[óo]n\s+de\s+terminado|definition\s+of\s+done|dod|dependencias?|reglas?\s+de\s+negocio|alcance|objetivo|requerimientos?\s+que\s+abarca)\s*:?",
        re.IGNORECASE,
    )


    NUMBERED_ITEM_PATTERN = re.compile(
        r"^\s*(?:\d+[\.\)]|\bAC-?\d+[\.:\)]?|\bCA-?\d+[\.:\)]?|\bQA-?\d+[\.:\)]?)\s*(.+)$",
        re.MULTILINE | re.IGNORECASE,
    )

    BULLET_ITEM_PATTERN = re.compile(
        r"^\s*[\*\-•]\s*(.+)$",
        re.MULTILINE,
    )

    @classmethod
    def normalize_str(cls, s: str) -> str:
        """Elimina tildes y normaliza a minúsculas para comparaciones semánticas."""
        return "".join(
            c for c in unicodedata.normalize("NFD", s.lower())
            if unicodedata.category(c) != "Mn"
        )

    @classmethod
    def extract(
        cls,
        description: Optional[str],
        custom_field_value: Optional[str] = None,
    ) -> list[AcceptanceCriterion]:
        """
        Método de compatibilidad para extraer Criterios de Aceptación desde descripción o texto de campo.
        """
        fields: dict[str, Any] = {}
        if description:
            fields["description"] = description
        if custom_field_value:
            fields["customfield_ac"] = custom_field_value

        criteria, _, _ = cls.extract_from_fields(fields, custom_ac_field_id="customfield_ac")
        return criteria

    @classmethod
    def extract_from_fields(
        cls,
        fields: dict[str, Any],
        custom_ac_field_id: Optional[str] = None,
    ) -> tuple[list[AcceptanceCriterion], list[str], list[str]]:
        """
        Extrae Criterios de Aceptación, Pruebas QA y DoD inspeccionando campos personalizados y la descripción.
        Retorna (criteria, qa_tests, dod_items).
        """
        from src.infrastructure.jira.jira_client import JiraClient

        criteria_text: Optional[str] = None
        qa_tests_text: Optional[str] = None
        dod_text: Optional[str] = None

        # 1. Si se indicó un ID explícito de campo de criterios (ej. en .env)
        if custom_ac_field_id and custom_ac_field_id in fields:
            val = fields.get(custom_ac_field_id)
            criteria_text = JiraClient.extract_text(val)

        # 2. Escanear campos personalizados buscando por nombres de campos o keys conocidas
        for k, v in fields.items():
            if not v:
                continue

            # Si es customfield_10614 (Criterios de Aceptación en Jira)
            if k == "customfield_10614" and not criteria_text:
                criteria_text = JiraClient.extract_text(v)

            # Si es customfield_10615 (Pruebas QA en Jira)
            if k == "customfield_10615" and not qa_tests_text:
                qa_tests_text = JiraClient.extract_text(v)

        description_text = JiraClient.extract_text(fields.get("description")) or ""

        # 3. Extraer Criterios de Aceptación
        criteria: list[AcceptanceCriterion] = []
        if criteria_text and criteria_text.strip():
            criteria = cls._parse_text_to_criteria(criteria_text.strip(), require_explicit_markers=False)

        if not criteria and description_text:
            criteria = cls._extract_section_criteria(description_text)

        # 4. Extraer Pruebas QA
        qa_tests: list[str] = []
        if qa_tests_text and qa_tests_text.strip():
            qa_tests, dod_extracted = cls._parse_qa_tests_field(qa_tests_text.strip())
            if dod_extracted and not dod_text:
                dod_text = "\n".join(dod_extracted)

        if not qa_tests and description_text:
            qa_tests = cls._extract_section_lines(description_text, cls.QA_TESTS_HEADER_PATTERN)

        # 5. Extraer DoD
        dod_items: list[str] = []
        if dod_text:
            dod_items = cls._parse_lines(dod_text)
        elif description_text:
            dod_items = cls._extract_section_lines(description_text, cls.DOD_HEADER_PATTERN)

        return criteria, qa_tests, dod_items

    @classmethod
    def _clean_item_line(cls, line: str) -> str:
        """
        Limpia prefijos de viñeta (*, -, •) o numeración (1., 2., AC-001:, QA-001:) de una línea.
        """
        clean = line.strip()
        bullet_m = cls.BULLET_ITEM_PATTERN.match(clean)
        if bullet_m:
            clean = bullet_m.group(1).strip()

        num_m = cls.NUMBERED_ITEM_PATTERN.match(clean)
        if num_m:
            clean = num_m.group(1).strip()

        return clean

    @classmethod
    def _parse_lines(cls, text: str) -> list[str]:
        """
        Convierte un bloque de texto en una lista de líneas limpias.
        """
        raw_lines = [line.strip() for line in text.split("\n") if line.strip()]
        items: list[str] = []
        for line in raw_lines:
            clean = cls._clean_item_line(line)
            if len(clean) >= 4:
                items.append(clean)
        return items

    @classmethod
    def _parse_qa_tests_field(cls, text: str) -> tuple[list[str], list[str]]:
        """
        Parsea el texto de un campo de pruebas QA, separando si contiene encabezados de DoD o Dependencias.
        """
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        qa_tests: list[str] = []
        dod_items: list[str] = []

        current_section = "QA_TESTS"

        for line in lines:
            normalized = cls.normalize_str(line)
            if "definicion de terminado" in normalized or "definition of done" in normalized or "dod" in normalized:
                current_section = "DOD"
                continue
            elif "dependencias" in normalized or "dependencies" in normalized:
                current_section = "DEPENDENCIES"
                continue
            elif "pruebas qa" in normalized or "qa tests" in normalized:
                current_section = "QA_TESTS"
                continue

            clean_item = cls._clean_item_line(line)
            if len(clean_item) >= 3:
                if current_section == "QA_TESTS":
                    qa_tests.append(clean_item)
                elif current_section == "DOD":
                    dod_items.append(clean_item)

        return qa_tests, dod_items

    @classmethod
    def _extract_section_criteria(cls, text: str) -> list[AcceptanceCriterion]:
        """
        Busca la sección 'Criterios de Aceptación' en el texto y extrae la lista de criterios.
        """
        if "escenario:" in text.lower() or "scenario:" in text.lower():
            gherkin_matches = re.findall(r"(?:Escenario|Scenario)\s*:\s*([^.\n]+)", text, re.IGNORECASE)
            if gherkin_matches:
                criteria = []
                for i, scenario in enumerate(gherkin_matches, start=1):
                    clean_scenario = scenario.strip()
                    if clean_scenario:
                        criteria.append(
                            AcceptanceCriterion(
                                id=f"AC-{i:03d}",
                                description=f"Escenario: {clean_scenario}",
                                rule_type="GHERKIN",
                            )
                        )
                if criteria:
                    return criteria

        match = cls.CRITERIA_HEADER_PATTERN.search(text)
        if match:
            section_text = text[match.end():].strip()
            next_match = cls.SECTION_BREAK_PATTERN.search(section_text)
            if next_match:
                section_text = section_text[:next_match.start()].strip()
            return cls._parse_text_to_criteria(section_text, require_explicit_markers=False)

        return cls._parse_text_to_criteria(text, require_explicit_markers=True)

    @classmethod
    def _extract_section_lines(cls, text: str, header_pattern: re.Pattern) -> list[str]:
        """
        Busca una sección por su encabezado y devuelve sus líneas de ítems.
        """
        match = header_pattern.search(text)
        if not match:
            return []

        section_text = text[match.end():].strip()
        next_match = cls.SECTION_BREAK_PATTERN.search(section_text)
        if next_match:
            section_text = section_text[:next_match.start()].strip()

        return cls._parse_lines(section_text)

    @classmethod
    def _parse_text_to_criteria(
        cls,
        text: str,
        require_explicit_markers: bool = False,
    ) -> list[AcceptanceCriterion]:
        """
        Convierte un bloque de texto en una lista de AcceptanceCriterion.
        """
        raw_lines = [line.strip() for line in text.split("\n") if line.strip()]
        criteria: list[AcceptanceCriterion] = []
        count = 1

        for line in raw_lines:
            has_marker = bool(
                cls.NUMBERED_ITEM_PATTERN.match(line)
                or cls.BULLET_ITEM_PATTERN.match(line)
            )

            if require_explicit_markers and not has_marker:
                continue

            clean = cls._clean_item_line(line)
            if len(clean) >= 4:
                criteria.append(
                    AcceptanceCriterion(
                        id=f"AC-{count:03d}",
                        description=clean,
                    )
                )
                count += 1

        return criteria
