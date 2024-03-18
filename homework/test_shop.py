"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(500)
        assert not product.check_quantity(1500)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        original_quantity = product.quantity
        product.buy(100)
        assert product.quantity == original_quantity - 100

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(1500)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_add_product(self, cart, product):
        cart.add_product(product, 5)
        assert product in cart.products
        assert cart.products[product] == 5

    def test_remove_product(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 3)
        assert cart.products[product] == 2

    def test_remove_product_completely(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product)
        assert product not in cart.products

    def test_clear_cart(self, cart, product):
        cart.add_product(product, 5)
        cart.clear()
        assert cart.products == {}

    def test_get_total_price(self, cart, product):
        cart.add_product(product, 5)
        expected_total = 5 * product.price
        assert cart.get_total_price() == expected_total

    def test_buy_success(self, cart, product):
        cart.add_product(product, 1)
        cart.buy()  # не выбрасывает исключение
        assert product.quantity == 999  # начальное количество - купленное

    def test_buy_error(self, cart):
        not_enough_stock = Product("limited edition", 1000, "rare item", 1)
        cart.add_product(not_enough_stock, 2)  # пытаемся добавить больше, чем есть в наличии
        with pytest.raises(ValueError):
            cart.buy()  # ожидаем ошибку при попытке купить