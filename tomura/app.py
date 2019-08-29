import asyncio
import inspect
from queue import Queue

from tomura.graphics import Graphics
from tomura.utils import get_logger


class Tomura:

    def __init__(self, name, pool_size=500):
        self.logger = get_logger(name)
        self.pool_size = pool_size
        self.queue = Queue(pool_size)

        for i in range(pool_size):
            graphics = Graphics()
            graphics.add_node(name="main", func=None)

            self.queue.put_nowait(graphics)

    def node(self, name):
        def decorator(func):
            res = inspect.getargs(func.__code__)
            for i in range(self.pool_size):
                graphics = self.queue.get_nowait()
                graphics.add_node(name=name, parents=list(res.args), func=func)
                self.queue.put_nowait(graphics)

        return decorator

    def run(self, ip, port):
        async def handle_echo(reader, writer):
            graphics = self.queue.get_nowait()
            count = 0
            try:
                while True:
                    count = count + 1
                    data = b''
                    try:
                        data = await asyncio.wait_for(reader.read(2048), 1)
                        if count == 1:
                            graphics.context["src_reader"] = reader
                            graphics.context["src_writer"] = writer
                    except:
                        if data == b'':
                            break
                        await asyncio.sleep(0.1)
                        continue

                    finally:
                        graphics.nodes["main"].data = data
                        await graphics.run()
                        res = graphics.nodes['result'].data
                        writer.write(res)
                        await writer.drain()
                        graphics.clear()
                        if data == b'':
                            break

            except Exception as e:
                self.logger.exception("致命错误")
                print(e)
            finally:

                for key, value in graphics.context.items():
                    if "writer" in key:
                        value.close()
                    del value
                graphics.context = {}
                graphics.clear()
                self.queue.put_nowait(graphics)
                # writer.close()

        async def main():
            server = await asyncio.start_server(
                handle_echo, ip, port)

            addr = server.sockets[0].getsockname()
            print(f'Serving on {addr}')

            async with server:
                await server.serve_forever()

        asyncio.run(main())

    async def forward(self, reader, writer, res):

        writer.write(res.encode("utf-8"))

        res = await reader.readuntil()

        await writer.drain()

        return res
