# src/extensions/dependency_extension.py

from flask import Flask, current_app
from typing import Optional


class DependencyExtension:
    _global_container = None  # Renamed global variable

    def __init__(self, app: Optional[Flask] = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self._register_container_property(app)
        # Initialize the DI container with app context
        db = current_app.extensions['sqlalchemy'].db
        self._global_container.initialize(db)

    @staticmethod
    def _register_container_property(app: Flask):
        app.extensions['di_container'] = DependencyExtension._global_container

    @staticmethod
    def set_container(container: Optional[object]):
        DependencyExtension._global_container = container

    @staticmethod
    def get_container() -> Optional[object]:
        return current_app.extensions.get('di_container')
