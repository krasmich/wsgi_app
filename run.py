from wsgiref.simple_server import make_server

from framework.main import App
from urls import fronts
from views import routes

application = App(routes, fronts)

with make_server('', 8070, application) as httpd:
    print("Запуск проекта на порту 8070...")
    httpd.serve_forever()
