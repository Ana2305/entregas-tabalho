from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db
from models.product import Product

product_bp = Blueprint('product', __name__, url_prefix='/products', strict_slashes=False)



# ========================
# GET - Listar produtos
# ========================
@product_bp.route('/', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'description': p.description
    } for p in products]), 200

# ========================
# GET - Produto específico
# ========================
@product_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    p = Product.query.get_or_404(id)
    return jsonify({
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'description': p.description
    }), 200

# ========================
# POST - Criar produto
# ========================
@product_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json() or {}
    name = data.get('name')
    price = data.get('price')
    description = data.get('description', '')

    if not name or price is None:
        return jsonify({"msg": "Dados incompletos"}), 400

    try:
        price = float(price)
    except (ValueError, TypeError):
        return jsonify({"msg": "Preço deve ser um número"}), 400

    p = Product(name=name, price=price, description=description)
    db.session.add(p)
    db.session.commit()
    return jsonify({"msg": "Produto criado", "id": p.id}), 201

# ========================
# PUT - Atualizar produto
# ========================
@product_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    p = Product.query.get_or_404(id)
    data = request.get_json() or {}

    if 'name' in data:
        p.name = data['name']
    if 'price' in data:
        try:
            p.price = float(data['price'])
        except (ValueError, TypeError):
            return jsonify({"msg": "Preço deve ser um número"}), 400
    if 'description' in data:
        p.description = data['description']

    db.session.commit()
    return jsonify({"msg": "Produto atualizado"}), 200

# ========================
# DELETE - Deletar produto
# ========================
@product_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    p = Product.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"msg": "Produto deletado"}), 200
