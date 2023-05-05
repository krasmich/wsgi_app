from datetime import date

from views import Index, ContactUs, CategoryList, CreateCategory, CreateCars, CarsList, CopyCars


def date_front(request):
    request['date'] = date.today()


def address_front(request):
    request['address'] = 'г. Самара ул. Ново-Садова 11, тел. 888-777'


fronts = [date_front, address_front]

routes = {
    '/': Index(),
    '/contact/': ContactUs(),
    '/cars-list/': CarsList(),
    '/create-car/': CreateCars(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/copy-car/': CopyCars()
}
