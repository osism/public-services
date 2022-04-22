import yaml
import robot_accounts
import replication_rules
import registries
import projects
from api import Api


def main(api: Api, config: dict) -> None:
    registries.create(api=api, registries=config['registries'])
    projects.create(api=api, projects=config['projects'])
    replication_rules.create(api=api, replication_rules=config['replication_rules'])
    print(robot_accounts.create(api=api, robot_accounts=config['robot_accounts']))


if __name__ == "__main__":
    with open("config.yml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    api = Api(
        url=config['api']['url'],
        username=config['api']['username'],
        password=config['api']['password'],
        verify=config['api']['verify']
    )
    main(api, config)
