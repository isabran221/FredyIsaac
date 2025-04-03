from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Gemini API key
genai.configure(api_key="AIzaSyARg5I6lZMgsPdw6gkVb4K4lJsxOGNEa6M")

# Model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Context for the chatbot
base_context = (
    "You are FredyIsaac Assistant, a helpful chatbot that ONLY answers questions related to the FredyIsaac smart hiring platform. "
    "FredyIsaac helps match candidates and companies using AI based on skills and experience. "
    "If the user asks anything unrelated to FredyIsaac or too generic, politely tell them to ask something specific about the platform. "
    "Always respond in the same language the user uses."
)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "").strip()

        if not user_input:
            return jsonify({"response": "Please enter a question."}), 400

        prompt = f"{base_context}\nUser: {user_input}\nFredyIsaac:"
        response = model.generate_content(prompt)
        reply = response.text.strip()
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"response": f"Error generating response: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5005, debug=True)
