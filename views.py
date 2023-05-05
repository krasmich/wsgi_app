from framework.templator import render
from patterns.сreational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


# контроллер - главная страница
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


# контроллер - "Для связи"
class ContactUs:
    def __call__(self, request):
        return '200 OK', render('contact.html', address=request.get('address', None))


# контроллер 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - список автомобилей
class CarsList:
    def __call__(self, request):
        logger.log('Список Автомобилей')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('car_list.html',
                                    objects_list=category.cars,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать автомобиль
class CreateCars:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                car = site.create_car('passenger_cars', name, category)
                site.cars.append(car)

            return '200 OK', render('car_list.html',
                                    objects_list=category.cars,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_car.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - создать категорию
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)


# контроллер - список категорий
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)


# контроллер - копировать автомобиль
class CopyCars:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_car = site.get_car(name)
            if old_car:
                new_name = f'copy_{name}'
                new_car = old_car.clone()
                new_car.name = new_name
                site.cars.append(new_car)

            return '200 OK', render('cars_list.html',
                                    objects_list=site.cars,
                                    name=new_car.category.name)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
