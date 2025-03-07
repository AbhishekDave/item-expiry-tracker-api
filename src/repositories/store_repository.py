# src/repositories/store_repository.py

from src.models.grocery_models.store_model import Store


class StoreRepository:
    def __init__(self, db):
        self.db = db

    def add_store(self, store_data):
        self.db.session.add(store_data)
        self.db.session.commit()

    def get_all_store(self):
        return self.db.session.query(Store).all()
