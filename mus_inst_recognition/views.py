import os
import shutil
import uuid
import asyncio

from aiohttp import web
import aiohttp_jinja2

from recognition_tool.label_image import recognize_image

def redirect(request, router_name):
    url = request.app.router[router_name].url()
    raise web.HTTPFound(url)


class FromLocal(web.View):

    @aiohttp_jinja2.template('from_local.html')
    async def get(self):
        pass

    @aiohttp_jinja2.template('from_local.html')
    async def post(self):
        reader = await self.request.multipart()
        image = await reader.next()
        filename = image.filename
        dir_name = 'uploaded_data'
        sub_dir = str(uuid.uuid4())
        size = 0

        if filename == '':
            return {'not_choose_file': True}

        path_to_image_dir = os.path.join(os.getcwd() + f'/{dir_name}/{sub_dir}/')
        os.mkdir(path_to_image_dir)
        full_path_to_image = os.path.join(os.getcwd() + f'/{dir_name}/{sub_dir}/', filename)

        with open(full_path_to_image, 'wb+') as f:
            while True:
                chunk = await image.read_chunk()
                if not chunk:
                    break
                size += len(chunk)
                f.write(chunk)

        eval_time, recognized = recognize_image(
            path_to_image=f'{dir_name}/{sub_dir}/' + filename
        )
        # TODO: delete files from uploaded_data
        # shutil.rmtree(path_to_image_dir)
        print(recognized)
        return {'eval_time': eval_time, 'recognized': recognized,
                'image_path': f'{sub_dir}/{filename}'}


class ByLink(web.View):

    @aiohttp_jinja2.template('by_link.html')
    async def get(self):
        pass
