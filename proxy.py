import asyncio
import io
import re
from urllib.parse import urljoin

import aiohttp
from aiohttp import web


def modify(s):
    try:
        body_start_index = s.index('<body')
    except ValueError:
        body_start_index = 0
    try:
        body_end_index = s.index('</body>')
    except ValueError:
        body_end_index = len(s) - 1
    pre_body = s[:body_start_index]
    body = s[body_start_index:body_end_index]
    post_body = s[body_end_index:]
    split_parts = re.split(r'[>\s](\w{6})(?!([^<]+)?>)(?=[^\w])', body, flags=re.UNICODE)
    parts = []
    need_append = True
    forbidden_tags = ['<{0}{1}'.format(close, tag) for tag in ('script', 'style') for close in ('', '/')]
    for part in split_parts:
        if part is None:
            continue
        tags = {tag: part.rfind(tag) for tag in forbidden_tags}
        if not all([index == -1 for index in tags.values()]):
            need_append = '/' in max(tags, key=lambda item: tags[item])
        if need_append and len(part) == 6:
            part += '™'
        parts.append(part)
    body = ' '.join(parts)
    return pre_body + body + post_body


async def proxy_handler(request):
    target_url = urljoin('https://habrahabr.ru', request.path)

    request_headers = dict(request.headers)
    request_headers['Host'] = 'habrahabr.ru'

    async with aiohttp.ClientSession() as session:
        response = await session.get(target_url, headers=request_headers)

        # Build proxy response headers
        exclude_headers = ('Content-Encoding', )
        proxy_response_headers = {k: v for k, v in response.headers.items() if k not in exclude_headers}

        proxy_response = web.StreamResponse(
            status=response.status,
            reason=response.reason,
            headers=proxy_response_headers
        )

        await proxy_response.prepare(request)

        need_to_modify = response.content_type == 'text/html'

        while True:
            if need_to_modify:
                chunk = await response.content.read()
            else:
                chunk = await response.content.read(io.DEFAULT_BUFFER_SIZE)
            if not chunk:
                break
            if need_to_modify:
                chunk_str = chunk.decode(response.charset)
                chunk_str = modify(chunk_str)
                chunk = bytes(chunk_str, response.charset)
            proxy_response.write(chunk)
            await proxy_response.drain()

        await proxy_response.write_eof()
        await response.release()

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