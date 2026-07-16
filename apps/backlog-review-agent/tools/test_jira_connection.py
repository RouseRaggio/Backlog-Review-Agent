import os

from dotenv import load_dotenv
from jira import JIRA

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

if not all([JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN]):
    raise ValueError(
        "Faltan variables de entorno. Revisa tu archivo .env"
    )

jira = JIRA(
    server=JIRA_URL,
    basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN),
)

me = jira.myself()

print("=====================================")
print("✅ Conexión exitosa con Jira")
print("=====================================")
print(f"Usuario : {me['displayName']}")
print(f"Correo  : {me.get('emailAddress', 'No disponible')}")