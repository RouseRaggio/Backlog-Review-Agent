"""
Test Jira Connection

Verifica la conexión con Jira Cloud utilizando la API REST.

Uso:

python tools/test_connection.py
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
        raise ValueError("JIRA_URL no configurada.")

    if not email:
        raise ValueError("JIRA_EMAIL no configurado.")

    if not token:
        raise ValueError("JIRA_API_TOKEN no configurado.")

    url = f"{base_url}/rest/api/3/myself"

    response = requests.get(
        url,
        auth=(email, token),
        headers={
            "Accept": "application/json"
        },
        timeout=30,
    )

    response.raise_for_status()

    user = response.json()

    print("=" * 80)
    print("BACKLOG REVIEW AGENT")
    print("=" * 80)

    print("\n✅ Conexión exitosa con Jira\n")

    print(f"Usuario : {user.get('displayName')}")
    print(f"Cuenta  : {user.get('accountId')}")
    print(f"Correo  : {user.get('emailAddress', 'No disponible')}")
    print(f"URL     : {base_url}")

    print("\nEstado: OK")
    print("=" * 80)


if __name__ == "__main__":
    main()