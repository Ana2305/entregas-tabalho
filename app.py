import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.user import db, User
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)

    @app.route('/')
    def home():
        return jsonify({"msg": "API Cannoli Dashboard rodando 🎉"})

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password') or not data.get('role'):
            return jsonify({"msg": "Dados incompletos"}), 400
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"msg": "Usuário já existe"}), 400
        
        new_user = User(username=data['username'], role=data['role'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "Usuário criado com sucesso"}), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({"msg": "Dados incompletos"}), 400

        user = User.query.filter_by(username=data['username']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({"msg": "Usuário ou senha incorretos"}), 401

        # Convertemos o identity em string JSON para evitar "Subject must be a string"
        user_identity = json.dumps({"username": user.username, "role": user.role})
        access_token = create_access_token(identity=user_identity)
        return jsonify(access_token=access_token), 200

    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        # Convertemos de volta a string JSON para dicionário
        current_user = json.loads(get_jwt_identity())
        return jsonify(logged_in_as=current_user), 200

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
