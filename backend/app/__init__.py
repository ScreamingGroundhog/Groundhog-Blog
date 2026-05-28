from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    from app.routes.auth import auth_bp
    from app.routes.articles import articles_bp
    from app.routes.categories import categories_bp
    from app.routes.tags import tags_bp
    from app.routes.files import files_bp
    from app.routes.public import public_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(articles_bp, url_prefix="/api/articles")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(tags_bp, url_prefix="/api/tags")
    app.register_blueprint(files_bp, url_prefix="/api/files")
    app.register_blueprint(public_bp, url_prefix="/api/public")

    return app
