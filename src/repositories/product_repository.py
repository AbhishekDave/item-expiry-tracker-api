# src/repositories/product_repository.py

from src.models.grocery_models.product_model import Product


class ProductRepository:
    def __init__(self, db):
        self.db = db

    def add_product(self, product_data):
        self.db.session.add(product_data)
        self.db.session.commit()

    def get_all_products(self):
        return self.db.session.query(Product).all()
