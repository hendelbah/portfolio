from flask import Flask


def create_app(testing=False):
    """Create and configure an instance of the Flask application."""
    # noinspection PyShadowingNames
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="qwerty", TESTING=testing)
    from web_report import routes
    app.register_blueprint(routes.bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
