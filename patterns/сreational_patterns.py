from copy import deepcopy
from quopri import decodestring

from patterns.behavioral_patterns import Subject, FileWriter


# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name


# админ
class Admin(User):
    pass


# студент
class Client(User):

    def __init__(self, name):
        self.cars = []
        super().__init__(name)


class UserFactory:
    types = {
        'client': Client,
        'admin': Admin
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# порождающий паттерн Прототип
class CarPrototype:
    # прототип автомобилей

    def clone(self):
        return deepcopy(self)


class Car(CarPrototype, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.cars.append(self)
        self.clients = []
        super().__init__()

    def __getitem__(self, item):
        return self.clients[item]

    def add_client(self, client: Client):
        self.clients.append(client)
        client.cars.append(self)
        self.notify()


# грузовые автомобили
class Trucks(Car):
    pass


# легковые автомобили
class PassengerCars(Car):
    pass


class CarFactory:
    types = {
        'trucks': Trucks,
        'passenger_cars': PassengerCars
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# категория
class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.cars = []

    def car_count(self):
        result = len(self.cars)
        if self.category:
            result += self.category.car_count()
        return result


# основной интерфейс проекта
class Engine:
    def __init__(self):
        self.admins = []
        self.clients = []
        self.cars = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_car(type_, name, category):
        return CarFactory.create(type_, name, category)

    def get_car(self, name):
        for item in self.cars:
            if item.name == name:
                return item
        return None

    def get_client(self, name) -> Client:
        for item in self.clients:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)
