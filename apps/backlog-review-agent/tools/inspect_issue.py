"""
Inspect Jira Issue

Herramienta para inspeccionar la estructura completa de un Issue
retornado por la API REST de Jira.

Uso:

python tools/inspect_issue.py CAP-249
"""

import json
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()


def main():

    if len(sys.argv) != 2:
        print("Uso:")
        print("python tools/inspect_issue.py <ISSUE_KEY>")
        return

    issue_key = sys.argv[1]

    base_url = os.getenv("JIRA_URL")
    email = os.getenv("JIRA_EMAIL")
    token = os.getenv("JIRA_API_TOKEN")

    url = f"{base_url}/rest/api/3/issue/{issue_key}"

    response = requests.get(
        url,
        auth=(email, token),
        headers={
            "Accept": "application/json"
        },
        timeout=30,
    )

    response.raise_for_status()

    issue = response.json()

    print("=" * 80)
    print(f"Issue: {issue_key}")
    print("=" * 80)

    print("\n=== CAMPOS DISPONIBLES ===\n")

    fields = issue["fields"]

    print("\n========================")
    print("CAMPOS IMPORTANTES")
    print("========================\n")

    important_fields = [
        "summary",
        "issuetype",
        "status",
        "priority",
        "assignee",
        "parent",
        "description",
    ]

    for field in important_fields:

        print(f"\n----- {field} -----")

        value = fields.get(field)

        print(json.dumps(value, indent=2, ensure_ascii=False, default=str))

    for field in sorted(fields.keys()):

        value = fields[field]

        print("-" * 80)
        print(field)

        if isinstance(value, (dict, list)):
            print(json.dumps(value, indent=2, ensure_ascii=False))
        else:
            print(value)

    print("\n")
    print("=" * 80)
    print("FIN")
    print("=" * 80)


if __name__ == "__main__":
    main()