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
app.config["JWT_SECRET_KEY"] = "kN!4xDf0#Wm93Pz^T8r$Hq@2vLg6YsXeZbA"  # Ma clée privée
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

@app.route('/')
def hello_world():
    return render_template('accueil.html')

# Création d'une route qui vérifie l'utilisateur et retour un Jeton JWT si ok.
# La fonction create_access_token() est utilisée pour générer un jeton JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username == "admin" and password == "admin":
        role = "admin"
    elif username == "test" and password == "test":
        role = "user"
    else:
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

    additional_claims = {"role": role}
    access_token = create_access_token(identity=username, additional_claims=additional_claims)
    return jsonify(access_token=access_token)
    


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
