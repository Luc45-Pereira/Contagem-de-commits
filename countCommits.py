import requests
from datetime import datetime

# Substitua esses valores com suas informações
organization = ''
start_date = "2023-08-01T00:00:00Z"  # Data de início do período desejado
end_date = "2023-08-07T23:59:59Z"    # Data de término do período desejado
access_token = ""

# Construa o URL da API para listar os repositórios da organização
repos_url = f"https://api.github.com/orgs/{organization}/repos"

# Configure o cabeçalho da autenticação
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Faça a solicitação à API para obter a lista de repositórios da organização
repos_response = requests.get(repos_url, headers=headers)
pullIds = []
# Verifique se a solicitação foi bem-sucedida
if repos_response.status_code == 200:
    repos = repos_response.json()
    total_commits = 0
    
    # Para cada repositório, obtenha a lista de pull requests e conte os commits
    for repo in repos:
        pulls_url = repo["pulls_url"].replace("{/number}", "")
        pulls_response = requests.get(pulls_url, headers=headers, params={"state": "all"})
        if pulls_response.status_code == 200:
            pull_requests = pulls_response.json()
            for pull_request in pull_requests:
                created_at = pull_request["created_at"]
                if start_date <= created_at <= end_date and pull_request["user"]["login"] == 'Luc45-Pereira':
                    commits_url = pull_request["commits_url"]
                    commits_response = requests.get(commits_url, headers=headers)
                    
                    if commits_response.status_code == 200:
                        pullIds.append(pull_request['number'])
                        commits = commits_response.json()
                        total_commits += len(commits)

    print(f"Total de seus commits em pull requests da organização: {total_commits}")
    print(f"Pull requests: {pullIds}")
    print(f"Total de pull requests: {len(pullIds)}")
else:
    print("Erro ao acessar a API do GitHub:", repos_response.status_code)

