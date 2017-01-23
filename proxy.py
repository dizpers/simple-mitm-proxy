import io

import asyncio

from urllib.parse import urljoin

import aiohttp
from aiohttp import web


async def proxy_handler(request):
    target_url = urljoin('https://habrahabr.ru', request.path)

    request_headers = dict(request.headers)
    request_headers['Host'] = 'habrahabr.ru'
    request = request.clone(headers=request_headers)

    async with aiohttp.ClientSession() as session:
        response = await session.get(target_url, headers=request_headers)

        # Build proxy response headers
        exclude_headers = ('Content-Encoding', 'Content-Length')
        # exclude_headers = tuple()
        proxy_response_headers = {k: v for k, v in response.headers.items() if k not in exclude_headers}

        proxy_response = web.StreamResponse(
            status=response.status,
            reason=response.reason,
            headers=proxy_response_headers
        )

        await proxy_response.prepare(request)

        while True:
            chunk = await response.content.read(io.DEFAULT_BUFFER_SIZE)
            if not chunk:
                break
            proxy_response.write(chunk)
            await proxy_response.drain()

        await proxy_response.write_eof()

    return proxy_response


if __name__ == '__main__':
    proxy_server = web.Server(proxy_handler)

    loop = asyncio.get_event_loop()
    f = loop.create_server(proxy_server, '0.0.0.0', 8080)
    srv = loop.run_until_complete(f)

    print('Proxy is listening on', srv.sockets[0].getsockname())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.close()
