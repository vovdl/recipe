# -*- coding: utf-8 -*-
import asyncio
import aiohttp_jinja2
import jinja2
from aiohttp_session import session_middleware, setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp import web
from cryptography import fernet

import reqSQL, base64
from routes import routes
from middlewares import authorize


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')

fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)

middle = [
    session_middleware(EncryptedCookieStorage(secret_key)),
    authorize,
]

app = web.Application(middlewares=middle)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

for route in routes:
    app.router.add_route(route[0], route[1], route[2], name=route[3])
app['static_root_url'] = '/static'
app.router.add_static('/static', 'static', name='static')

#app.on_cleanup.append(on_shutdown)
#app['websockets'] = []

web.run_app(app)