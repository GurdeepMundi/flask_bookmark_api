from flask import Flask, jsonify, url_for, redirect
from markupsafe import escape
import os
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db, Bookmark
from flask_jwt_extended import JWTManager
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR


def create_app(test_config=None):
    app = Flask(__name__,
                # Tells flask that there might be some configuration outside the file.
                instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
        )

    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    # route for visiting bookmarked url using short url
    @app.get('/<short_url>')
    def redirect_to_rui(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()
        if bookmark:
            bookmark.visits = bookmark.visits+1  # increasing visit count
            db.session.commit()
            return redirect(bookmark.url)

    # Handling client errors
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({
            'error':'Not found'
        }), HTTP_404_NOT_FOUND
    # Handling server errors
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        # It is a good practice to have error logging and reporting like this
        # So that we can send it to the admin of our app
        return jsonify({
            'error':'Something went wrong, we are working on it'
        }), HTTP_500_INTERNAL_SERVER_ERROR

    return app
