import os
from flask_admin import Admin
from models import db, User,Planet, Character, Favorite
from flask_admin.contrib.sqla import ModelView

class UserView(ModelView):
    column_list=["id","username","password","email","created","edited","favorites"]

class CharacterView(ModelView):
    column_list=["id","name","eye_color","gender","hair_color","created","edited","favorites"]

class PlanerView(ModelView):
    column_list=["id","name","diameter","climate","terrain","created","edited","favorites"]

class FavoriteView(ModelView):
    column_list=["id","user_id","character_id","planet_id","created","user","character","planet"]

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserView(User, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))