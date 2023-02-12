from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from models import db, User
from config import ApplicationConfig
from flask_session import Session

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return "<h1>Index Page!<h1>"

@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    }) 

@app.route("/signup", methods=["POST"])
def signup_user():
    email = request.json["email"]
    password = request.json["password"]

    user_valid = User.query.filter_by(email=email).first() is not None

    if user_valid:
        return jsonify({"error": "User already exists"}), 409

    hash_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hash_password)
    db.session.add(new_user)
    db.session.commit()


    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })

@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    
    session["user_id"] = user.id

    return jsonify({
        "id": user.id,
        "email": user.email
    })

if __name__ == "__main__":
    app.run(debug=True)