"""
Domain Service Port: TestCaseGenerator Interface
"""

from abc import ABC, abstractmethod
from src.domain.entities import (
    AcceptanceCriterion,
    GenerationOptions,
    TestCase,
    UserStory,
)


class TestCaseGenerator(ABC):
    """
    Puerto para generadores de casos de prueba (Rule-Based, LLM, etc.).
    """

    @abstractmethod
    def generate(
        self,
        story: UserStory,
        criteria: list[AcceptanceCriterion],
        options: GenerationOptions,
    ) -> list[TestCase]:
        """
        Genera casos de prueba estructurados y trazables a partir de la historia y criterios.
        """
        pass
