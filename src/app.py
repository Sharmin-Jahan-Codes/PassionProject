from flask import Flask, request, render_template
import os
import json

app = Flask(__name__)

# Define directories for storing uploaded files in each category
UPLOAD_FOLDER = 'static/uploads'
CATEGORIES = ['basic_needs', 'emotions', 'activities']

# Create the necessary directories for each category
for category in CATEGORIES:
    os.makedirs(os.path.join(UPLOAD_FOLDER, category), exist_ok=True)

# Allowed file extensions for images, videos, and audio
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'mp4', 'avi'}

# Default state for tasks
tasks = {
    'food': False,
    'rest': False,
    'wash': False
}

# Mode flag to switch between Parent Mode and Child Mode
mode = "child"  # Default mode is child

# Task images (you can replace the image paths with actual image files)
task_images = {
    'food': 'images/food.png',
    'rest': 'images/rest.png',
    'wash': 'images/wash.png'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
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

    # Get the category and check if it's valid
    category = request.form.get('category')
    if category not in CATEGORIES:
        response = {'message': 'Invalid category'}
        return app.response_class(
            response=json.dumps(response),
            status=400,
            mimetype='application/json'
        )

    # Check if the post request has the file part
    if 'file' not in request.files:
        response = {'message': 'No file part'}
        return app.response_class(
            response=json.dumps(response),
            status=400,
            mimetype='application/json'
        )
    
    file = request.files['file']
    
    # If no file is selected
    if file.filename == '':
        response = {'message': 'No selected file'}
        return app.response_class(
            response=json.dumps(response),
            status=400,
            mimetype='application/json'
        )
    
    # If the file is allowed, save it in the corresponding category folder
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
    app.run(debug=True)


