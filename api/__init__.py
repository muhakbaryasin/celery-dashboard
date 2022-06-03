from api.settings import (
    initialize_flask_app,
    initialize_plugins,
    # register_blueprints,
    register_restful_api
)


def create_app():
    app = initialize_flask_app()

    with app.app_context():
        # Initialize Plugins
        initialize_plugins(app)
        # Register blueprints
        # register_blueprints(app)
        register_restful_api(app)

        return app
