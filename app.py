from flask import Flask
from flask_migrate import Migrate
from veri import *
from sqlalchemy import select
from flask import request
from blueprintler import api_bp
from flask_cors import CORS



def create_app():
    app= Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://eticaret_user:123456@localhost/ticaret"
    db.init_app(app)
    migrate= Migrate()
    migrate.init_app(app,db)


    CORS(app)

    @app.route('/')
    def index():
        return {"sunucu":"OK"}
    
    app.register_blueprint(api_bp, url_prefix='/api')

    return app