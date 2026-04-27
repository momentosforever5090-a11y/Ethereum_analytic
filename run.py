from app import server  # 'server' es la instancia de Flask creada en app/__init__.py

if __name__ == '__main__':
    server.run(debug=True)
