# api/handler.py
from flask import Flask, request, jsonify
import json
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "https://gamepadvision.netlify.app",
                "https://mildly-generous-tarpon.ngrok-free.app",
            ]
        }
    },
)

CSS_FILE_PATH = "css_storage.json"

def load_css_data():
    if os.path.exists(CSS_FILE_PATH):
        try:
            with open(CSS_FILE_PATH, "r") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error loading JSON: {e}")
            return {}
    return {}

def save_css_data(css_data):
    try:
        with open(CSS_FILE_PATH, "w") as file:
            json.dump(css_data, file, indent=4)
    except IOError as e:
        print(f"Error saving CSS data: {e}")

@app.route("/receive_css", methods=["POST"])
@cross_origin()
def receive_css():
    try:
        data = request.get_json()
        slug = data.get("slug")
        encoded_css = data.get("css")

        if not slug or not encoded_css:
            return jsonify({"error": "Invalid data"}), 400

        css_data = load_css_data()
        css_data[slug] = encoded_css
        save_css_data(css_data)
        return jsonify({"status": "success", "slug": slug})

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

@app.route("/get_css/<slug>", methods=["GET"])
@cross_origin()
def get_css(slug):
    try:
        css_data = load_css_data()
        if slug in css_data:
            return jsonify({"css": css_data[slug]})
        else:
            return jsonify({"error": "CSS not found for the provided slug"}), 404
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": "An error occurred", "details": str(e)}), 500
