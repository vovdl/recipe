from auth.views import Login, SignUp, SignOut


routes = [
    ('GET', '/',        SignUp,  'main'),
    ('*',   '/login',   Login,     'login'),
    ('*',   '/signup',   SignUp,     'signup'),
]
