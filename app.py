from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Directory for uploaded files
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(200))
    first_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    profile_image = db.Column(db.String(200))
    job_title = db.Column(db.String(100))
    summary = db.Column(db.Text)
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))

# Create the database and tables
with app.app_context():
    db.create_all()

USER_DATA_FOLDER = 'user_data'  # Make sure this directory exists

def get_user_data_directory(username):
    return os.path.join(USER_DATA_FOLDER, username)

def initialize_user_data(username):
    user_data_path = get_user_data_directory(username)
    os.makedirs(user_data_path, exist_ok=True)

    # Create default data files if they do not exist
    default_profile_data = {
        'full_name': '',
        'first_name': '',
        'email': '',
        'phone_number': '',
        'job_title': '',
        'summary': '',
        'linkedin': '',
        'github': '',
        'profile_image': ''
    }
    with open(os.path.join(user_data_path, 'profile.json'), 'w') as f:
        json.dump(default_profile_data, f)

    with open(os.path.join(user_data_path, 'skills.json'), 'w') as f:
        json.dump([], f)

    with open(os.path.join(user_data_path, 'projects.json'), 'w') as f:
        json.dump([], f)

def load_user_data(username):
    user_data_path = get_user_data_directory(username)
    
    # Ensure user data directory exists
    if not os.path.exists(user_data_path):
        initialize_user_data(username)  # Initialize if not present

    # Load user profile data
    with open(os.path.join(user_data_path, 'profile.json')) as f:
        profile_data = json.load(f)

    # Load skills data
    try:
        with open(os.path.join(user_data_path, 'skills.json')) as f:
            skills_data = json.load(f)
    except FileNotFoundError:
        skills_data = []

    # Load projects data
    try:
        with open(os.path.join(user_data_path, 'projects.json')) as f:
            projects_data = json.load(f)
    except FileNotFoundError:
        projects_data = []

    return profile_data, skills_data, projects_data

def save_user_data(username, profile_data, skills_data, projects_data):
    user_data_path = get_user_data_directory(username)
    os.makedirs(user_data_path, exist_ok=True)

    with open(os.path.join(user_data_path, 'profile.json'), 'w') as f:
        json.dump(profile_data, f)

    with open(os.path.join(user_data_path, 'skills.json'), 'w') as f:
        json.dump(skills_data, f)

    with open(os.path.join(user_data_path, 'projects.json'), 'w') as f:
        json.dump(projects_data, f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        
        if User.query.filter_by(username=username).first():
            return "User already exists!"  # Handle user already exists scenario

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        initialize_user_data(username)  # Initialize user data files
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()  # Hash password
        
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                session['username'] = username  # Store username in session
                return redirect(url_for('home'))  # Redirect to home page after login
            else:
                return render_template('login.html', error_message="Invalid password!")  # Password incorrect
        else:
            return render_template('login.html', error_message="Username not found! Please register.")  # Username not found

    return render_template('login.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session.get('username')
    current_user = User.query.filter_by(username=username).first()

    if not current_user:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

    if request.method == 'POST':
        # Load existing data
        profile_data, existing_skills_data, existing_projects_data = load_user_data(username)

        # Get updated information from the form
        profile_data.update({
            'full_name': request.form.get('full_name', ''),
            'first_name': request.form.get('first_name', ''),
            'email': request.form.get('email', ''),
            'phone_number': request.form.get('phone_number', ''),
            'job_title': request.form.get('job_title', ''),
            'summary': request.form.get('summary', ''),
            'linkedin': request.form.get('linkedin', ''),
            'github': request.form.get('github', ''),
        })

        # Handle file upload for the profile image
        if 'profile_image' in request.files:
            profile_image = request.files['profile_image']
            if profile_image and profile_image.filename:
                filename = secure_filename(profile_image.filename)
                profile_image_path = os.path.join(app.root_path, 'static/uploads', filename)
                profile_image.save(profile_image_path)
                profile_data['profile_image'] = f'uploads/{filename}'  # Save the relative path to the image
            else:
                profile_data['profile_image'] = current_user.profile_image  # Keep the existing image if not changed
        else:
            profile_data['profile_image'] = current_user.profile_image  # Keep the existing image if not provided

        # Handle skills input
        skills = request.form.getlist('skills[]')
        proficiency = request.form.getlist('proficiency[]')

        # Combine existing skills with new ones
        new_skills_data = [{'name': skill.strip(), 'proficiency': int(proficiency[i])} 
                           for i, skill in enumerate(skills) if skill.strip()]
        combined_skills_data = existing_skills_data + new_skills_data  # Append new skills

        # Handle project input
        project_names = request.form.getlist('project_names[]')
        project_descriptions = request.form.getlist('project_descriptions[]')
        project_images = request.files.getlist('project_images[]')

        combined_projects_data = []  # Start with an empty list

        # Combine existing projects with new ones
        for i in range(len(project_names)):
            if project_names[i].strip():  # Only add projects with a name
                project_data = {
                    'name': project_names[i],
                    'description': project_descriptions[i],
                }
                if project_images[i] and project_images[i].filename:
                    filename = secure_filename(project_images[i].filename)
                    project_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    project_images[i].save(project_image_path)
                    project_data['image'] = f'uploads/{filename}'
                combined_projects_data.append(project_data)

        combined_projects_data += existing_projects_data  # Append existing projects

        # Save user data to files
        save_user_data(username, profile_data, combined_skills_data, combined_projects_data)
        return redirect(url_for('profile'))

    # Get user data to render the profile
    profile_data, skills_data, projects_data = load_user_data(username)
    user_data = {
        'full_name': profile_data.get('full_name', ''),
        'first_name': profile_data.get('first_name', ''),
        'email': profile_data.get('email', ''),
        'phone_number': profile_data.get('phone_number', ''),
        'job_title': profile_data.get('job_title', ''),
        'summary': profile_data.get('summary', ''),
        'linkedin': profile_data.get('linkedin', ''),
        'github': profile_data.get('github', ''),
        'profile_image': profile_data.get('profile_image', ''),
        'skills': skills_data,
        'projects': projects_data
    }

    return render_template('profile.html', user_data=user_data)


@app.route('/portfolio/<int:portfolio_id>')
def portfolio(portfolio_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    profile_data, skills_data, projects_data = load_user_data(username)
    
    user_data = {
        'full_name': profile_data.get('full_name', ''),
        'first_name': profile_data.get('first_name', ''),
        'email': profile_data.get('email', ''),
        'phone_number': profile_data.get('phone_number', ''),
        'job_title': profile_data.get('job_title', ''),
        'summary': profile_data.get('summary', ''),
        'linkedin': profile_data.get('linkedin', ''),
        'github': profile_data.get('github', ''),
        'profile_image': profile_data.get('profile_image', ''),
        'skills': skills_data,
        'projects': projects_data,
        'css_file': f'/static/css/portfolio_{portfolio_id}_style.css',
        'js_file': f'/static/js/portfolio_{portfolio_id}_script.js'
    }

    template_path = f'portfolios/portfolio_{portfolio_id}/index.html'
    
    try:
        return render_template(template_path, user_data=user_data)
    except Exception as e:
        app.logger.error(f"Error rendering portfolio: {e}")
        return "Portfolio not found", 404

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
