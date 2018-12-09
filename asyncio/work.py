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
        # print(self._others)

    # server part
    async def find(self, request):
        file = request.match_info.get('file')
        print('asking for %s', file)
        if file in os.listdir(self._dir):
            data = await self.read(file)
            return web.Response(text=data)
        else:       # ask others
            if self._others:
                data = [await self.ask_others(f'http://{node["host"]}:{node["port"]}/find/{file}')
                    for node in self._others.values()]
                #print('DATA',data)
                return web.Response(text=''.join(data))
            else:
                return web.Response(status=404)

            # return web.Response(status=404)

    async def read(self, file):
        async with aiofiles.open(self._dir+'/'+file, 'r') as f:
            content = await f.read()
            return content


    async def write(self, file, data):
        async with aiofiles.open(file, 'w') as f:
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
        app.add_routes([web.get('/find/{file}', self.find)])
        web.run_app(app, host=self._host, port=int(self._port))

def load(file):
    with open(file, "r") as f:
        data = f.read()
    return yaml.load(data)

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
