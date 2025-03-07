# src/configs/dependency_container.py

from src.models.auth_models.user_model import User
from src.models.grocery_models.grocery_list_name_model import GroceryListName

from src.schemas.auth_schemas.user_schema import UserSchema
from src.schemas.grocery_schemas.grocery_list_name_schema import GroceryListNameSchema

from src.repositories.user_repository import UserRepository
from src.repositories.grocery_list_name_repository import GroceryListNameRepository

from src.services.user_services import UserService
from src.services.grocery_services import GroceryService


class DependencyContainer:
    def __init__(self):
        self.models = {}
        self.schemas = {}
        self.repositories = {}
        self.services = {}

    def create_models(self, db):
        self.models['User'] = User(db)
        self.models['GroceryName'] = GroceryListName(db)

    def create_schemas(self):
        self.schemas['UserSchema'] = UserSchema()
        self.schemas['GroceryNameSchema'] = GroceryListNameSchema()

    def create_repositories(self, db):
        self.repositories['user_repository'] = UserRepository(db)
        self.repositories['grocery_repository'] = GroceryListNameRepository(db)

    def create_services(self):
        self.services['user_service'] = UserService(self.repositories['user_repository'])
        self.services['grocery_service'] = GroceryService(self.repositories['grocery_repository'])

    def initialize(self, db):
        self.create_models(db)
        self.create_schemas()
        self.create_repositories(db)
        self.create_services()

    def get_model(self, model_name):
        return self.models[model_name]

    def get_schema(self, schema_name):
        return self.schemas[schema_name]

    def get_repository(self, repository_name):
        return self.repositories.get(repository_name)

    def get_service(self, service_name):
        return self.services.get(service_name)


# Create a global container instance
container = DependencyContainer()
