from flask import Flask
from flasgger import Swagger
import os
from report_app.db import *


def create_app(testing=False, db_path=None):
    """Create and configure an instance of the Flask application."""
    # noinspection PyShadowingNames
    app = Flask(__name__)
    if db_path is None:
        db_path = os.path.join(app.root_path, "report.sqlite")
    app.config.from_mapping(SECRET_KEY="qwerty", TESTING=testing,
                            DATABASE=db_path)
    from report_app import routes, api
    app.register_blueprint(routes.bp)
    app.register_blueprint(api.api_bp, url_prefix='/api/v1')
    Swagger(app, template_file='static/specification.yaml')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
