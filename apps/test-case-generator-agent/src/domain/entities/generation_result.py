"""
Domain Entity: GenerationResult
"""

from __future__ import annotations

from dataclasses import dataclass, field
from src.domain.entities.test_case import TestCase
from src.domain.enums import Confidence, TestCaseType


@dataclass(slots=True)
class GenerationResult:
    """
    Resultado consolidado del proceso de generación de casos de prueba.
    """

    project_key: str
    issue_key: str
    test_cases: list[TestCase] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    traceability_map: dict[str, list[str]] = field(default_factory=dict)
    overall_confidence: Confidence = Confidence.HIGH

    @property
    def total_cases(self) -> int:
        return len(self.test_cases)

    @property
    def positive_count(self) -> int:
        return sum(1 for tc in self.test_cases if tc.type == TestCaseType.POSITIVE)

    @property
    def negative_count(self) -> int:
        return sum(1 for tc in self.test_cases if tc.type == TestCaseType.NEGATIVE)

    @property
    def validation_count(self) -> int:
        return sum(1 for tc in self.test_cases if tc.type == TestCaseType.VALIDATION)

    @property
    def boundary_count(self) -> int:
        return sum(1 for tc in self.test_cases if tc.type == TestCaseType.BOUNDARY)

    @property
    def traceability_rate(self) -> float:
        if not self.traceability_map:
            return 100.0 if self.total_cases > 0 else 0.0
        covered = sum(1 for cases in self.traceability_map.values() if len(cases) > 0)
        return round((covered / len(self.traceability_map)) * 100, 2)
