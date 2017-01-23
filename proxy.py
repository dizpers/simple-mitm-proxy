import asyncio

from urllib.parse import urljoin

import aiohttp
from aiohttp import web


async def proxy(request):
    target_url = urljoin('https://habrahabr.ru', request.match_info['path'])

    request_headers = dict(request.headers)
    request_headers['Host'] = 'habrahabr.ru'
    print(request_headers)

    async with aiohttp.ClientSession() as session:
        async with session.get(target_url, headers=request_headers) as response:
            raw_text = await response.text()

    # No transformation for now
    text = raw_text

    # Build proxy response headers
    exclude_headers = ('Content-Encoding', 'Content-Length')
    proxy_response_headers = {k: v for k, v in response.headers.items() if k not in exclude_headers}

    proxy_response = web.Response(
        status=response.status,
        reason=response.reason,
        text=text,
        headers=proxy_response_headers,
    )

    del proxy_response.headers['Content-Length']

    return proxy_response


if __name__ == '__main__':
    app = web.Application()
    app.router.add_route('GET', '/{path:\w*}', proxy)

    loop = asyncio.get_event_loop()
    f = loop.create_server(app.make_handler(), '0.0.0.0', 8080)
    srv = loop.run_until_complete(f)

    print('Proxy is listening on', srv.sockets[0].getsockname())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
