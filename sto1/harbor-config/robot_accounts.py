from api import Api


def rework_permissions(permissions_list: list) -> list:
    for permission in permissions_list:
        permission['access'] = []
        for entry in permission['access_simplified']:
            resource, action = entry.split(":")
            permission['access'].append(
                {"action": action, "resource": resource}
            )
        del permission['access_simplified']
    return permissions_list


def create(api: Api, robot_accounts: list) -> list:
    result = []
    for robot_account in robot_accounts:
        robot_account['permissions'] = rework_permissions(permissions_list=robot_account['permissions'])

        rvalue = api.post(endpoint="robots", payload=robot_account)

        if "is_failed" not in rvalue:
            result.append(f"{rvalue['name']}: {rvalue['secret']}")

    return result
