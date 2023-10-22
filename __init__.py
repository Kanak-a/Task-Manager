from flask import Blueprint
# Create a blueprint for the 'auth' package
auth_bp = Blueprint('auth', __name__)

# Import views and routes specific to the 'auth' package
from . import views

# You can also configure and initialize any package-specific functionality here
# For example, you might set up additional authentication or database settings

# This is where you might define package-specific functions or setup code
# related to user authentication, registration, etc.