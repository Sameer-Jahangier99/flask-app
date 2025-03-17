from flask import Flask, render_template, request, jsonify
from flask_cors import CORS 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# Configure PostgreSQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@localhost:5432/tiktok-post'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return {'message': 'Hello, World!'}


if __name__ == '__main__':
    with app.app_context():  # Ensures Flask has an active app context
        db.create_all()
    app.run(debug=True, host='0.0.0.0')