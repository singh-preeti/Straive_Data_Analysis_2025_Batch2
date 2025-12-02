from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.bookResource import (
    BooksGETResource,
    BookGETResource,
    BookPOSTResource,
    BookPUTResource,
    BookDELETEResource
)

app = Flask(__name__)
CORS(app)
api = Api(app, prefix="/api")

# Add routes
api.add_resource(BooksGETResource, "/books")
api.add_resource(BookGETResource, "/books/<int:id>")
api.add_resource(BookPOSTResource, "/books")
api.add_resource(BookPUTResource, "/books/<int:id>")
api.add_resource(BookDELETEResource, "/books/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
