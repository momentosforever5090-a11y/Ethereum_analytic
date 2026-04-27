from dash import Input, Output, html
from flask_login import current_user

def register_callbacks(dash_app):
    def update_greeting(_):
        if current_user.is_authenticated:
            return html.Div([
                html.Span(f'👋 Bienvenido, {current_user.username}!', 
                          style={'fontWeight': 'bold', 'fontSize': '20px'}),
                html.Br(),
                html.Small('Este es tu panel de control personalizado')
            ])
        return html.Div('⚠️ No autenticado', style={'color': 'red'})
    
    # Registro explícito, sin decorador
    dash_app.callback(
        Output('user-greeting', 'children'),
        Input('user-greeting', 'id')
    )(update_greeting)
