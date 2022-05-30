from api import Api


def create(api: Api, registries: list) -> None:
    for registry in registries:
        api.post(endpoint="registries", payload=registry)
