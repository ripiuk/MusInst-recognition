import asyncio

from aiohttp import web
import aiohttp_jinja2


def redirect(request, router_name):
    url = request.app.router[router_name].url()
    raise web.HTTPFound(url)


class FromLocal(web.View):

    @aiohttp_jinja2.template('from_local.html')
    async def get(self):
        print(self.request)


class ByLink(web.View):

    @aiohttp_jinja2.template('by_link.html')
    async def get(self):
        print(self.request)
