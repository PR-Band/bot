from http import HTTPStatus
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
        response.raise_for_status()
        return response.json()

    def get_categories_by_name(self, category_name: str):
        response = httpx.get(self.url, params={'title': category_name})
        response.raise_for_status()
        return response.json()

    def search_categories_by_name(self, category_name: str):
        response = httpx.get(self.url, params={'search': category_name})
        response.raise_for_status()
        return response.json()


class ProductClient:
    def __init__(self, url: str):
        self.url = f'{url}/api/v1/products/'

    def post_product(self, uid, product):
        new_product = {
            'title': product,
            'category_id': uid,
        }
        response = httpx.post(self.url, json=new_product)
        if response.status_code == HTTPStatus.CONFLICT:
            return False
        response.raise_for_status()
        return True


class ScheduleTemplateClient:
    def __init__(self, url: str):
        self.url = f'{url}/api/v1/schedule_templates/'

    def post_schedule_templates(self, day, start_slot, end_slot, uid, product_id):
        new_schedule_templates = {
            'id': uid,
            'product_id': product_id,
            'day': day,
            'start_slot': start_slot,
            'end_slot': end_slot,
        }
        response = httpx.post(self.url, json=new_schedule_templates)
        if response.status_code == HTTPStatus.CONFLICT:
            return False
        response.raise_for_status()
        return True


class ApiClient:

    def __init__(self, url: str):

        self.users = UserClient(url=url)
        self.products = ProductClient(url=url)
        self.categories = CategoryClient(url=url)
        self.scheduletemplate = ScheduleTemplateClient(url=url)


api = ApiClient(url='http://127.0.0.1:8000')
