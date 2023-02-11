from flask import Flask
from models import db, User

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Index Page!<h1>"

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/users')
def user():
    return 'user'

if __name__ == "__main__":
    app.run(debug=True)

db.init_app(app)
db.create_all()