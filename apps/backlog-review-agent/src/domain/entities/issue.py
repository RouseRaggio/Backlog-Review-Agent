"""
Domain Model: Issue

Representa un Issue de Jira dentro del dominio del
Backlog Review Agent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(slots=True)
class Issue:
    """Entidad principal del dominio."""

    # -------------------------
    # Identificación
    # -------------------------

    id: str
    key: str

    # -------------------------
    # Información general
    # -------------------------

    issue_type: str
    summary: str
    description: Optional[str] = None

    # -------------------------
    # Gestión
    # -------------------------

    status: Optional[str] = None
    priority: Optional[str] = None

    reporter: Optional[str] = None
    assignee: Optional[str] = None

    # -------------------------
    # Planeación
    # -------------------------

    epic: Optional[str] = None
    sprint: Optional[str] = None
    story_points: Optional[float] = None

    # -------------------------
    # Calidad
    # -------------------------

    acceptance_criteria: Optional[str] = None

    labels: list[str] = field(default_factory=list)

    # -------------------------
    # Enlace
    # -------------------------

    url: Optional[str] = None

    # =====================================================
    # Helpers
    # =====================================================

    @property
    def has_description(self) -> bool:
        return bool(self.description and self.description.strip())

    @property
    def has_epic(self) -> bool:
        return bool(self.epic)

    @property
    def has_priority(self) -> bool:
        return bool(self.priority)

    @property
    def has_story_points(self) -> bool:
        return self.story_points is not None

    @property
    def has_acceptance_criteria(self) -> bool:
        return bool(
            self.acceptance_criteria
            and self.acceptance_criteria.strip()
        )

    @property
    def is_story(self) -> bool:
        return self.issue_type.lower() == "historia"

    @property
    def is_task(self) -> bool:
        return self.issue_type.lower() == "tarea"

    @property
    def is_bug(self) -> bool:
        return self.issue_type.lower() == "bug"

    @property
    def is_epic(self) -> bool:
        return self.issue_type.lower() == "epic"

    @property
    def is_subtask(self) -> bool:
        return self.issue_type.lower() == "subtarea"

    def __str__(self) -> str:
        return f"{self.key} [{self.issue_type}] {self.summary}"