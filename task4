from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import time
import hashlib
import base64

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)  # SHA-256

with app.app_context():
    db.create_all()

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == hash_password(password):
        return username

@app.route('/')
def home():
    return "<h1>Welcome!</h1>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Username and password required"}), 400
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already exists"}), 400
        try:
            raw_password = base64.b64decode(data['password']).decode('utf-8')
        except Exception as e:
            return jsonify({"error": "Invalid base64 encoding"}), 400
        user = User(
            username=data['username'],
            password=hash_password(raw_password)
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"id": user.id}), 201

    return '''
    <h1>Регистрация</h1>
    <p>Отправь код в консоль браузера(открывается на f12)</p>
    <pre>
fetch('/register', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    username: 'ваш_логин',
    password: btoa('ваш_пароль')
  })
})
.then(r => r.json()).then(console.log)
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
