from src.config.settings import settings
from src.config.setup import create_app
from src.routes import register_blueprints

app = create_app()
register_blueprints(app)


if __name__ == '__main__':
    app.run(debug=settings.DEBUG)
