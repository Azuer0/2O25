from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import time

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return username

@app.route('/')
def home():
    return "<h1>Welcome!</h1>"

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Username and password required"}), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already exists"}), 400

        user = User(username=data['username'], password=data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({"id": user.id}), 201
    return '''
    <h1>Регистрация</h1>
    <p>Отправь код в консоль браузера(открывается на f12)</p>
    <pre>
fetch('/register', {
method: 'POST',
headers: {
'Content-Type': 'application/json',
},
body: JSON.stringify({
username: 'ваш_логин',
password: 'ваш_пароль'
})
})
.then(response => response.json())
.then(data => console.log(data));
    </pre>
'''


@app.route('/users')
def list_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username} for u in users])

@app.route('/process_json', methods=['POST'])
@auth.login_required
def process_json():
    start_time = time.time()
    if not request.is_json:
        return jsonify({"error": "JSON data required"}), 400

    data = request.get_json()
    processing_time = round((time.time() - start_time) * 1000, 2)

    return jsonify({
        "status": "success",
        "data": data,
        "processing_time_ms": processing_time,
        "user": auth.current_user()
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
