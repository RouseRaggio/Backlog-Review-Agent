"""
Domain Entity: TestCase
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from src.domain.enums import (
    Category,
    Confidence,
    Priority,
    Status,
    TestCaseType,
)


@dataclass(slots=True)
class TestCase:
    """
    Representa un Caso de Prueba generado.
    """

    __test__ = False

    id: str

    title: str
    description: str
    type: TestCaseType
    category: Category
    priority: Priority
    expected_result: str
    requirement_reference: str  # Issue Key (ej. GES-123)
    acceptance_criteria_reference: Optional[str] = None  # AC-001 o 'USER_STORY'
    preconditions: list[str] = field(default_factory=list)
    required_data: dict[str, str] = field(default_factory=dict)
    steps: list[str] = field(default_factory=list)
    confidence: Confidence = Confidence.HIGH
    status: Status = Status.READY
