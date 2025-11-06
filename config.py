import os

class Config:
    # Chaves secretas
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-muito-segura'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'chave-jwt-secreta'

    # Caminho absoluto da pasta onde está o arquivo config.py
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Caminho da pasta database
    DB_FOLDER = os.path.join(BASE_DIR, 'database')
    os.makedirs(DB_FOLDER, exist_ok=True)  # cria a pasta se não existir

    # Caminho completo do arquivo SQLite
    DB_PATH = os.path.join(DB_FOLDER, 'cannoli.db')

    # URI do SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
