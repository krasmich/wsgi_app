from wsgiref.simple_server import make_server

from framework.main import App
from urls import routes, fronts


application = App(routes, fronts)

with make_server('', 8080, application) as httpd:
    print("Запуск проекта на порту 8080...")
    httpd.serve_forever()
