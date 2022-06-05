"""
This package contains all the frontend stuff.

Packages:

- `routes`: contains modules with frontend blueprints and all view functions.

Modules:

- `forms.py': there is all forms for posting data on web pages. It uses wtforms module.
"""

from clinic_app.views.routes import auth_bp, general_bp, admin_bp, doctor_bp
