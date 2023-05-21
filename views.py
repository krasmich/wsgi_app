from framework.templator import render
from patterns.architectural_pattern import UnitOfWork

from patterns.structural_patterns import AppRoute, Debug
from patterns.сreational_patterns import Engine, Logger, MapperRegistry
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, \
    ListView, CreateView, BaseSerializer

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


routes = {}


# контроллер - главная страница
@AppRoute(routes=routes, url='/')
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


# контроллер - "Для связи"
@AppRoute(routes=routes, url='/contact/')
class ContactUs:
    def __call__(self, request):
        return '200 OK', render('contact.html', address=request.get('address', None))


# контроллер 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - список автомобилей
@AppRoute(routes=routes, url='/cars-list/')
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
@AppRoute(routes=routes, url='/create-car/')
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

                car.observers.append(email_notifier)
                car.observers.append(sms_notifier)

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
@AppRoute(routes=routes, url='/create-category/')
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
@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)


# контроллер - копировать автомобиль
@AppRoute(routes=routes, url='/copy-course/')
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


@AppRoute(routes=routes, url='/client-list/')
class ClientListView(ListView):
    template_name = 'client_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('client')
        return mapper.all()


@AppRoute(routes=routes, url='/create-client/')
class ClientCreateView(CreateView):
    template_name = 'create_client.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('client', name)
        site.clients.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/add-client/')
class AddClientByCarCreateView(CreateView):
    template_name = 'add_client.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['cars'] = site.cars
        context['clients'] = site.clients
        return context

    def create_obj(self, data: dict):
        car_name = data['car_name']
        car_name = site.decode_value(car_name)
        car = site.get_car(car_name)
        client_name = data['client_name']
        client_name = site.decode_value(client_name)
        client = site.get_client(client_name)
        car.add_client(client)


@AppRoute(routes=routes, url='/api/')
class CarApi:
    @Debug(name='CarApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.cars).save()
