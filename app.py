# Import necessary modules
from flask import Flask, request, jsonify
from pyrizz import pyrizz
import os

app = Flask(__name__)

ALLOWED_CATEGORIES = ["romantic", "clever", "geeky", "dev", "all"]

# Retrieve OpenAI API key from environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError(
        "OpenAI API key is missing. Set the OPENAI_API_KEY environment variable."
    )

openai_client = pyrizz.init_openai(OPENAI_API_KEY)


# Define your API endpoints
@app.route("/api/pickup-line", methods=["GET"])
def get_pickup_line():
    category = request.args.get("category")

    if not category or category not in ALLOWED_CATEGORIES:
        return (
            jsonify(
                {
                    "error": f"Invalid or missing category. Allowed categories: {', '.join(ALLOWED_CATEGORIES)}"
                }
            ),
            400,
        )

    line = pyrizz.get_random_category_line(category)
    return jsonify({"pickup_line": line})


@app.route("/api/random-pickup-line", methods=["GET"])
def get_random_pickup_line():
    line = pyrizz.get_random_line()
    return jsonify({"pickup_line": line})


@app.route("/api/ai-line", methods=["GET"])
def get_ai_line():
    keyword = request.args.get("keyword")

    if not keyword:
        return jsonify({"error": "Missing keyword parameter"}), 400

    ai_line = pyrizz.get_ai_line(keyword, openai_client)
    return jsonify({"ai_pickup_line": ai_line})


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
