"""
This module takes care of starting the API Server, loading the DB, and adding the endpoints.
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Product, Ingredient, ProductIngredient, Favorites, Order
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import datetime

# Create a Blueprint for the API
api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# ----------- Endpoints for User Management ----------- #

@api.route('/users', methods=['GET'])
def get_users():
    """Fetch all users."""
    users = User.query.all()
    users = [user.serialize() for user in users]
    if users:
        return jsonify({'users': users}), 200
    return jsonify({'msg': 'No se ha encontrado ningun usuario. Disculpen las molestias.'}), 404

@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """Fetch a specific user by ID."""
    user = User.query.get(id)
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    return jsonify(user.serialize()), 200

@api.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json()
    required_fields = ['name', 'full_name', 'telephone', 'address', 'email', 'password']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'msg': 'Todos los campos son obligatorios'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'msg': 'Ya estas registrado'}), 400
    
    try:
        registation_date = datetime.strptime(registation_date_str, "%d-%m-%Y")
        print(registation_date)
    except ValueError:
        return jsonify({"success": False, "msg": "Fecha de publicación no válida"}), 400

    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    access_token = create_access_token(identity=new_user.id)
    return jsonify(new_user.serialize()), 201

@api.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    """Update a user's information."""
    user = User.query.get(id)
    user_id = get_jwt_identity()

    if user_id != user.id:
        return jsonify({"success": False, "msg": "No tienes permiso para modificar este usuario"}), 403

    if not user:
        return jsonify({"success": False, "msg": "Usuario no encontrado"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "msg": "Datos faltantes"}), 400
    
    for key, value in data.items():
        setattr(user, key, value)

    try:
        db.session.commit()
        return jsonify(user.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al actualizar el usuario", "error": str(e)}), 500

@api.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    """Delete a user by ID."""
    user = User.query.get(id)
    if not user:
        return jsonify({'msg': 'Usuario no encontrado'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 204

# ----------- Endpoints for Product Management ----------- #

@api.route('/products', methods=['GET'])
def get_products():
    """Fetch all products."""
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])

@api.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    """Fetch a specific product by ID."""
    product = Product.query.get(id)
    if not product:
        return jsonify({'msg': 'Producto no encontrado'}), 404
    return jsonify(product.serialize()), 200

@api.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    """Create a new product."""
    data = request.get_json()
    new_product = Product(name=data['name'])  
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.serialize()), 201

@api.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    """Update a product's information."""
    product = Product.query.get(id)
    if not product:
        return jsonify({'msg': 'Producto no encontrado'}), 404

    data = request.get_json()
    product.name = data['name']  
    db.session.commit()
    return jsonify(product.serialize()), 200

@api.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    """Delete a product by ID."""
    product = Product.query.get(id)
    if not product:
        return jsonify({'msg': 'Producto no encontrado'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 204

# ----------- Endpoints for Ingredient Management ----------- #

@api.route('/ingredients', methods=['GET'])
def get_ingredients():
    """Fetch all ingredients."""
    ingredients = Ingredient.query.all()
    return jsonify([ingredient.serialize() for ingredient in ingredients])

@api.route('/ingredients/<int:id>', methods=['GET'])
def get_ingredient(id):
    """Fetch a specific ingredient by ID."""
    ingredient = Ingredient.query.get(id)
    if not ingredient:
        return jsonify({'msg': 'Ingrediente no encontrado'}), 404
    return jsonify(ingredient.serialize()), 200

@api.route('/ingredients', methods=['POST'])
@jwt_required()
def create_ingredient():
    """Create a new ingredient."""
    data = request.get_json()
    new_ingredient = Ingredient(name=data['name'])
    db.session.add(new_ingredient)
    db.session.commit()
    return jsonify(new_ingredient.serialize()), 201

@api.route('/ingredients/<int:id>', methods=['PUT'])
@jwt_required()
def update_ingredient(id):
    """Update an ingredient's information."""
    ingredient = Ingredient.query.get(id)
    if not ingredient:
        return jsonify({'msg': 'Ingrediente no encontrado'}), 404

    data = request.get_json()
    ingredient.name = data['name']  
    db.session.commit()
    return jsonify(ingredient.serialize()), 200

@api.route('/ingredients/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ingredient(id):
    """Delete an ingredient by ID."""
    ingredient = Ingredient.query.get(id)
    if not ingredient:
        return jsonify({'msg': 'Ingrediente no encontrado'}), 404

    db.session.delete(ingredient)
    db.session.commit()
    return jsonify({'message': 'Ingredient deleted'}), 204

# ----------- Endpoints for Product Ingredients ----------- #

@api.route('/products/<int:product_id>/ingredients', methods=['GET'])
def get_product_ingredients(product_id):
    """Fetch all ingredients for a specific product."""
    product = Product.query.get_or_404(product_id)
    ingredients = product.ingredients 
    return jsonify([ingredient.serialize() for ingredient in ingredients])

@api.route('/products/<int:product_id>/ingredients', methods=['POST'])
@jwt_required()
def add_product_ingredient(product_id):
    """Add an ingredient to a specific product."""
    product = Product.query.get(product_id)
    data = request.get_json()
    ingredient = Ingredient.query.get(data['ingredient_id'])
    
    if not ingredient:
        return jsonify({'msg': 'Ingrediente no encontrado'}), 404
    
    product.ingredients.append(ingredient)
    db.session.commit()
    return jsonify({'message': 'Ingredient added to product'}), 201

@api.route('/products/<int:product_id>/ingredients/<int:ingredient_id>', methods=['DELETE'])
@jwt_required()
def remove_product_ingredient(product_id, ingredient_id):
    """Remove an ingredient from a specific product."""
    product = Product.query.get(product_id)
    ingredient = Ingredient.query.get(ingredient_id)
    
    if not ingredient or ingredient not in product.ingredients:
        return jsonify({'msg': 'Ingrediente no encontrado en el producto'}), 404

    product.ingredients.remove(ingredient)
    db.session.commit()
    return jsonify({'message': 'Ingredient removed from product'}), 204
