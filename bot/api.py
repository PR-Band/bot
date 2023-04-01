import httpx


# try, except  HTTPStatusError: Client error '409 CONFLICT'
class UserClient:
    def __init__(self, url: str):
        self.url = f'{url}/api/v1/users/'

    def registrate(self, username: str, tgid: int) -> None:

        data = {'tgid': tgid, 'username': username}
        # if
        response = httpx.post(self.url, json=data)

        #if httpx.HTTPStatusError:


        response.raise_for_status()


class ApiClient:

    def __init__(self, url: str):

        self.users = UserClient(url=url)


api = ApiClient(url='http://127.0.0.1:8000')
