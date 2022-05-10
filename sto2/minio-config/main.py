import yaml
import buckets
import users
import subprocess
from s3 import S3, S3Admin


def main(s3: S3, config: dict) -> None:
    buckets.create(s3=s3, buckets=config['buckets'])


def admin(s3admin: S3Admin, config: dict) -> None:
    users.create(s3admin=s3admin, users=config['users'])


if __name__ == "__main__":
    with open("config.yml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    s3 = S3(
        endpoint=config['s3']['endpoint'],
        access_key=config['s3']['secret_key'],
        secret_key=config['s3']['access_key']
    )

    target = "mcconfig"
    subprocess.run(
        [
            "mc",
            "--json",
            "alias",
            "set",
            target,
            f"https://{config['s3']['endpoint']}",
            config['s3']['secret_key'],
            config['s3']['access_key']
        ],
        text=True,
        check=True,
        timeout=None,
        env=None,
        capture_output=True
    )
    s3admin = S3Admin(target=target)

    main(s3, config)
    admin(s3admin, config)

    subprocess.run(
        ["mc", "--json", "alias", "rm", target],
        text=True,
        check=True,
        timeout=None,
        env=None,
        capture_output=True
    )
