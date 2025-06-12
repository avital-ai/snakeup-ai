from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ===== Supabase connection =====
SUPABASE_URL = "https://njwzxkazbreyckqfchab.supabase.co" 
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5qd3p4a2F6YnJleWNrcWZjaGFiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk2NDg2MDksImV4cCI6MjA2NTIyNDYwOX0.s6EH1BrB0FIT6jNeg0-AY57B2z-derYEHsnXchwp74k"

SUPABASE_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# ===== Routes =====

@app.route("/")
def home():
    return "AI Server is running!"

@app.route("/getnewgame", methods=["POST"])
def get_new_game():
    try:
        # נשלוף משחק חדש מהטבלה
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/music_games?select=*&limit=1",
            headers=SUPABASE_HEADERS
        )

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch game", "details": response.text}), 500

        data = response.json()
        if not data:
            return jsonify({"error": "No games found"}), 404

        return jsonify(data[0])  # מחזיר משחק אחד
