from flask import Flask, request, jsonify
from sympy import sympify
from flask_cors import CORS

app = Flask(__name__)
# Configuration de CORS
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

@app.route('/', methods=['GET'])
def home():
    return "Bienvenue sur l'API de la calculatrice !"

@app.route('/calculate', methods=["POST", "OPTIONS"])
def calculate():
    # Gérer explicitement les requêtes OPTIONS
    if request.method == "OPTIONS":
        return "", 200
        
    try:
        data = request.get_json()
        expression = data.get("expression", "")
        result = sympify(expression)
        return jsonify({"result": float(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Point d'entrée pour les fonctions serverless sur Vercel
from http import HTTPStatus

# Handler for Vercel serverless functions
def handler(request, context):
    with app.request_context(request):
        return app(request)

# Ce bloc ne sera pas utilisé par Vercel, mais permet de tester localement
if __name__ == '__main__':
    app.run(debug=True)