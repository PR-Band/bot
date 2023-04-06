import httpx


# try, except  HTTPStatusError: Client error '409 CONFLICT'
class UserClient:
    def __init__(self, url: str):
        self.url = f'{url}/api/v1/users/'

    def registrate(self, username: str, tgid: int) -> None:

        data = {'tgid': tgid, 'username': username}
        # if
        response = httpx.post(self.url, json=data)

        # if httpx.HTTPStatusError:

        response.raise_for_status()


class CategoryClient:
    def __init__(self, url: str):
        self.url = f'{url}/api/v1/categories/'

    def get_categories(self):
        response = httpx.get(self.url)
        # logger.info(response.status_code)
        # logger.info(response.text)
        return response.json()

    def get_categories_by_name(self, category_name: str):
        categories_duble = []
        categories_all = api.categories.get_categories()
        for category in categories_all:
            if category_name in category['title']:
                categories_duble.append(category)
        return categories_duble
# str36
# response = httpx.get(self.url, params={'title': category_name})
# logger.info(response.status_code)
# logger.info(response.text)
# return response.json()


class ProductClient:
    def __init__(self, url: str):
        self.url = f'{url}/api/v1/products/'

    def post_product(self, uid, product):
        new_product = {
            'title': product,
            'category_id': uid,
        }
        response = httpx.post(self.url, json=new_product)
        # logger.info(response.status_code)
        # logger.info(response.json())
        if response.status_code == 409:
            return False
        return True


class ApiClient:

    def __init__(self, url: str):

        self.users = UserClient(url=url)
        self.products = ProductClient(url=url)
        self.categories = CategoryClient(url=url)


api = ApiClient(url='http://127.0.0.1:8000')
