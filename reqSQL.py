import datetime
from aiohttp import web
import asyncpg
import uuid
import json

async def run():
    conn = await asyncpg.connect(user='postgres', password='1234',
                                 database='recipe', host='127.0.0.1')
async def signup(request):
    try:
        # happy path where name is set
        user = request.query['name']
        # Process our new user
        print("Creating new user with name: ", user)
        conn = await asyncpg.connect(user='postgres', password='1234',
                                     database='recipe', host='127.0.0.1')
        uid = uuid.uuid1()
        await conn.execute('''
                INSERT INTO public.users(
        	        id, nickname, blocked, favorites)
        	        VALUES ($1, $2, $3, $4);
                ''', uid, user, False, [])
        values = await conn.fetch('''SELECT * FROM users where id=$1''', uid)
        print(values)
        response_obj = {'status': 'success', 'answer': str(values)}
        # return a success json response with status code 200 i.e. 'OK'
        await conn.close()
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        # Bad path where name is not set
        print(e)
        response_obj = {'status': 'failed', 'reason': str(e)}
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)

async def user(request):
    try:
        # happy path where name is set
        user = request.query['name']
        # Process our new user
        print("Creating new user with name: ", user)
        conn = await asyncpg.connect(user='postgres', password='1234',
                                     database='recipe', host='127.0.0.1')
        counts = await conn.fetch('''SELECT count(rid) FROM public.recipes WHERE author = (SELECT id FROM public.users WHERE nickname = $1);''', user)
        #print(values['id'])
        print(counts.count)
        counts = counts[0]['count']
        values = await conn.fetch('''SELECT id, nickname, blocked, favorites FROM public.users WHERE nickname = $1;''', user)
        values = {'id' : str(values[0]['id']), 'nickname' : values[0]['nickname'], 'blocked' : values[0]['blocked'], 'favorites' : values[0]['favorites'], 'count_recipes' : str(counts)}
        response_obj = {'status': 'success', 'answer': values}
        print(values)
        # return a success json response with status code 200 i.e. 'OK'
        await conn.close()
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'reason': str(e)}
        print("reason: "+str(e))
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)

async def listrec(request):
    try:
        # happy path where name is set
        user = request.query['name']
        # Process our new user
        print("Creating new user with name: ", user)
        conn = await asyncpg.connect(user='postgres', password='1234',
                                     database='recipe', host='127.0.0.1')
        values = await conn.fetch('''SELECT * FROM public.recipes WHERE author = (SELECT id FROM public.users WHERE nickname = $1);''', user)
        items = []
        for row in values:
            print(row)
            items.append({'rid': str(row['rid']), 'rname': row['rname'], 'description': row['description'], 'steps': row['steps'], 'type': row['type'], 'author': str(row['author']), 'likes': row['likes'], 'hashtags': row['hashtags'], 'blocked': row['blocked'], 'creation_date': str(row['creation_date']), 'photo': row['photo']})
        print(items)
        response_obj = {'status': 'success', 'answer': items}
        # return a success json response with status code 200 i.e. 'OK'
        await conn.close()
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'reason': str(e)}
        print("reason: "+str(e))
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)

async def listusers(request):
    try:
        conn = await asyncpg.connect(user='postgres', password='1234',
                                     database='recipe', host='127.0.0.1')
        values = await conn.fetch('''SELECT * FROM public.users;''')
        response_obj = {'status': 'success', 'answer': str(values)}
        print(values)
        # return a success json response with status code 200 i.e. 'OK'
        await conn.close()
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'reason': str(e)}
        print("reason: "+str(e))
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)

async def filter_recipe_by_name(request):
    try:
        filter_name = request.query['name']
        conn = await asyncpg.connect(user='postgres', password='1234',
                                     database='recipe', host='127.0.0.1')
        values = await conn.fetch('''SELECT * FROM public.recipes WHERE rname LIKE '%$1%';''',filter_name)
        items = []
        for row in values:
            print(row)
            items.append({'rid': str(row['rid']), 'rname': row['rname'], 'description': row['description'], 'steps': row['steps'], 'type': row['type'], 'author': str(row['author']), 'likes': row['likes'], 'hashtags': row['hashtags'], 'blocked': row['blocked'], 'creation_date': str(row['creation_date']), 'photo': row['photo']})
        print(items)
        response_obj = {'status': 'success', 'answer': items}
        # return a success json response with status code 200 i.e. 'OK'
        await conn.close()
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'reason': str(e)}
        print("reason: "+str(e))
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)

async def filter_recipe(request):
    try:
        conn = await asyncpg.connect(user='postgres', password='1234',
                                     database='recipe', host='127.0.0.1')
        if('name' in request.query):
            filter_name = request.query['name']
            print(filter_name)
            values = await conn.fetch('''SELECT * FROM public.recipes WHERE rname LIKE $1;''', '%'+filter_name+'%')
        if ('type' in request.query):
            filter_name = request.query['type']
            values = await conn.fetch('''SELECT * FROM public.recipes WHERE type = $1;''', filter_name)
        if ('hashtag' in request.query):
            filter_name = request.query['hashtag']
            values = await conn.fetch('''SELECT * FROM public.recipes WHERE hashtags LIKE '$1';''', filter_name)
        if(not 'name' in request.query and not 'type' in request.query and not 'hashtag' in request.query):
            values = await conn.fetch('''SELECT * FROM public.recipes;''')

        items = []
        for row in values:
            print(row)
            items.append({'rid': str(row['rid']), 'rname': row['rname'], 'description': row['description'], 'steps': row['steps'], 'type': row['type'], 'author': str(row['author']), 'likes': row['likes'], 'hashtags': row['hashtags'], 'blocked': row['blocked'], 'creation_date': str(row['creation_date']), 'photo': row['photo']})
        print(items)
        response_obj = {'status': 'success', 'answer': items}
        # return a success json response with status code 200 i.e. 'OK'
        await conn.close()
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'reason': str(e)}
        print("reason: "+str(e))
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)

async def filterRecipes(request):
    try:
        conn = await asyncpg.connect(user='postgres', password='1234',
                                     database='recipe', host='127.0.0.1')
        if('name' in request.query):
            filter_name = request.query['name']
            print(filter_name)
            values = await conn.fetch('''SELECT * FROM public.recipes WHERE rname LIKE $1;''', '%'+filter_name+'%')
        if ('type' in request.query):
            filter_name = request.query['type']
            values = await conn.fetch('''SELECT * FROM public.recipes WHERE type = $1;''', filter_name)
        if ('hashtag' in request.query):
            filter_name = request.query['hashtag']
            values = await conn.fetch('''SELECT * FROM public.recipes WHERE hashtags LIKE '$1';''', filter_name)
        if(not 'name' in request.query and not 'type' in request.query and not 'hashtag' in request.query):
            values = await conn.fetch('''SELECT * FROM public.recipes;''')

        items = []
        for row in values:
            print(row)
            items.append({'rid': str(row['rid']), 'rname': row['rname'], 'description': row['description'], 'steps': row['steps'], 'type': row['type'], 'author': str(row['author']), 'likes': row['likes'], 'hashtags': row['hashtags'], 'blocked': row['blocked'], 'creation_date': str(row['creation_date']), 'photo': row['photo']})
        print(items)
        response_obj = {'status': 'success', 'answer': items}
        # return a success json response with status code 200 i.e. 'OK'
        await conn.close()
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'reason': str(e)}
        print("reason: "+str(e))
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)

async def chooseFavorites(request):
    #дописать лайки
    try:
        conn = await asyncpg.connect(user='postgres', password='1234',
                                     database='recipe', host='127.0.0.1')
        if 'user'in request.query and 'recipe' in request:
            user, recipe = request.query['user'], request.query['recipe']
            print(user+" "+recipe)
            json_values = await conn.fetch('''SELECT favorites FROM public.users WHERE id = $1;''', user)
            print(json_values)
            if json_values[0]['favorites'] is None:
                print("none")
                recipe = [str(recipe)]
                print(recipe)
                values = await conn.execute('''UPDATE public.users
                                                    SET favorites = $1
                                                    WHERE id = $2;''', recipe, str(user))
            if json_values[0]['favorites'] is not None:
                print("NOT none")
                items = []
                for row in json_values:
                    print(row)
                    print(" "+str(row['favorites'][0]))
                    for r in row['favorites']:
                        print("     "+str(r))
                        items.append(str(r))
                items.append(recipe)
                print("Not NONE: "+str(items))
                output = []
                for x in items:
                    if x not in output:
                        output.append(x)
                values = await conn.execute('''UPDATE public.users
                                                    SET favorites = $1
                                                    WHERE id = $2;''', output, str(user))
                print(values)
        response_obj = {'status': 'success', 'answer': "OK"}
        # return a success json response with status code 200 i.e. 'OK'
        await conn.close()
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'reason': str(e)}
        print("reason: "+str(e))
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)

async def showFavorites(request):
    try:
        conn = await asyncpg.connect(user='postgres', password='1234',
                                       database='recipe', host='127.0.0.1')
        user = ""
        if 'user' in request.query:
            user = request.query['user']
        values = await conn.fetch('''SELECT favorites FROM public.users WHERE id = $1;''', user)
        print(values)
        values = values[0]['favorites']
        print(str(values))
        favorites = []
        for item in values:
            favorites.append(str(item))
        print(favorites)
        for item in favorites:
            values = await conn.fetch('''SELECT * FROM public.recipes WHERE rid = $1;''', item)
            print(values)
        response_obj = {'status': 'success', 'answer': "OK"}
        # return a success json response with status code 200 i.e. 'OK'
        await conn.close()
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'reason': str(e)}
        print("reason: " + str(e))
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)

async def addRecipe(request):
    try:
        conn = await asyncpg.connect(user='postgres', password='1234',
                                       database='recipe', host='127.0.0.1')
        user = ""
        data = {}
        data['rid'] = str(uuid.uuid1())
        if 'rname' in request.query:
            data['rname'] = request.query['rname']
        if 'description' in request.query:
            data['description'] = request.query['description']
        if 'steps' in request.query:
            data['steps'] = request.query['steps']
        if 'type' in request.query:
            data['type'] = request.query['type']
        if 'author' in request.query:
            data['author'] = request.query['author']
        if 'photo' in request.query:
            data['photo'] = request.query['photo']
        if 'hashtags' in request.query:
            data['hashtags'] = request.query['hashtags']
        data['blocked'] = False
        data['creation_date'] = datetime.datetime.now()
        keys, values = _split_dict(data)
        sql = 'INSERT INTO recipes ({}) VALUES ({})'.format(
            ', '.join(keys),
            ', '.join(_placeholders(data)))
        print(sql)
        print(data)
        print(values)
        values = await conn.execute(sql, *values)
        print(values)
        response_obj = {'status': 'success', 'answer': str(values)}
        # return a success json response with status code 200 i.e. 'OK'
        await conn.close()
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'reason': str(e)}
        print("reason: " + str(e))
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)

async def updateRecipe(request):
    try:
        conn = await asyncpg.connect(user='postgres', password='1234',
                                       database='recipe', host='127.0.0.1')
        user = ""
        data = {}
        filter = {}
        if 'rid' in request.query:
            filter['rid'] = request.query['rid']
        if 'rname' in request.query:
            data['rname'] = request.query['rname']
        if 'description' in request.query:
            data['description'] = request.query['description']
        if 'steps' in request.query:
            data['steps'] = request.query['steps']
        if 'type' in request.query:
            data['type'] = request.query['type']
        if 'author' in request.query:
            data['author'] = request.query['author']
        if 'photo' in request.query:
            data['photo'] = request.query['photo']
        if 'hashtags' in request.query:
            data['hashtags'] = request.query['hashtags']
        if 'blocked' in request.query:
            data['blocked'] = request.query['blocked']
        keys, values = _split_dict(data)
        where_keys, where_vals = _split_dict(filter)
        up_keys, up_vals = _split_dict(data)
        changes = _pairs(up_keys, sep=', ')
        where = _pairs(where_keys, start=len(up_keys) + 1)
        sql = 'UPDATE recipes SET {} WHERE {}'.format(
            changes, where)
        print(sql)
        print(changes, where)
        values = up_vals + where_vals
        print(values)
        values = await conn.execute(sql, *values)
        print(values)
        response_obj = {'status': 'success', 'answer': str(values)}
        # return a success json response with status code 200 i.e. 'OK'
        await conn.close()
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'reason': str(e)}
        print("reason: " + str(e))
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)

async def userRecipe(request):
    try:
        conn = await asyncpg.connect(user='postgres', password='1234',
                                       database='recipe', host='127.0.0.1')
        if 'user' in request.query:
            data = request.query['user']
        values = await conn.fetch('''SELECT * FROM public.recipes WHERE author = $1;''', str(data))
        print(values)
        response_obj = {'status': 'success', 'answer': str(values)}
        # дописать JSON с ответа
        # return a success json response with status code 200 i.e. 'OK'
        await conn.close()
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'reason': str(e)}
        print("reason: " + str(e))
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)

def _placeholders(variables):
    return ['${}'.format(i) for i, _ in enumerate(variables, 1)]

def _split_dict(dic):
    keys = sorted(dic.keys())
    return keys, [dic[k] for k in keys]

def _pairs(keys, *, start=1, sep=' AND '):
    return sep.join('{}=${}'.format(k, i) for i, k in enumerate(keys, start))