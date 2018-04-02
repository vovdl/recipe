import json
from time import time
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from auth.models import User


def redirect(request, router_name):
    url = request.app.router[router_name].url()
    raise web.HTTPFound(url)


def set_session(session, user_id, request):
    session['user'] = str(user_id)
    session['last_visit'] = time()
    redirect(request, 'main')


def convert_json(message):
    return json.dumps({'error': message})


class Login(web.View):

    @aiohttp_jinja2.template('auth/login.html')
    async def get(self):
        session = await get_session(self.request)
        print(session)
        if session.get('user'):
            redirect(self.request, 'main')
        return {'content': 'Please enter login or email'}

    async def post(self):
        data = await self.request.post()
        print(str(data))
        user = User(data)
        result = await user.check_user()
        if 'id' in result:
            print('Сессия ' + result['id'])
            session = await get_session(self.request)
            print(session)
            await set_session(session, str(result['id']), self.request)
        else:
            return web.Response(content_type='application/json', text=json.dumps(result))


class SignUp(web.View):

    @aiohttp_jinja2.template('auth/signup.html')
    async def get(self, **kw):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'main')
        return {'content': 'Please enter your data'}

    async def post(self, **kw):
        data = await self.request.post()
        print(str(data))
        user = User(data)
        result = await user.create_user()
        if 'id' in result:
            session = await get_session(self.request)
            set_session(session, str(result), self.request)
        else:
            return web.Response(content_type='application/json', text=convert_json(result))


class SignOut(web.View):

    async def get(self, **kw):
        session = await get_session(self.request)
        if session.get('user'):
            del session['user']
            redirect(self.request, 'login')
        else:
            raise web.HTTPForbidden(body=b'Forbidden')