from flask import Flask 
from flask import render_template
from flask import json
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
    return render_template('accueil.html')

# Route pour afficher le formulaire de connexion
@app.route('/formulaire', methods=['GET'])
def formulaire():
    return render_template('formulaire.html')  # Affiche le formulaire HTML

# Création d'une route qui vérifie l'utilisateur et retour un Jeton JWT si ok.
# La fonction create_access_token() est utilisée pour générer un jeton JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    if username == "admin" and password == "admin":
        access_token = create_access_token(identity={"username": username, "role": "admin"})
        return jsonify(access_token=access_token)
        
    elif username == "test" and password == "test":
        access_token = create_access_token(identity={"username": username, "role": "user"})
        return jsonify(access_token=access_token)
       
    else:
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 4
    

# Route protégée par un jeton valide
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route("/admin", methods=["GET"])
@jwt_required()
def admin():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify(msg="Accès interdit : rôle admin requis"), 403
    return jsonify(msg="Bienvenue Admin ! Vous avez accès à cette page."), 200


                                                                                                               
if __name__ == "__main__":
  app.run(debug=True)
