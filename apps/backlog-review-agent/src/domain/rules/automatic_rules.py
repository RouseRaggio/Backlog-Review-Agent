"""
Automatic Audit Rules

Catálogo de reglas automáticas utilizadas por el Rule Engine.
"""

from src.domain.entities.rule import Rule


AUTOMATIC_RULES = [

    Rule(
        id="BR-001",
        name="El Issue debe tener un título",
        field="summary",
        applies_to=[
            "Epic",
            "Historia",
            "Tarea",
            "Bug",
            "Subtarea",
        ],
        severity="HIGH",
        recommendation="Agregar un título claro y representativo."
    ),

    Rule(
        id="BR-002",
        name="El Issue debe tener descripción",
        field="description",
        applies_to=[
            "Epic",
            "Historia",
            "Tarea",
            "Bug",
        ],
        severity="HIGH",
        recommendation="Agregar una descripción clara y completa."
    ),

    Rule(
        id="BR-003",
        name="El Issue debe tener prioridad",
        field="priority",
        applies_to=[
            "Epic",
            "Historia",
            "Tarea",
            "Bug",
            "Subtarea",
        ],
        severity="MEDIUM",
        recommendation="Asignar una prioridad al Issue."
    ),

    Rule(
        id="BR-004",
        name="El Issue debe tener responsable",
        field="assignee",
        applies_to=[
            "Historia",
            "Tarea",
            "Bug",
            "Subtarea",
        ],
        severity="MEDIUM",
        recommendation="Asignar un responsable al Issue."
    ),

    
    Rule(
        id="BR-005",
        name="El Issue debe pertenecer a un Sprint",
        field="sprint",
        applies_to=[
            "Historia",
            "Tarea",
            "Bug",
            "Subtarea",
        ],
        severity="HIGH",
        recommendation="Asociar el Issue a un Sprint."
    ),

    Rule(
        id="BR-006",
        name="El Issue debe estar asociado a una Epic",
        field="epic",
        applies_to=[
            "Historia",
            "Tarea",
            "Bug",
        ],
        severity="HIGH",
        recommendation="Asociar el Issue a una Epic."
    ),

    Rule(
        id="BR-007",
        name="La Historia debe tener Story Points",
        field="story_points",
        applies_to=[
            "Historia",
        ],
        severity="HIGH",
        recommendation="Asignar Story Points a la Historia."
    ),

    Rule(
        id="BR-008",
        name="La Historia debe tener criterios de aceptación",
        field="acceptance_criteria",
        applies_to=[
            "Historia",
        ],
        severity="HIGH",
        recommendation="Agregar criterios de aceptación verificables."
    ),

    Rule(
        id="BR-009",
        name="El Issue debe tener estado",
        field="status",
        applies_to=[
            "Epic",
            "Historia",
            "Tarea",
            "Bug",
            "Subtarea",
        ],
        severity="LOW",
        recommendation="Asignar un estado al Issue."
    ),

    Rule(
        id="BR-010",
        name="El Issue debe tener tipo",
        field="issue_type",
        applies_to=[
            "Epic",
            "Historia",
            "Tarea",
            "Bug",
            "Subtarea",
        ],
        severity="CRITICAL",
        recommendation="Asignar un tipo de Issue."
    ),
]