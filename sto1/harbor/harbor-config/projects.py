from api import Api


def create(api: Api, projects: list) -> None:
    for project in projects:
        api.post(endpoint="projects", payload=project)
