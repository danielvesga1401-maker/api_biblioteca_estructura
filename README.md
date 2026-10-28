# API de Biblioteca

## Configurar
1. En pgAdmin crea una base de datos llamada `biblioteca_db`.
2. Copia `.env.example` a `.env` en la raíz.
3. Edita `.env` con la contraseña real de tu usuario PostgreSQL.
4. Instala dependencias: `py -m pip install -r requirements.txt`
5. Inicia: `py -m uvicorn main:app --reload`

Swagger: http://127.0.0.1:8000/docs
Comprobar conexión: http://127.0.0.1:8000/salud

Las tablas se crean al iniciar. Los datos de `biblioteca.db` (SQLite) no se copian automáticamente.
No subas `.env` a GitHub. Si publicaste una contraseña real, cámbiala.
