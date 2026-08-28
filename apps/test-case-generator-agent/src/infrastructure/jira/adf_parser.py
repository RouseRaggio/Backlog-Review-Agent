"""
Infrastructure: Atlassian Document Format (ADF) Parser

Recorre la jerarquía de nodos ADF (doc, heading, paragraph, bulletList,
orderedList, listItem, text, rule, etc.) y reconstruye texto plano estructurado
manteniendo encabezados, viñetas y saltos de línea legibles.
"""

from __future__ import annotations

from typing import Any, Optional


class ADFParser:
    """
    Parser robusto para Atlassian Document Format (ADF).
    """

    @classmethod
    def to_text(cls, value: Any) -> Optional[str]:
        """
        Convierte un objeto ADF (dict o list) en texto estructurado con saltos de línea.
        """
        if value is None:
            return None

        if not isinstance(value, dict):
            return str(value).strip() if str(value).strip() else None

        if value.get("type") != "doc" and "content" not in value:
            return str(value).strip() if str(value).strip() else None

        chunks: list[str] = []
        cls._parse_node(value, chunks)

        text = "".join(chunks).strip()
        # Normalizar múltiples saltos de línea consecutivos
        import re
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text if text else None

    @classmethod
    def _parse_node(cls, node: Any, output: list[str], list_depth: int = 0) -> None:
        if not isinstance(node, dict):
            if isinstance(node, list):
                for item in node:
                    cls._parse_node(item, output, list_depth)
            return

        node_type = node.get("type", "")
        content = node.get("content", [])

        if node_type == "text":
            text = node.get("text", "")
            output.append(text)

        elif node_type == "heading":
            # Agregar salto de línea antes y después del heading
            output.append("\n\n")
            for child in content:
                cls._parse_node(child, output, list_depth)
            output.append("\n")

        elif node_type == "paragraph":
            output.append("\n")
            for child in content:
                cls._parse_node(child, output, list_depth)
            output.append("\n")

        elif node_type in ("bulletList", "orderedList"):
            output.append("\n")
            for child in content:
                cls._parse_node(child, output, list_depth + 1)
            output.append("\n")

        elif node_type == "listItem":
            indent = "  " * max(0, list_depth - 1)
            output.append(f"\n{indent}* ")
            for child in content:
                cls._parse_node(child, output, list_depth)

        elif node_type == "rule":
            output.append("\n---\n")

        else:
            for child in content:
                cls._parse_node(child, output, list_depth)
