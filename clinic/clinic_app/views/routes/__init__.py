"""
Package contains all view functions that are split into modules and
associated with corresponding blueprints.
"""
from clinic_app import login_manager
from clinic_app.service import UserService
from clinic_app.views.routes.admin import admin_bp
from clinic_app.views.routes.auth import auth_bp
from clinic_app.views.routes.doctor import doctor_bp
from clinic_app.views.routes.general import general_bp

login_manager.user_loader(UserService.get)

__all__ = ['auth_bp', 'general_bp', 'admin_bp', 'doctor_bp']
