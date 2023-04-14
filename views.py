from framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


class ContactUs:
    def __call__(self, request):
        return '200 OK', render('contact.html', address=request.get('address', None))
