from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
db= SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Auto increment
    username = db.Column(db.String(8), unique=True, nullable=False) # Auto increment
    email = db.Column(db.String(120), unique=True, nullable=False) # Auto increment
    password = db.Column(db.Text(), nullable=False) # Auto increment
    create_at = db.Column(db.DateTime, default=datetime.now()) # Auto increment
    updated_at = db.Column(db.DateTime, onupdate=datetime.now()) # Auto increment
    # backref to specify reverse relationship
    bookmarks = db.relationship('Bookmark', backref="user") 


    # String representation of the class
    def __repr__(self)->str:
        return f'User>>>{self.username}'
    
class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Auto increment
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=True)
    visits = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_at = db.Column(db.DateTime, default=datetime.now()) # Auto increment
    updated_at = db.Column(db.DateTime, onupdate=datetime.now()) # Auto increment

    def generate_short_characters(self):
        characters=string.digits+string.ascii_letters
        picked_chars=''.join(random.choices(characters, k=3))
        link=self.query.filter_by(short_url=picked_chars).first()

        if link:
            self.generate_short_characters()
        else:
            return picked_chars

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url=self.generate_short_characters()

    def __repr__(self)->str:
        return 'Bookmark>>> {self.url}'