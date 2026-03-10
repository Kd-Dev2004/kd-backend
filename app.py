from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# Load API key securely from environment variables
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Root endpoint
@app.route("/")
def home():
    return "KD Backend Running"

# Health check endpoint (used by uptime monitoring)
@app.route("/health")
def health():
    return jsonify({"status": "alive"})

# AI chat endpoint
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "prompt" not in data:
        return jsonify({"error": "Prompt is required"}), 400

    prompt = data["prompt"]

    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = completion.choices[0].message.content

        return jsonify({
            "response": response_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
