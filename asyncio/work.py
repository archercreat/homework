import asyncio
import os
import aiofiles
from aiohttp import web, ClientSession
import argparse
import yaml
import sys



class Daemon:
    def __init__(self, host: str, port: int, dir: str, others: dict, save: bool):
        self._host = host
        self._port = port
        self._dir = dir
        self._others = others
        self._save = save

    # server part
    async def find(self, request):
        file = request.match_info.get('file')
        print('looking for', file)
        if file in os.listdir(self._dir):
            data = await self.read(file)
            return web.Response(text=data)
        else:
            data = [await self.ask_others(f'http://{node["host"]}:{node["port"]}/lookup/{file}')
                    for node in self._others.values() if self._others]
            d = ''.join(data)
            if d:
                if self._save:
                    await self.write(file, d)
                return web.Response(text=d)
            return web.Response(status=404)

    async def lookup(self, request):
        file = request.match_info.get('file')
        print('lookup', file)
        if file in os.listdir(self._dir):
            data = await self.read(file)
            return web.Response(text=data)
        return web.Response(text='')

    async def read(self, file):
        async with aiofiles.open(os.path.join(self._dir, file), 'r') as f:
            content = await f.read()
            return content


    async def write(self, file, data):
        async with aiofiles.open(os.path.join(self._dir, file), 'w') as f:
            await f.write(data)

    # client part
    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def ask_others(self, url):
        async with ClientSession() as session:
            return await self.fetch(session, url)

    def run(self):
        app = web.Application()
        app.add_routes([web.get('/find/{file}', self.find),
                        web.get('/lookup/{file}', self.lookup)])
        web.run_app(app, host=self._host, port=int(self._port))

def load(file):
    with open(file, "r") as f:
        return yaml.load(f.read())

def parse_args(args):
    parser = argparse.ArgumentParser(description='Async File Storage')
    parser.add_argument('-c',
                        '--config',
                        action="store",
                        type=str,
                        default="config.yaml",
                        help='Config file')
    return parser.parse_args(args)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    conf = load(args.config)
    x = Daemon(**conf)
    x.run()
