# src/repositories/grocery_item_repository.py

from src.models.grocery_models.grocery_item_model import GroceryItem


class GroceryItemRepository:
    def __init__(self, db):
        self.db = db

    def add_grocery_item(self, grocery_item_data):
        self.db.session.add(grocery_item_data)
        self.db.session.commit()

    def get_all_grocery_items(self):
        return self.db.session.query(GroceryItem).all()
