from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)  
    full_name = db.Column(db.String(40), nullable=False)
    telephone = db.Column(db.String(15), unique=True, nullable=False)
    address = db.Column(db.String(60), nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    is_active = db.Column(db.Boolean(), default=True) 

    orders = db.relationship('Order', back_populates='customer') 

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "telephone": self.telephone,
            "address": self.address,  
            "email": self.email,
            # No serializar la contraseña por motivos de seguridad
        }
    
class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    products = db.relationship('ProductIngredient', back_populates='ingredient')


    def __repr__(self):
        return f'<Ingredient {self.name}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'products': [pi.product.serialize() for pi in self.products]
        }

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    ingredients = db.relationship('ProductIngredient', back_populates='product')


    def __repr__(self):
        return f'<Product {self.name}>'
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "ingredients": [pi.ingredient.serialize() for pi in self.ingredients]
        }

class ProductIngredient(db.Model):
    __tablename__ = 'product_ingredients'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
    quantity = db.Column(db.String(50))
    product = db.relationship('Product', back_populates='ingredients')
    ingredient = db.relationship('Ingredient', back_populates='products')

    def __repr__(self):
        return f'<ProductIngredient {self.ingredient_id}>'
    
    def serialize(self):
        return {
            "product_id": self.product_id,
            "ingredient_id": self.ingredient_id,
            "ingredient_name": self.ingredient.name,  
            "quantity": self.quantity  
        }

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    quantity_items = (db.Column(db.Integer))
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float(), nullable=False)

    customer = db.relationship('User', back_populates='orders')

    def __repr__(self):
        return f'<Order {self.id}>'
    
    def serialize(self):
        return {
            "quantity_items": self.quantity_items,
            "customer_id": self.customer_id,
            "date": self.date,
            "total": self.total
        }
    
class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='favorites')
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    product = db.relationship('Product', backref='favorites')

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True)
    order = db.relationship('Order', backref='favorites')

    def __repr__(self):
        return f'<Favorites {self.user_id} - Product {self.product_id} - Order {self.order_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "order_id": self.order_id
        }

