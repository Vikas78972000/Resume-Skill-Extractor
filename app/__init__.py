# app/__init__.py

from .routes import api, skills  # Preloading key modules
from .middleware import logging  # Preloading middleware

__all__ = ["api", "skills", "logging"]  # Explicitly define exported modules