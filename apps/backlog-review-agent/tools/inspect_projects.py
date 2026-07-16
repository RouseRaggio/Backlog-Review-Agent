"""
Inspect Jira Projects

Lista todos los proyectos disponibles en la instancia de Jira.

Uso:

python tools/inspect_projects.py
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

    url = f"{base_url}/rest/api/3/project/search"

    response = requests.get(
        url,
        auth=(email, token),
        headers={
            "Accept": "application/json"
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    projects = data.get("values", [])

    print("=" * 120)
    print("PROYECTOS DISPONIBLES")
    print("=" * 120)

    if not projects:
        print("No se encontraron proyectos.")
        return

    for index, project in enumerate(projects, start=1):

        print(f"\n[{index}] {project['name']}")
        print(f"Key       : {project['key']}")
        print(f"ID        : {project['id']}")
        print(f"Tipo      : {project.get('projectTypeKey', '-')}")
        print(f"Privado   : {project.get('isPrivate', False)}")

        lead = project.get("lead")

        if lead:
            print(f"Líder     : {lead.get('displayName')}")

        print("-" * 120)

    print(f"\nTotal de proyectos: {len(projects)}")
    print("=" * 120)


if __name__ == "__main__":
    main()