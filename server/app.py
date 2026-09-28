#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

class Books(Resource):
    def get(self):
        books = [BookSchema().dump(b) for b in Book.query.all()]
        return books, 200


api.add_resource(Books, '/books', endpoint='books')

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

if __name__ == '__main__':
    app.run(port=5555, debug=True)