from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # Ma clée privée
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

@app.route('/') 
def hello_world():
    return render_template('accueil.html')  # Page d'accueil avec lien vers le formulaire

# Route pour afficher le formulaire de connexion
@app.route('/formulaire', methods=['GET'])
def formulaire():
    return render_template('formulaire.html')  # Affiche le formulaire HTML

# Création d'une route qui vérifie l'utilisateur et retourne un jeton JWT si les informations sont correctes
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    # Vérification des utilisateurs
    if username == "admin" and password == "adminpass":
        access_token = create_access_token(identity={"username": username, "role": "admin"})
        return jsonify(access_token=access_token)
    elif username == "user" and password == "userpass":
        access_token = create_access_token(identity={"username": username, "role": "user"})
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

# Route protégée par un jeton valide
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Route pour les utilisateurs
@app.route("/user", methods=["GET"])
@jwt_required()
def user():
    identity = get_jwt_identity()
    if identity.get("role") != "user":
        return jsonify({"msg": "Accès refusé : vous n'êtes pas un utilisateur"}), 403
    return jsonify({"msg": f"Bienvenue utilisateur {identity['username']} !"}), 200

# Route pour les administrateurs
@app.route("/admin", methods=["GET"])
@jwt_required()
def admin():
    identity = get_jwt_identity()
    if identity.get("role") != "admin":
        return jsonify({"msg": "Accès refusé : vous n'êtes pas administrateur"}), 403
    return jsonify({"msg": f"Bienvenue Admin {identity['username']} !"}), 200

if __name__ == "__main__":
    app.run(debug=True)
