# Flask-Vue Example

This is a simple example of how to use Vue in a non-SPA context. At the first commit is a simple Flask app serving simple html pages to 2 routes, `/index` and `/about`. The main repository is after integration with Vue, with changes I will explain here.

## Initial State

Initially there is a file structure of roughly:

    .
    ├── app
    │   ├── __init__.py
    │   ├── main
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   └── templates
    │       ├── index.html
    │       └── about.html
    ├── config.py
    ├── README.md
    ├── requirements.txt
    └── run.py
The HTML templates are stored in the `/templates` folder and Flask by default will look there. If we want simple Vue usage then we can always import from a CDN and just create some js files to import.


## npm and Vue CLI 3
Of Course, to have any real Javascript integration we need npm. We will use the recently released version 3 of Vue CLI. After installing this we can `cd app` and then `vue create frontend`. Follow through the defaults or pick your own flavour.

Vue by default is set up for SPAs, though we want to add components to individual, probably already existing pages. We can use the 'pages' config option. As explained in the [Vue CLI docs](https://cli.vuejs.org/config/), we should create a `vue.config.js` file in root (beside package.json) and then we can specify individual pages to spit out at the end of the build process and where to find the template and js file to build them.

First though, create a structure in `src` of something like:

    src
    ├── assets
    │   └── logo.png
    ├── components
    │   ├── about.vue
    │   ├── HelloWorld.vue
    │   └── index.vue
    └── pages
        ├── about
        │   └── main.js
        └── index
            └── main.js
and now that we know what structure we will have, change the still-empty `vue.config.js` file to:

    module.exports = {
      pages: {
        index: {
          // entry for the page
          entry: 'src/pages/index/main.js',
          // the source template
          template: 'public/index.html',
          // output as dist/index.html
          filename: 'index.html'
        },
        about: {
            entry: 'src/pages/about/main.js',
            template: 'public/about.html',
            filename: 'about.html',
            title: 'About Page'
        }
      }
    }
Notice that the templates are expected in `app/frontend/public` so we should now move the templates here from the default Flask `app/templates` folder.

In this example each of these 'index' and 'about' pages just use the stock 'HelloWorld' Component with different messages, though it is obviously easy to expand from there.

## Configuring Flask

There are 2 main tasks to do while configuring Flask now: Dealing with Mustache-clash and telling it where to look for templates and assets.

 1. Both Vue and Jinja2 use the {{ mustache }} notation. In this case we will change jinja2 to use something else, though it is also possible to change Vue's notation, and guides to do this exist.
 2. Currently Flask expects templates from `app/templates` and static files from `app/static`. Since we need our fancy ES6 and .vue files and other goodies to be put together by webpack and babel they will end up in a gruesome minified form in the `app/frontend/dist` folder (unless of course we use more vue-cli config options to change the output directories of either templates or assets - instructions in the aforementioned docs). We will therefore direct Flask to this new location to look for these files.

We end up with a heavily modified `create_app()` method in the main `__init__.py`:

    def create_app(config_class=Config):

        # define a custom class overwriting the jinja2 template options
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
                          # static_url_path defaults to static_folder. we want to keep it clear
                          static_url_path='',
                          template_folder=TEMPLATE_PATH
                          )

        app.config.from_object(config_class)

        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

        return app

## Run

At this point you can hit `npm run lint` and `npm run build` and see a lovely `dist` folder pop out full of a couple of templates and some assets.

If you haven't already:

    python3.6 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    export FLASK_APP=run.py
and:

    flask run
Now heading to `localhost:5000/about` and `localhost:5000/index` should get you some nice looking vue-generated pages!

