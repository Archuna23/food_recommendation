"""
Food Recommendation System - Flask backend
Content-based filtering using Cosine Similarity (same logic as newfood.py)

Run:
    pip install -r requirements.txt
    python app.py
Open: http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# ---------------------------------------------------------------
# Food dataset
# ---------------------------------------------------------------
data = {
    "Food": [
        "Chicken Biryani",
        "Veg Biryani",
        "Chicken Fried Rice",
        "Veg Fried Rice",
        "Masala Dosa",
        "Paneer Butter Masala",
        "Chicken Pizza",
        "Veg Burger",
        "Chicken Noodles",
        "Veg Sandwich",
    ],
    "Vegetarian": [0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    "Spicy":      [9, 6, 7, 5, 7, 6, 5, 3, 8, 2],
    "Healthy":    [5, 8, 5, 8, 7, 6, 4, 5, 5, 8],
    "Protein":    [9, 6, 8, 5, 5, 8, 8, 6, 8, 5],
    "Fast_Food":  [3, 2, 8, 7, 2, 3, 10, 10, 8, 6],
}

df = pd.DataFrame(data)
FEATURES = ["Vegetarian", "Spicy", "Healthy", "Protein", "Fast_Food"]


def get_recommendations(vegetarian, spicy, healthy, protein, fast_food):
    """Return all foods sorted by similarity with the user profile."""
    user = [[vegetarian, spicy, healthy, protein, fast_food]]

    result = df.copy()
    result["Similarity"] = cosine_similarity(user, result[FEATURES])[0]

    # Filter food based on vegetarian preference
    if vegetarian == 1:
        result = result[result["Vegetarian"] == 1]

    return result.sort_values(by="Similarity", ascending=False)


def parse_int(payload, key, low, high):
    """Read an integer from JSON and make sure it is within [low, high]."""
    value = int(payload.get(key))
    if not low <= value <= high:
        raise ValueError(f"{key} must be between {low} and {high}")
    return value


# ---------------------------------------------------------------
# Routes
# ---------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/recommend", methods=["POST"])
def recommend():
    payload = request.get_json(silent=True) or {}
    try:
        vegetarian = parse_int(payload, "vegetarian", 0, 1)
        spicy = parse_int(payload, "spicy", 1, 10)
        healthy = parse_int(payload, "healthy", 1, 10)
        protein = parse_int(payload, "protein", 1, 10)
        fast_food = parse_int(payload, "fast_food", 1, 10)
    except (TypeError, ValueError) as err:
        return jsonify({"error": f"Invalid input: {err}"}), 400

    result = get_recommendations(vegetarian, spicy, healthy, protein, fast_food)

    foods = [
        {
            "name": row["Food"],
            "vegetarian": int(row["Vegetarian"]),
            "spicy": int(row["Spicy"]),
            "healthy": int(row["Healthy"]),
            "protein": int(row["Protein"]),
            "fast_food": int(row["Fast_Food"]),
            "similarity": round(float(row["Similarity"]) * 100, 2),
        }
        for _, row in result.iterrows()
    ]

    return jsonify(
        {
            "user_profile": [vegetarian, spicy, healthy, protein, fast_food],
            "top3": foods[:3],
            "all": foods,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
