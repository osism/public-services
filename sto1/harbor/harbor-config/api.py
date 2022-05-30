from json import JSONDecodeError
import requests


class Api:
    url: str = ""
    password: str = ""
    username: str = ""
    verify: bool = True

    def __init__(self, url: str, password: str, username: str, verify: bool = True) -> None:
        self.url = url
        self.password = password
        self.username = username
        self.verify = verify

        requests.packages.urllib3.disable_warnings()

    def get(self, endpoint: str) -> list:
        r = requests.get(
            url=f"{self.url}/{endpoint}",
            auth=(self.username, self.password),
            verify=self.verify
        )
        result = r.json()

        if type(result) is dict:
            return [result]

        return result

    def post(self, endpoint: str, payload: dict, statuscode: int = 201) -> dict:
        r = requests.post(
            url=f"{self.url}/{endpoint}",
            auth=(self.username, self.password),
            json=payload,
            verify=self.verify
        )

        # Catch error when r.json() is not available
        try:
            result = r.json()
        except JSONDecodeError:
            result = {}

        if r.status_code != statuscode:
            print("Failed!")
            # add a dict key to identify if the result is an error message
            result['is_failed'] = True

        return result
