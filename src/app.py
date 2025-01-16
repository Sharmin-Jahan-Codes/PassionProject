import os
from flask import Flask, request, render_template, redirect, url_for, session, flash
import json

app = Flask(__name__)

# Secret key for session management
app.secret_key = os.urandom(24)

# Storing uploaded files in each category
UPLOAD_FOLDER = 'static/uploads'
CATEGORIES = ['daily_living', 'emotions', 'activities', 'nutrition']

# Create the necessary directories for each category
for category in CATEGORIES:
    os.makedirs(os.path.join(UPLOAD_FOLDER, category), exist_ok=True)

# Allowed file extensions for images, videos, and audio
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'mp4', 'avi'}

# Default state for tasks
tasks = {
    'daily_living': False,
    'emotion': False,
    'activity': False,
    'nutrition': False
}

# Switch between Parent Mode and Child Mode
mode = "child"  # Default mode is child

# Task images
task_images = {
    'daily_living': 'images/daily_living.png',
    'emotion': 'images/emotion.png',
    'activity': 'images/activity.png',
    'nutrition': 'images/nutrition.png'
}

# Simulate a simple user database (replace with real database in production)
users = {
    'parent': 'password123',  # Example user
    'child': 'childpassword'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', mode=mode, tasks=tasks, task_images=task_images)

# Toggle between Parent and Child mode
@app.route('/toggle_mode', methods=['POST'])
def toggle_mode():
    global mode
    mode = "parent" if mode == "child" else "child"
    response = {'message': f'Mode switched to {mode}', 'mode': mode}
    return app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))  # Already logged in

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Simple check 
        if username in users and users[username] == password:
            session['username'] = username  # Store the username in session
            return redirect(url_for('home'))
        else:
            flash('Invalid Username or Password !', 'danger')
            return render_template('login.html')

    return render_template('login.html')

# Sign-up route
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if 'username' in session:
        return redirect(url_for('home'))  # Already logged in

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        if username in users:
            flash('Username Already Exists. Please Choose a Different Username.', 'danger')
            return render_template('sign_up.html')
        
        # Store the new user 
        users[username] = password
        flash('Account Created Successfully !', 'success')
        return redirect(url_for('login'))

    return render_template('sign_up.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    flash('Logged Out Successfully !')
    return redirect(url_for('login'))


# Get the current state of tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return app.response_class(
        response=json.dumps(tasks),
        status=200,
        mimetype='application/json'
    )

# Update the state of a task (e.g., food, rest, wash)
@app.route('/update_task', methods=['POST'])
def update_task():
    if mode == "parent":
        data = request.json
        task = data.get('task')
        status = data.get('status')

        if task in tasks:
            tasks[task] = status
            response = {'message': f'{task} updated to {status}', 'tasks': tasks}
            return app.response_class(
                response=json.dumps(response),
                status=200,
                mimetype='application/json'
            )
        else:
            response = {'message': 'Task not found'}
            return app.response_class(
                response=json.dumps(response),
                status=400,
                mimetype='application/json'
            )
    else:
        response = {'message': 'You cannot modify tasks in Child Mode'}
        return app.response_class(
            response=json.dumps(response),
            status=403,
            mimetype='application/json'
        )

# Get all images for a selected category
@app.route('/category_images/<category>', methods=['GET'])
def category_images(category):
    if category not in CATEGORIES:
        return "Invalid category", 400
    
    category_folder = os.path.join(UPLOAD_FOLDER, category)
    
    if not os.path.exists(category_folder):
        return "No files found in this category", 404
    
    files = [f for f in os.listdir(category_folder) if allowed_file(f)]
    if not files:
        return "No files found in this category", 404
    
    file_paths = [os.path.join('uploads', category, file) for file in files]
    
    return render_template('category_images.html', category=category, file_paths=file_paths)

# Route for uploading files in different categories
@app.route('/static/uploads', methods=['POST'])
def upload_file():
    if mode != "parent":
        response = {'message': 'You cannot upload files in Child Mode'}
        return app.response_class(
            response=json.dumps(response),
            status=403,
            mimetype='application/json'
        )

    category = request.form.get('category')
    if category not in CATEGORIES:
        response = {'message': 'Invalid category'}
        return app.response_class(
            response=json.dumps(response),
            status=400,
            mimetype='application/json'
        )

    if 'file' not in request.files:
        response = {'message': 'No file part'}
        return app.response_class(
            response=json.dumps(response),
            status=400,
            mimetype='application/json'
        )
    
    file = request.files['file']
    
    if file.filename == '':
        response = {'message': 'No selected file'}
        return app.response_class(
            response=json.dumps(response),
            status=400,
            mimetype='application/json'
        )
    
    if file and allowed_file(file.filename):
        filename = os.path.join(UPLOAD_FOLDER, category, file.filename)
        file.save(filename)
        response = {'message': f'File successfully uploaded to {category}: {filename}'}
        return app.response_class(
            response=json.dumps(response),
            status=200,
            mimetype='application/json'
        )
    else:
        response = {'message': 'Invalid file format'}
        return app.response_class(
            response=json.dumps(response),
            status=400,
            mimetype='application/json'
        )

if __name__ == '__main__':
    print (os.getcwd())
    app.run(debug=True)
