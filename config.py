# keep this file and other files used by the create_app function free of inner-project import statements to help
# prevent circular imports.  Setting up cache in a separate cache.py file similar to this config.py file is very helpful.

class Config:
    #data base config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # user configurations
    flask_debug = False
    dash_debug = False
    dash_auto_reload = False

    # flask configurations
    SECRET_KEY = 'askjdfkajsdfksdf'
