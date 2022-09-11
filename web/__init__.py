from web.settings import (
    initialize_flask_app,
    initialize_plugins,
    register_blueprints,
    register_restful_api,
    configure_database,
    db,
    login_manager
)


def create_app(config):
    app = initialize_flask_app()
    app.config.from_object(config)

    with app.app_context():
        # Initialize Plugins
        initialize_plugins(app)
        # Register blueprints
        register_blueprints(app)
        register_restful_api(app)
        configure_database(app)

        return app
