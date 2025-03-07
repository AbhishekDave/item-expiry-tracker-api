# src/apis/grocery_api/grocery_api_get.py

from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import jwt_required

from src.configs.development_config import db
from src.models.grocery_models.grocery_item_model import GroceryItem
from src.models.grocery_models.grocery_list_name_model import GroceryListName
from src.models.grocery_models.product_model import Product
from src.models.grocery_models.store_model import Store
from src.models.mapping_models.store_product_mapping_model import StoreProductMapping

from src.services.user_services import UserService
from src.services.grocery_services import GroceryService
from src.services.serialization_services.grocery_serialization_service import GrocerySerializationService

grocery_name_get_api_bp = Blueprint('grocery_name_get_api', __name__)


@grocery_name_get_api_bp.route('/grocery-list-names', methods=['GET'])
@jwt_required()
def get_grocery_names():
    # Log the incoming request URL
    api_url = request.url
    current_app.logger.info(f"\nRequest URL: {api_url}")

    user_service = UserService(db)
    grocery_service = GroceryService(db)
    grocery_serialization_service = GrocerySerializationService()

    current_user_id = user_service.find_current_user_id()

    grocery_name_list = grocery_service.find_all_grocery_names_by_user_id(current_user_id)

    fields_to_exclude = []
    grocery_data_dump = grocery_serialization_service.serialize_grocery_names(grocery_name_list, fields=fields_to_exclude)

    return jsonify(grocery_data_dump)


@grocery_name_get_api_bp.route('/grocery-names/<int:grocery_name_id>/items', methods=['POST'])
@jwt_required()
def create_grocery_name(grocery_name_id):
    api_url = request.url
    current_app.logger.info(f"\nRequest URL: {api_url}")

    data = request.json

    user_id = UserService.find_current_user_id()

    # handle grocery name
    grocery_list_name = GroceryListName.query.filter_by(user_id=user_id, grocery_list_name=data['grocery-list-name']['name'])

    # Step 1: Handle Product
    product = Product.query.filter_by(name=data['product']['name']).first()
    if not product:
        product = Product(name=data['product']['name'],
                          product_type=data['product']['product_type'])
        db.session.add(product)
        db.session.commit()

    # Step 2: Handle Store
    store = Store.query.filter_by(name=data['store']['name']).first()
    if not store:
        store = Store(name=data['store']['name'],
                      description=data['store']['description'],
                      location=data['store']['location'])
        db.session.add(store)
        db.session.commit()

    # Step 3: Handle StoreProductMapping
    mapping = StoreProductMapping.query.filter_by(store_id=store.id,
                                                  product_id=product.id).first()
    if not mapping:
        mapping = StoreProductMapping(store_id=store.id,
                                      product_id=product.id,
                                      price=data['mapping']['price'],
                                      quantity=data['mapping']['quantity'],
                                      expiry_date=data['mapping']['expiry_date'])
        db.session.add(mapping)
        db.session.commit()

    # Step 4: Link Product to Grocery List
    grocery_item = GroceryItem(grocery_name_id=grocery_name_id,
                               item_id=product.id)
    db.session.add(grocery_item)
    db.session.commit()

    return jsonify({"message": "Grocery item added successfully."}), 201
