import os
import threading
import asyncio

from yaml import Loader
from yaml import load

from aiohttp import web, ClientSession



class Storage:

    def __init__(self):
        with open("config.yaml", "r") as f:
            data = f.read()
        self._config = load(data, Loader=Loader)
        self._host = self._config['host']
        self._port = self._config['port']
        self._dir = self._config['dir']
        self._others = self._config['others']
        self._save_from_others = self._config['save_from_others']

    async def _find(self, request):
        file = request.match_info.get('file')
        if file in os.listdir(self._dir):
            thread = threading.Thread(target=self._read_file, args=(file, ))
            thread.start()
            thread.join()
            return web.Response(text=self.read_response)
        else:
            thread = threading.Thread(target=self._async_find, args=(file, ))
            thread.start()
            thread.join()
            if self.friendly_find_response:
                return web.Response(text=self.friendly_find_response)
            raise web.HTTPNotFound()

    async def _find_silently(self, request):
        file = request.match_info.get('file')
        if file in os.listdir(self._dir):
            thread = threading.Thread(target=self._read_file, args=(file, ))
            thread.start()
            thread.join()
            return web.Response(text=self.read_response)
        else:
            raise web.HTTPNotFound()

    def _async_find(self, file):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = asyncio.gather(*[self._ask_others(
            "http://{}:{}/find/{}".format(node['host'], node['port'], file))
            for node in self._others.values()])
        responses = loop.run_until_complete(tasks)
        loop.close()
        self.friendly_find_response = None
        for response in responses:
            if response != 'False':
                if self._save_from_others:
                    thread = threading.Thread(target=self._save_file, args=(file,))
                    thread.start()
                    thread.join()
                self.friendly_find_response = response

    @staticmethod
    async def _fetch(session, url):
        async with session.get(url) as response:
            return await response.text()

    async def _ask_others(self, url):
        async with ClientSession() as session:
            return await self._fetch(session, url)

    def _read_file(self, file):
        with open(os.path.join(self._dir, file), "r") as f:
            self.read_response = f.read()

    def _save_file(self, file):
        with open(os.path.join(self._dir, file), "w") as f:
            f.write(file)

    def run(self):
        app = web.Application()
        app.add_routes([
            web.get('/{file}', self._find),
            web.get('/find/{file}', self._find_silently),
        ])
        web.run_app(app, host=self._host, port=int(self._port))



if __name__ == '__main__':
    Storage().run()
