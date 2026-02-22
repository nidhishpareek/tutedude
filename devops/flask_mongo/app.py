from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "backend", "data.json")

MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "test")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION", "submissions")


def get_collection():
    if not MONGO_URI:
        raise ValueError("MONGO_URI is not set")
    client = MongoClient(MONGO_URI)
    return client[MONGO_DB_NAME][MONGO_COLLECTION]


@app.route("/api", methods=["GET"])
def api_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/", methods=["GET", "POST"])
def index():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        try:
            if not name or not email:
                raise ValueError("Name and email are required")

            collection = get_collection()
            collection.insert_one({"name": name, "email": email})
            return redirect(url_for("success"))
        except (ValueError, PyMongoError) as e:
            error = str(e)

    return render_template("form.html", error=error)


@app.route("/success", methods=["GET"])
def success():
    return render_template("success.html")


@app.route("/submissions", methods=["GET"])
def submissions():
    error = None
    records = []

    try:
        collection = get_collection()
        cursor = collection.find({}, {"_id": 0, "name": 1, "email": 1})
        records = list(cursor)
    except (ValueError, PyMongoError) as e:
        error = str(e)

    return render_template("submissions.html", records=records, error=error)


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = (request.form.get("itemName") or "").strip()
    item_description = (request.form.get("itemDescription") or "").strip()

    if request.is_json:
        payload = request.get_json(silent=True) or {}
        item_name = (payload.get("itemName") or item_name).strip()
        item_description = (payload.get("itemDescription") or item_description).strip()

    if not item_name or not item_description:
        return jsonify({"error": "itemName and itemDescription are required"}), 400

    try:
        collection = get_collection()
        collection.insert_one(
            {"itemName": item_name, "itemDescription": item_description}
        )
        return jsonify({"message": "Todo item submitted successfully"}), 201
    except (ValueError, PyMongoError) as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
