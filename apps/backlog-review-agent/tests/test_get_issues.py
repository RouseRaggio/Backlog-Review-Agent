from src.infrastructure.jira.jira_client import JiraClient

client = JiraClient()

issues = client.get_issues(
    project_key="CAP"
)

print(f"Issues encontrados: {len(issues)}")

for issue in issues:

    print("----------------------------")

    print(issue["key"])

    print(issue["fields"]["issuetype"]["name"])

    print(issue["fields"]["summary"])