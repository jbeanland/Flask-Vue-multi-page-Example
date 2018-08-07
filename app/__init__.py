from flask import Flask
import os

from config import Config

app = Flask(__name__)


if __name__ == "__main__":
    app.run(debug=True)


def create_app(config_class=Config):
    # Both Vue and Jinja2 use {{ mustache }} notation so one of them needs overriding
    class CustomFlask(Flask):
        jinja_options = Flask.jinja_options.copy()
        jinja_options.update(dict(
            block_start_string='(%',
            block_end_string='%)',
            variable_start_string='((',
            variable_end_string='))',
            comment_start_string='(#',
            comment_end_string='#)',
        ))

    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_PATH = os.path.join(BASE_PATH, 'frontend/dist')
    STATIC_PATH = os.path.join(BASE_PATH, 'frontend/dist')

    app = CustomFlask(__name__,
                      static_folder=STATIC_PATH,
                      static_url_path='',
                      template_folder=TEMPLATE_PATH
                      )

    app.config.from_object(config_class)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
