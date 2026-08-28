"""
Composition Root: Dependency Injection for Test Case Generator Agent.
"""

from __future__ import annotations

from src.application.use_cases.analyze_user_story import AnalyzeUserStoryUseCase
from src.application.use_cases.generate_test_cases import GenerateTestCasesUseCase
from src.infrastructure.generators.rule_based_generator import RuleBasedTestCaseGenerator
from src.infrastructure.jira.jira_gateway_adapter import JiraGatewayAdapter


def build_jira_gateway() -> JiraGatewayAdapter:
    """
    Construye el adaptador de Jira Gateway.
    """
    return JiraGatewayAdapter()


def build_generate_use_case() -> GenerateTestCasesUseCase:
    """
    Ensambla GenerateTestCasesUseCase con generador y gateway de Jira.
    """
    generator = RuleBasedTestCaseGenerator()
    jira_gateway = build_jira_gateway()
    return GenerateTestCasesUseCase(
        generator=generator,
        jira_gateway=jira_gateway,
    )


def build_analyze_use_case() -> AnalyzeUserStoryUseCase:
    """
    Ensambla AnalyzeUserStoryUseCase con gateway de Jira.
    """
    jira_gateway = build_jira_gateway()
    return AnalyzeUserStoryUseCase(
        jira_gateway=jira_gateway,
    )


def build_application() -> GenerateTestCasesUseCase:
    """
    Compatibilidad con punto de entrada anterior.
    """
    return build_generate_use_case()
