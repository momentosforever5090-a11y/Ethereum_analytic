from app import server  # 'server' es la instancia de Flask

if __name__ == '__main__':
    # Para producción con Gunicorn no se usa debug
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
