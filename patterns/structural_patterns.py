from time import time


# структурный паттерн - Декоратор
class AppRoute:
    def __init__(self, routes, url):
        """
        Сохраняем значение переданного параметра
        """
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        """
        Сам декоратор
        """
        self.routes[self.url] = cls()
