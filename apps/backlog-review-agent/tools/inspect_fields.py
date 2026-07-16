"""
Inspect Jira Fields

Lista todos los campos disponibles en la instancia de Jira,
incluyendo los custom fields.

Uso:

python tools/inspect_fields.py
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()


def main():

    base_url = os.getenv("JIRA_URL")
    email = os.getenv("JIRA_EMAIL")
    token = os.getenv("JIRA_API_TOKEN")

    if not base_url:
        raise ValueError("JIRA_URL no configurada")

    if not email:
        raise ValueError("JIRA_EMAIL no configurado")

    if not token:
        raise ValueError("JIRA_API_TOKEN no configurado")

    url = f"{base_url}/rest/api/3/field"

    response = requests.get(
        url,
        auth=(email, token),
        headers={
            "Accept": "application/json"
        },
        timeout=30,
    )

    response.raise_for_status()

    fields = response.json()

    print("=" * 120)
    print("CAMPOS DISPONIBLES EN JIRA")
    print("=" * 120)

    for field in sorted(fields, key=lambda x: x["id"]):

        print(f"\nID          : {field['id']}")
        print(f"Nombre      : {field['name']}")
        print(f"Custom      : {field.get('custom', False)}")

        schema = field.get("schema")

        if schema:
            print(f"Tipo        : {schema.get('type')}")
            print(f"Sistema     : {schema.get('system')}")
            print(f"Custom Type : {schema.get('custom')}")

        print("-" * 120)


if __name__ == "__main__":
    main()