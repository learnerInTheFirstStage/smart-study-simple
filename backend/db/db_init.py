from flask import Flask
from db.database import db


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("Database tables created.")