from flask_restful import Resource
from flask import request
import sqlite3
import json
from resources.bookResource import *


# ================================
# BASIC SECURITY (Username + Password)
# ================================
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"


def check_credentials():
    username = request.headers.get("X-USERNAME")
    password = request.headers.get("X-PASSWORD")

    if username != VALID_USERNAME or password != VALID_PASSWORD:
        return False
    return True


# ================================
# SQLite Connection
# ================================
def get_db_connection():
    try:
        conn = sqlite3.connect("emp.db")
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        raise Exception(f"Database connection failed: {str(e)}")


# ================================
# Create books table if missing
# ================================
def create_books_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


create_books_table()


# ================================
# GET ALL BOOKS
# ================================
class BooksGETResource(Resource):
    def get(self):
        if not check_credentials():
            return {"error": "Unauthorized"}, 401

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM books")
            rows = cursor.fetchall()
            return [dict(row) for row in rows], 200

        except Exception as e:
            return {"error": str(e)}, 500

        finally:
            conn.close()


# ================================
# GET BOOK BY ID
# ================================
class BookGETResource(Resource):
    def get(self, id):
        if not check_credentials():
            return {"error": "Unauthorized"}, 401

        if id <= 0:
            return {"error": "Invalid ID"}, 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
            row = cursor.fetchone()

            if not row:
                return {"message": "Book not found"}, 404

            return dict(row), 200

        except Exception as e:
            return {"error": str(e)}, 500

        finally:
            conn.close()


# ================================
# ADD NEW BOOK
# ================================
class BookPOSTResource(Resource):
    def post(self):
        if not check_credentials():
            return {"error": "Unauthorized"}, 401

        try:
            data = request.get_json(force=True)
        except:
            return {"error": "Invalid JSON"}, 400

        title = data.get("title")
        if not title or not title.strip():
            return {"message": "Title is required"}, 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO books (title) VALUES (?)", (title,))
            conn.commit()

            return {"id": cursor.lastrowid, "title": title}, 201

        except Exception as e:
            return {"error": str(e)}, 500

        finally:
            conn.close()


# ================================
# UPDATE BOOK
# ================================
class BookPUTResource(Resource):
    def put(self, id):
        if not check_credentials():
            return {"error": "Unauthorized"}, 401

        if id <= 0:
            return {"error": "Invalid ID"}, 400

        try:
            data = request.get_json(force=True)
        except:
            return {"error": "Invalid JSON"}, 400

        title = data.get("title")
        if not title or not title.strip():
            return {"message": "Title is required"}, 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("UPDATE books SET title = ? WHERE id = ?", (title, id))
            conn.commit()

            if cursor.rowcount == 0:
                return {"message": "Book not found"}, 404

            return {"id": id, "title": title}, 200

        except Exception as e:
            return {"error": str(e)}, 500

        finally:
            conn.close()


# ================================
# DELETE BOOK
# ================================
class BookDELETEResource(Resource):
    def delete(self, id):
        if not check_credentials():
            return {"error": "Unauthorized"}, 401

        if id <= 0:
            return {"error": "Invalid ID"}, 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM books WHERE id = ?", (id,))
            conn.commit()

            if cursor.rowcount == 0:
                return {"message": "Book not found"}, 404

            return {"message": "Deleted"}, 204

        except Exception as e:
            return {"error": str(e)}, 500

        finally:
            conn.close()
