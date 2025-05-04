import os
from flask import Flask, request, jsonify, render_template
from flask import send_from_directory
import httpx
from dotenv import load_dotenv


env_path = os.path.join(os.path.dirname(__file__), ".env")


# Load .env using absolute path
load_dotenv(dotenv_path=env_path)




app = Flask(__name__)

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("API key not found. Please set the GROQ_API_KEY environment variable.")

BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')
@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    data = request.get_json()
    ingredients = data.get('ingredient', '')
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    json_data = {
        "model": "llama3-8b-8192",  # Or choose your model
        "messages": [
            {"role": "system", "content": "You are a helpful recipe assistant."},
            {"role": "user", "content": f"Generate a recipe using these ingredients only: {ingredients}"}
        ]
    }

    response = httpx.post(BASE_URL, headers=headers, json=json_data)

    if response.status_code == 200:
        recipe = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No recipe generated.")
    else:
        recipe = "Failed to generate recipe."

    return jsonify({"recipe": recipe})

if __name__ == '__main__':
    app.run(debug=True)
