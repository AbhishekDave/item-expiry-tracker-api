# src/models/grocery_models/grocery_item_model.py

from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Index

from src.configs.development_config import db


class GroceryItem(db.Model):
    __tablename__ = 'grocery_item'

    id = db.Column(db.Integer, primary_key=True)
    grocery_list_name_id = db.Column(db.Integer, db.ForeignKey('grocery_list_name.id'), index=True)
    item_id = db.Column(db.Integer, db.ForeignKey('product.id'), index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now(ZoneInfo('UTC')))
    modified_at = db.Column(db.DateTime, default=datetime.now(ZoneInfo('UTC')), onupdate=datetime.now(ZoneInfo('UTC')))
