from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Configuration Azure OpenAI
openai.api_type = "azure"
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
openai.api_base = "https://sakhi-mhud29zh-eastus2.cognitiveservices.azure.com/"
openai.api_version = "2024-12-01-preview"
deployment_name = "chatbot-model-openai"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"error": "Aucun message fourni"}), 400
            
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[{"role": "user", "content": user_input}],
            max_tokens=200
        )
        return jsonify({"response": response["choices"][0]["message"]["content"]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)