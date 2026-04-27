from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from dash import Dash
from .config import Config
from .models import users_db, User
from .forms import LoginForm

# ------------------------------------------------------------
# 1. Crear la app Flask
# ------------------------------------------------------------
server = Flask(__name__)
server.config.from_object(Config)

# ------------------------------------------------------------
# 2. Configurar Flask-Login
# ------------------------------------------------------------
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = 'login'  # endpoint de la función login
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

@login_manager.user_loader
def load_user(user_id):
    if user_id in users_db:
        return User(user_id, user_id)
    return None

# ------------------------------------------------------------
# 3. Crear la app Dash y montarla en el servidor Flask
# ------------------------------------------------------------
dash_app = Dash(
    __name__,
    server=server,
    url_base_pathname='/dashboard/',
    assets_folder='static'   # para que Dash también sirva desde static si es necesario
)

# Importar el layout y los callbacks de Dash (los definiremos después)
from .dash_app.layout import create_dash_layout
from .dash_app.callbacks import register_callbacks

dash_app.layout = create_dash_layout()
register_callbacks(dash_app)

# ------------------------------------------------------------
# 4. Proteger todas las rutas que empiecen con /dashboard/
# ------------------------------------------------------------
@server.before_request
def protect_dash():
    if request.path.startswith('/dashboard/'):
        if not current_user.is_authenticated:
            # Guardar la URL a la que quería acceder para redirigir después del login
            return redirect(url_for('login', next=request.url))

# ------------------------------------------------------------
# 5. Rutas Flask (login, logout, home, etc.)
# ------------------------------------------------------------
@server.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in users_db and users_db[username]['password'] == password:
            user = User(username, username)
            login_user(user, remember=form.remember.data)
            flash('¡Sesión iniciada correctamente!', 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('dashboard_index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html', form=form)

@server.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))

@server.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_index'))
    return redirect(url_for('login'))

@server.route('/dashboard')
def dashboard_index():
    # Redirige a la URL base de Dash (con la barra final)
    return redirect('/dashboard/')
