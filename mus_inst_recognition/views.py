import os
import shutil
import uuid
import aiohttp

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
        return {'eval_time': eval_time, 'recognized': recognized,
                'image_path': f'{sub_dir}/{filename}'}


class ByLink(web.View):

    @aiohttp_jinja2.template('by_link.html')
    async def get(self):
        pass

    @aiohttp_jinja2.template('by_link.html')
    async def post(self):
        data = await self.request.post()
        url = data.get('image_url')
        chunk_size = 100
        filename = os.path.basename(url)
        dir_name = 'uploaded_data'  # TODO: make it global
        sub_dir = str(uuid.uuid4())

        if filename == '':
            return {'not_choose_file': True}

        path_to_image_dir = os.path.join(os.getcwd() + f'/{dir_name}/{sub_dir}/')
        os.mkdir(path_to_image_dir)
        full_path_to_image = os.path.join(os.getcwd() + f'/{dir_name}/{sub_dir}/', filename)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                with open(full_path_to_image, 'wb') as fd:
                    while True:
                        chunk = await resp.content.read(chunk_size)
                        if not chunk:
                            break
                        fd.write(chunk)

        eval_time, recognized = recognize_image(
            path_to_image=f'{dir_name}/{sub_dir}/' + filename
        )
        return {'eval_time': eval_time, 'recognized': recognized,
                'image_path': f'{sub_dir}/{filename}'}
