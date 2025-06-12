from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ===== Supabase connection =====
SUPABASE_URL = "https://njwzxkazbreyckqfchab.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5qd3p4a2F6YnJleWNrcWZjaGFiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk2NDg2MDksImV4cCI6MjA2NTIyNDYwOX0.s6EH1BrB0FIT6jNeg0-AY57B2z-derYEHsnXchwp74k"
SUPABASE_TABLE = "music_games"

SUPABASE_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# ===== Routes =====

@app.route("/")
def home():
    return "AI Server is running!"

# 1. יצירת משחק חדש
@app.route("/getnewgame", methods=["POST"])
def get_new_game():
    game_data = {
        "name": "New Game",
        "score": 0
    }
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
        headers=SUPABASE_HEADERS,
        json=game_data
    )
    if response.status_code == 201:
        return jsonify({"id": response.json()[0]["id"]})
    else:
        return jsonify({"error": response.text}), 400

# 2. שמירת משחק לפי ID
@app.route("/savenewgame", methods=["POST"])
def save_new_game():
    data = request.get_json()
    game_id = data.get("id")
    name = data.get("name")
    score = data.get("score")

    if not game_id:
        return jsonify({"error": "Missing game ID"}), 400

    response = requests.patch(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?id=eq.{game_id}",
        headers=SUPABASE_HEADERS,
        json={"name": name, "score": score}
    )
    if response.status_code in [200, 204]:
        return jsonify({"status": "updated"})
    else:
        return jsonify({"error": response.text}), 400

# 3. שליפת משחק לפי ID
@app.route("/getgame/<game_id>", methods=["GET"])
def get_game(game_id):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?id=eq.{game_id}",
        headers=SUPABASE_HEADERS
    )
    if response.status_code == 200 and response.json():
        return jsonify(response.json()[0])
    else:
        return jsonify({"error": "Game not found"}), 404

# 4. פונקציית ניתוח טקסט
def analyze(text):
    if "forest" in text or "green" in text:
        return {"background_color": "green"}
    elif "sky" in text or "blue" in text:
        return {"background_color": "blue"}
    elif "fire" in text or "red" in text:
        return {"background_color": "red"}
    else:
        return {"background_color": "gray"}

@app.route("/analyze", methods=["POST"])
def handle_analyze():
    data = request.get_json()
    text = data.get("text", "")
    result = analyze(text.lower())
    return jsonify(result)

# ===== Main =====

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
