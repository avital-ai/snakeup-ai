# analyze.py
import json

def analyze(text):
    if "forest" in text or "green" in text:
        return {"background_color": "green"}
    elif "sky" in text or "blue" in text:
        return {"background_color": "blue"}
    elif "fire" in text or "red" in text:
        return {"background_color": "red"}
    else:
        return {"background_color": "gray"}

def save_result(result):
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(result, f)

if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as f:
        user_input = f.read()
    result = analyze(user_input.lower())
    save_result(result)
