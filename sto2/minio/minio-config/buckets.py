from s3 import S3
import policies
import json


def create(s3: S3, buckets: list) -> None:
    for bucket in buckets:
        if not s3.bucket_exists(bucket['name']):
            s3.make_bucket(bucket['name'])

        if bucket['policy'] == "download":
            policy = policies.Download(bucket=bucket['name']).get()
        elif bucket['policy'] == "public":
            policy = policies.Public(bucket=bucket['name']).get()
        elif bucket['policy'] == "private":
            policy = policies.Private(bucket=bucket['name']).get()

        s3.set_bucket_policy(bucket['name'], json.dumps(policy))
