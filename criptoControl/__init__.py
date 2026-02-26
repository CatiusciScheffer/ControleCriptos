from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from pathlib import Path
import os

# ----------------------------------------
# Extensões (criadas sem app)
# ----------------------------------------
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bootstrap = Bootstrap5()

# ----------------------------------------
# Fábrica de aplicação
# ----------------------------------------
def create_app(config_object: str | None = None) -> Flask:
    """
    Fábrica de aplicação Flask.

    :param config_object: caminho para classe de configuração
                          ex: 'criptoControl.config.DevConfig'
    """
    # Carregar variáveis do .env (na raiz do projeto)
    env_path = Path(__file__).resolve().parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)

    app = Flask(__name__)

    # -----------------------
    # Configuração
    # -----------------------
    if config_object:
        # opcional: caso você crie classes de config (DevConfig, ProdConfig, etc.)
        app.config.from_object(config_object)
    else:
        
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'DATABASE_URL',
            'sqlite:///crypto_data.db'
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ECHO'] = True

        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'uma_chave_secreta_padrao')
        app.config['COINMARKETCAP_API_KEY'] = os.getenv('COINMARKETCAP_API_KEY')

    # -----------------------
    # Inicializar extensões
    # -----------------------
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from criptoControl.models import User
        return User.query.get(int(user_id))

    # -----------------------
    # Registrar blueprints
    # -----------------------
    from criptoControl.routes.auth_routes import auth_bp
    from criptoControl.routes.transactions_routes import transaction_bp
    from criptoControl.routes.main_routes import main_bp
    from criptoControl.routes.crud_crypto_wallet import crypto_wallet_bp
    from criptoControl.routes.update_price import update_price_bp
    from criptoControl.routes.views_databases import views_db_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(crypto_wallet_bp)
    app.register_blueprint(update_price_bp)
    app.register_blueprint(views_db_bp)

    # -----------------------
    # Handlers de erro
    # -----------------------
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

    return app
