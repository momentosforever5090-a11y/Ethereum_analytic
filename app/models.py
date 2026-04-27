from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Base de datos simulada (puedes pasarla a config más adelante)
users_db = {
    'admin': {'password': 'user'},
    'user': {'password': 'pass'}
}
