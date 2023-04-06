import pytest

from bot.products import get_category_product
from bot.errors import IncorrectAddCmdError


@pytest.mark.parametrize('cmd, exp_category, exp_product', [
    ('/addproduct;Волейбол;тренер Владимир', 'Волейбол', 'тренер Владимир'),
    ('/addproduct;Массаж;мастер Андрей', 'Массаж', 'мастер Андрей'),
])
def test_parsed(cmd, exp_category, exp_product):
    category, product = get_category_product(cmd)
    assert category == exp_category
    assert product == exp_product


@pytest.mark.parametrize('cmd', [
    '/addproduct;Волейбол',
    '/addproduct',
])
def test_empty_product(cmd):
    with pytest.raises(IncorrectAddCmdError):
        get_category_product(cmd)
