import datetime

data = {}
data['key'] = datetime.datetime.now()
print(data)
#<link rel="icon" type="image/png" href="{{ static(images/icons/favicon.ico) }}"/>

app.router.add_post('/signup', reqSQL.signup)
app.router.add_get('/user', reqSQL.user)
app.router.add_get('/recipes', reqSQL.listrec)
app.router.add_get('/users', reqSQL.listusers)
app.router.add_get('/recipes/filter', reqSQL.filterRecipes)
app.router.add_put('/recipes', reqSQL.chooseFavorites)
app.router.add_get('/popular', reqSQL.showFavorites)
app.router.add_put('/recipes/add', reqSQL.addRecipe)
app.router.add_put('/recipes/update', reqSQL.updateRecipe)
app.router.add_get('/recipes/my', reqSQL.userRecipe)

< !-- < img src = "{{ static(images/img-01.png) }}" alt = "IMG" > -->

< !-- < link
rel = "icon"
type = "image/png"
href = "{{ static(images/icons/favicon.ico) }}" / > -->

	<link rel="stylesheet" type="text/css" href="{{ static(vendor/bootstrap/css/bootstrap.min.css) }}">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="{{ static(fonts/font-awesome-4.7.0/css/font-awesome.min.css) }}">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="{{ static(vendor/animate/animate.css) }}">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="{{ static(vendor/css-hamburgers/hamburgers.min.css) }}">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="{{ static(vendor/select2/select2.min.css) }}">