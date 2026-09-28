#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

class Books(Resource):
    def get(self):
        # Read pagination settings from the URL; fall back to defaults if missing or invalid
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        # Fetch only the requested page of books, in a consistent order.
        # error_out=False returns an empty page (not a 404) when page is out of range.
        pagination = Book.query.order_by(Book.id).paginate(
            page=page, per_page=per_page, error_out=False
        )

        # Serialize just this page's books
        books = [BookSchema().dump(b) for b in pagination.items]

        # Return the page of books along with metadata the frontend needs
        return {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
            "items": books,
        }, 200


api.add_resource(Books, '/books', endpoint='books')

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

if __name__ == '__main__':
    app.run(port=5555, debug=True)