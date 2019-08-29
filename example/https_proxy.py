from tomura.app import Tomura

from tomura.parse import ParseHeader, ParseConetet

server = Tomura("https_proxy")

import asyncio


@server.node("header")
async def header(main):
    data = main.data
    try:
        p = ParseHeader(data.decode())
    except Exception:
        return {
            "content": data
        }
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

    if port != 443:
        raise Exception("not support http")
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

        header.context['src_writer'].write(b"HTTP/1.0 200 Connection Established\r\n\r\n")
        await header.context['src_writer'].drain()
        res = b''

    else:
        header.context['dis_writer'].write(data.get("content"))
        await header.context['dis_writer'].drain()
        res = b''
        while True:
            try:
                temp = await asyncio.wait_for(header.context['dis_reader'].read(2048), 0.1)
                res += temp
                if temp == b'':
                    await asyncio.sleep(0.1)
                    break
            except Exception as e:
                await asyncio.sleep(0.1)
                break

    return res


@server.node("parse")
async def parse(result):
    # p = ParseConetet(result)
    return ""


if __name__ == '__main__':
    server.run("0.0.0.0", 8888)
