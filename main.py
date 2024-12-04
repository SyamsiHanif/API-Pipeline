from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database URI (using SQLite for demo purposes)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the User model (table schema)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# Route to render the form
@app.route('/')
def form():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>User Form</title>
    </head>
    <body>
        <h2>Enter User Details</h2>
        <form action="/submit-data" method="POST">
            <label for="name">Name:</label><br>
            <input type="text" id="name" name="name"><br><br>
            <label for="email">Email:</label><br>
            <input type="email" id="email" name="email"><br><br>
            <label for="age">Age:</label><br>
            <input type="number" id="age" name="age"><br><br>
            <label for="country">Country:</label><br>
            <input type="text" id="country" name="country"><br><br>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    '''

# Route to handle form submission and save data to the database
@app.route('/submit-data', methods=['POST'])
def submit_data():
    # Get data from the form
    name = request.form.get('name')
    email = request.form.get('email')
    age = request.form.get('age')
    country = request.form.get('country')

    # Create a new User object
    new_user = User(name=name, email=email, age=age, country=country)

    # Add the new user to the session and commit to save to the database
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "message": "Data submitted and saved successfully!",
            "data": {
                "name": name,
                "email": email,
                "age": age,
                "country": country
            }
        })
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": f"Error saving data: {str(e)}"}), 400

@app.route('/get-user/<int:id>', methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "country": user.country
        })
    else:
        return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    # Create the database tables (only once at the beginning)
    with app.app_context():
        db.create_all()

    app.run(debug=True)
