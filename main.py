#coding:utf-8
import web
from web.wsgiserver import CherryPyWSGIServer
from medication import Medication

CherryPyWSGIServer.ssl_certificate = "/opt/certificate/*.crt"
CherryPyWSGIServer.ssl_private_key = "/opt/certificate/*.key"

urls = (
    '', 'index',
    '/medication/(.+)', 'Medication'
)

class index:
    def GET(self):
        return "Hello, world!"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
    
