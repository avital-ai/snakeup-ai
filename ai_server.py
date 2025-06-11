from flask import Flask, request, jsonify

app = Flask(__name__)

def analyze(text):
    if "forest" in text or "green" in text:
        return {"background_color": "green"}
    elif "sky" in text or "blue" in text:
        return {"background_color": "blue"}
    elif "fire" in text or "red" in text:
        return {"background_color": "red"}
    else:
        return {"background_color": "gray"}
        
@app.route('/')
def index():
    return 'Hello from SnakeUp AI Server!'

@app.route('/analyze', methods=['POST'])
def handle_analyze():
    data = request.get_json()
    text = data.get("text", "")
    result = analyze(text.lower())
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
