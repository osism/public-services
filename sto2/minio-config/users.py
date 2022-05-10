from s3 import S3Admin
from policies import UserPolicy
import json
import uuid
import os


def create(s3admin: S3Admin, users: list) -> None:
    for user in users:
        s3admin.user_add(user['name'], user['secret'])

        # Set policies
        policy = UserPolicy(buckets=user['buckets'], user=user['name'])
        file = f"/tmp/{uuid.uuid1()}.json"
        with open(file, 'w') as f:
            json.dump(policy.get(), f)
        s3admin.policy_add(user['name'], file)
        os.remove(file)
        s3admin.policy_set(user['name'], user['name'])
