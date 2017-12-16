import asyncio

from aiohttp import web
import aiohttp_jinja2
import jinja2

from routes import routes

loop = asyncio.get_event_loop()

app = web.Application(loop=loop)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.router.add_static('/static', 'static', name='static')
app.router.add_static('/media', 'uploaded_data', name='media')

for route in routes:
    app.router.add_route(route[0], route[1], route[2], name=route[3])

web.run_app(app, host='127.0.0.1', port=8080)
