class BucketPolicy:
    bucket: str

    def __init__(self, bucket: str) -> None:
        self.bucket = bucket


class Download(BucketPolicy):
    def get(self) -> dict:
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
                    "Resource": f"arn:aws:s3:::{self.bucket}",
                },
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{self.bucket}/*",
                },
            ],
        }
        return policy


class Public(BucketPolicy):
    def get(self) -> dict:
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": [
                        "s3:GetBucketLocation",
                        "s3:ListBucket",
                        "s3:ListBucketMultipartUploads",
                    ],
                    "Resource": f"arn:aws:s3:::{self.bucket}",
                },
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": [
                        "s3:GetObject",
                        "s3:PutObject",
                        "s3:DeleteObject",
                        "s3:ListMultipartUploadParts",
                        "s3:AbortMultipartUpload",
                    ],
                    "Resource": f"arn:aws:s3:::{self.bucket}/*",
                },
            ],
        }
        return policy


class Private(BucketPolicy):
    def get(self) -> dict:
        policy = {
            "Version": "2012-10-17",
            "Statement": [],
        }
        return policy


class UserPolicy:
    buckets: list
    user: str

    def __init__(self, buckets: list, user: str) -> None:
        self.buckets = buckets
        self.user = user

    def get(self) -> dict:
        policy = {
            "Version": "2012-10-17",
            "Statement": []
        }

        for bucket in self.buckets:
            entry = {
                "Effect": "Allow",
                "Action": [],
                "Resource": [
                    f"arn:aws:s3:::{bucket['name']}/*",
                ]
            }
            if bucket['policy'] == "readonly":
                entry['Action'].append("s3:GetBucketLocation")
                entry['Action'].append("s3:GetObject")

            if bucket['policy'] == "readwrite":
                entry['Action'].append("s3:*")

            if bucket['policy'] == "writeonly":
                entry['Action'].append("s3:PutObject")

            policy['Statement'].append(entry)

        return policy
