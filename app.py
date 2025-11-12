from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, render_template
import openai

# Load .env file
load_dotenv()

# Configure Azure OpenAI
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")



app = Flask(__name__)

@app.route("/")
def index():
    """Serve the chat interface"""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        
        if not user_input:
            return jsonify({"error": "Message vide"}), 400
        
        # Appel à Azure OpenAI
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[{"role": "user", "content": user_input}],
            max_tokens=200
        )
        
        bot_response = response["choices"][0]["message"]["content"]
        return jsonify({"response": bot_response})
        
    except openai.error.InvalidRequestError as e:
        return jsonify({"error": f"Erreur de requête: {str(e)}"}), 400
    except openai.error.AuthenticationError as e:
        return jsonify({"error": "Erreur d'authentification Azure"}), 401
    except openai.error.APIError as e:
        return jsonify({"error": f"Erreur API Azure: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Erreur interne: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)