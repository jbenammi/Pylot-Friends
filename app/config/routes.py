from system.core.router import routes

routes['default_controller'] = 'Friends'
routes['POST']['/login'] = 'Friends#login'
routes['POST']['/register'] = 'Friends#register'
routes['GET']['/logout'] = 'Friends#logout'
routes['GET']['/view_friends'] = 'Friends#view_friends'
routes['GET']['/add/<id>'] = 'Friends#add_friends'
routes['GET']['/remove/<id>'] = 'Friends#remove_friends'
routes['GET']['/user/<id>'] = 'Friends#get_users'