from flask import Flask

from config import Config

app = Flask(__name__)


if __name__ == "__main__":
    app.run(debug=True)


def create_app(config_class=Config):
    app = Flask(__name__)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
