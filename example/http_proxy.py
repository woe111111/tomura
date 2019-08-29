from tomura.app import Tomura

from tomura.parse import ParseHeader, ParseConetet

server = Tomura("http_proxy")

import asyncio


@server.node("header")
async def header(main):
    data = main.data

    if main.context.get("dis_reader"):
        return {
            "content": data
        }

    p = ParseHeader(data.decode())
    try:
        temp = p.headers.get("Host").split(":")
    except:
        temp = [p.path.split(":")[-2].replace("/", "")]
    host = temp[0]
    try:
        port = temp[1]
    except:
        if "https" in p.path or "443" in p.path:
            port = 443
        else:
            port = 80

    if port == 443:
        raise Exception("not support https")
    else:
        return {
            "host": host,
            "port": port,
            "content": data
        }


@server.node("result")
async def res(header):
    """

    :param header:
    :return:
    """
    data = header.data

    if header.context.get("dis_reader") is None:
        header.context["dis_reader"], header.context["dis_writer"] = await asyncio.open_connection(
            data.get("host"), data.get("port"))

    writer = header.context["dis_writer"]
    reader = header.context["dis_reader"]

    writer.write(data.get("content"))
    await writer.drain()
    res = b''
    while True:
        try:
            temp = await asyncio.wait_for(reader.read(2048), 1)
            res += temp
            if temp == b'':
                break
        except:
            break
    return res


@server.node("parse")
async def parse(result):

    return result


if __name__ == '__main__':
    server.run("0.0.0.0", 8887)
