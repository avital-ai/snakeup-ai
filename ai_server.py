from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
SUPABASE_TABLE = "games"

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

@app.route('/')
def index():
    return 'Hello from SnakeUp AI Server!'

# 1. GETNEWGAME - יוצרת משחק חדש ומחזירה ID
@app.route('/getnewgame', methods=['POST'])
def get_new_game():
    game_data = {
        "name": "New Game",
        "score": 0
    }
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
        headers=headers,
        json=game_data
    )
    if response.status_code == 201:
        return jsonify({"id": response.json()[0]["id"]})
    else:
        return jsonify({"error": response.text}), 400

# 2. SAVENEWGAME - שומר משחק לפי ID
@app.route('/savenewgame', methods=['POST'])
def save_new_game():
    data = request.get_json()
    game_id = data.get("id")
    name = data.get("name")
    score = data.get("score")

    if not game_id:
        return jsonify({"error": "Missing game ID"}), 400

    response = requests.patch(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?id=eq.{game_id}",
        headers=headers,
        json={"name": name, "score": score}
    )
    if response.status_code in [200, 204]:
        return jsonify({"status": "updated"})
    else:
        return jsonify({"error": response.text}), 400

# 3. GETGAME - מחזירה משחק לפי ID
@app.route('/getgame/<game_id>', methods=['GET'])
def get_game(game_id):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?id=eq.{game_id}",
        headers=headers
    )
    if response.status_code == 200 and response.json():
        return jsonify(response.json()[0])
    else:
        return jsonify({"error": "Game not found"}), 404

# פונקציית אנליזה קיימת
def analyze(text):
    if "forest" in text or "green" in text:
        return {"background_color": "green"}
    elif "sky" in text or "blue" in text:
        return {"background_color": "blue"}
    elif "fire" in text or "red" in text:
        return {"background_color": "red"}
    else:
        return {"background_color": "gray"}

@app.route('/analyze', methods=['POST'])
def handle_analyze():
    data = request.get_json()
    text = data.get("text", "")
    result = analyze(text.lower())
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
