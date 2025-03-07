# src/repositories/grocery_item_repository.py
from src.models.mapping_models.store_product_mapping_model import StoreProductMapping


class StoreProductMappingRepository:
    def __init__(self, db):
        self.db = db

    def add_product(self, store_product_mapping_data):
        self.db.session.add(store_product_mapping_data)
        self.db.session.commit()

    def get_all_store_product_information(self):
        return self.db.session.query(StoreProductMapping).all()
