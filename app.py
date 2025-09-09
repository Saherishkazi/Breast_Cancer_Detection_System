from flask import Flask, request, jsonify, render_template, redirect, url_for, session 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app) 

# Configurations for SQLite and Session
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SECURE'] = True

# Initialize DB and session
db = SQLAlchemy(app)
Session(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Route to render login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user'] = user.email
            return redirect(url_for('free_test'))

        else:
            return "Invalid credentials"

    return render_template('login.html')

# Route to render signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return redirect(url_for('home'))
       

        # If email doesn't exist, create a new user
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('signup.html')


# Route to dashboard (after login)
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Welcome {session['user']}!"
    return redirect(url_for('login'))

# Prediction model
# Enable CORS
from flask_cors import CORS  # Import CORS
CORS(app)

# Load the model (ensure the path is correct)
model = joblib.load(r"models/Cancer_prediction.joblib")

@app.route('/')
def home():
    return render_template('index.html')  # This serves index.html from the templates folder


@app.route('/about')
def about():
    return render_template('AboutUs.html')

@app.route('/contact')
def contact():
    return render_template('ContactUsNew.html')

@app.route('/free-test')
def free_test():
    return render_template('new.html')



@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    print(data)

    # Extract features from the request data
    features = [
        float(data['radius_mean']),
        float(data['texture_mean']),
        float(data['perimeter_mean']),
        float(data['area_mean']),
        float(data['smoothness_mean']),
        float(data['compactness_mean']),
        float(data['concavity_mean']),
        float(data['concave_points_mean']),
        float(data['symmetry_mean']),
        float(data['fractal_dimension_mean']),
        float(data['radius_se']),
        float(data['texture_se']),
        float(data['perimeter_se']),
        float(data['area_se']),
        float(data['smoothness_se']),
        float(data['compactness_se']),
        float(data['concavity_se']),
        float(data['concave_points_se']),
        float(data['symmetry_se']),
        float(data['fractal_dimension_se']),
        float(data['radius_worst']),
        float(data['texture_worst']),
        float(data['perimeter_worst']),
        float(data['area_worst']),
        float(data['smoothness_worst']),
        float(data['compactness_worst']),
        float(data['concavity_worst']),
        float(data['concave_points_worst']),
        float(data['symmetry_worst']),
    ]

    # Make a prediction using the loaded model
    prediction = model.predict([features])
    
    # Return the prediction as JSON
    return jsonify({'prediction': prediction.tolist()})

# Main function
if __name__ == '__main__':
    with app.app_context():  # Set up application context
        db.create_all()  # Creates the users.db file and tables
    app.run(debug=True)
