from api import Api


def get_registry_id(api: Api, registry_name: str) -> int:
    result = api.get(endpoint="registries")

    for registry in result:
        if registry['name'] == registry_name:
            return {"id": registry['id']}

    return {"id": -1}


def create(api: Api, replication_rules: list) -> None:
    for replication_rule in replication_rules:
        replication_rule['dest_registry'] = get_registry_id(api=api, registry_name=replication_rule['dest_registry'])

        api.post(endpoint="replication/policies", payload=replication_rule)
