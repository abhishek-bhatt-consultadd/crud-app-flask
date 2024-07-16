from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medicines.db'
db = SQLAlchemy(app)

# Define User and Medicine Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)

# Create the database and tables
with app.app_context():
    db.drop_all() # note: remove it to allow memory to stay
    db.create_all()


# API Routes
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data: # if data is null, username or password is not present
        abort(400, description="Username or password missing")
    username = data['username']
    password = data['password']
    role = data['role']
    try:
        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully " + username}), 201
    except IntegrityError:  # check for db constraints
        db.session.rollback()
        abort(400, description="Username already exists")

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        abort(400, description="Missing username or password")
    user = User.query.filter_by(username=data['username'], password=data['password'])
    if user:
        return jsonify({"message": "Signin successful"}), 200
    else:
        abort(401, description="Either username or passsword incorrect")

@app.route('/medicines', methods=['GET'])
def get_medicines():
    medicines = Medicine.query.all()
    return [{
        'id': medicine.id,
        'title': medicine.title,
        'company': medicine.company,
    } for medicine in medicines], 200

@app.route('/medicine', methods=['POST'])
def create_medicine():
    data = request.get_json()
    if not data or 'title' not in data or 'company' not in data:
        abort(400, description="Title or Company not provided")
    title = data['title']
    company = data.get('company')
    try:
        new_medicine = Medicine(title=title, company=company)
        db.session.add(new_medicine)
        db.session.commit()
        return jsonify({"message": "Medicine created successfully " + title}), 201
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Medicine with this name already exists")

@app.route('/medicine/<int:id>', methods=['DELETE'])
def delete_medicine(id):
    medicine = Medicine.query.get(id)
    if medicine :
        db.session.delete(medicine)
        db.session.commit()
        return jsonify({"message": "Medicine deleted successfully"}), 200
    else :
        abort(404, description="Medicine not found")

@app.route('/medicine/<int:id>', methods=['PUT'])
def update_medicine(id):
    data = request.get_json()
    if not data:
        abort(400, description="Invalid input")
    medicine = Medicine.query.get_or_404(id)
    if 'title' in data:
        medicine.title = data['title']
    if 'company' in data:
        medicine.company = data['company']  
    db.session.commit()
    return jsonify({"message": "Medicine updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
