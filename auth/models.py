import uuid

import asyncpg
from aiohttp import web
import json


class User():

    def __init__(self, data, **kw):
        print(data)
        self.id = data.get('id')
        self.nickname = data.get('nickname')
        self.password = data.get('password')
        self.blocked = data.get('blocked')
        self.favorites = data.get('favorites')

    async def check_user(self, **kw):
        try:
            conn = await asyncpg.connect(user='postgres', password='1234',
                                         database='recipe', host='127.0.0.1')
            values = await conn.fetch('''SELECT * FROM public.users WHERE nickname = $1 and password = $2;''', self.nickname, self.password)
            print(values)
            self.id = str(values[0]['id'])
            self.blocked = values[0]['blocked']
            self.favorites = values[0]['favorites']
            await conn.close()
            answer = {}
            if self.id:
                print('id detected')
                answer['id'] = self.id
            else:
                answer['error'] = 'Проверьте правильность ввода'
        except Exception as e:
            # Bad path where name is not set
            response_obj = {'status': 'failed', 'reason': str(e)}
            # return failed with a status code of 500 i.e. 'Server Error'
            return web.Response(text=json.dumps(response_obj), status=500)
        return answer

    async def get_login(self, **kw):
        user = await self.collection.find_one({'_id': ObjectId(self.id)})
        return user.get('login')

    async def create_user(self, **kw):
        user = await self.check_user()
        if not user:
            try:
                print("Creating new user with name: ", user)
                conn = await asyncpg.connect(user='postgres', password='1234',
                                             database='recipe', host='127.0.0.1')
                self.id = uuid.uuid1()
                self.blocked = False
                self.favorites = []
                values = await conn.execute('''INSERT INTO public.users(
                            id, nickname, blocked, favorites, password)
                            VALUES ($1, $2, $3, $4);
                        ''', self.id, self.nickname, self.blocked, self.favorites, self.password)
                print(str(values))
                response_obj = {}
                if str(values) is 'INSERT 0 1':
                    response_obj['id'] = self.id
                await conn.close()
            except Exception as e:
                # Bad path where name is not set
                print(e)
                response_obj = {'status': 'failed', 'reason': str(e)}
                # return failed with a status code of 500 i.e. 'Server Error'
                return web.Response(text=json.dumps(response_obj), status=500)

            else:
                response_obj = 'User exists'
        return response_obj
