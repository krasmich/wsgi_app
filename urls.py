from datetime import date

from views import Index, ContactUs


def date_front(request):
    request['date'] = date.today()


def address_front(request):
    request['address'] = 'г. Самара ул. Ново-Садова 11, тел. 888-777'


fronts = [date_front, address_front]

routes = {
    '/': Index(),
    '/contact/': ContactUs()
}
