from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

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

@app.route('/')
def home():
    return render_template('index.html', mode=mode, tasks=tasks, task_images=task_images)

# Toggle between Parent and Child mode
@app.route('/toggle_mode', methods=['POST'])
def toggle_mode():
    global mode
    mode = "parent" if mode == "child" else "child"
    return jsonify({'message': f'Mode switched to {mode}', 'mode': mode})

# Get the current state of tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Update the state of a task (e.g., food, rest, wash)
@app.route('/update_task', methods=['POST'])
def update_task():
    if mode == "parent":
        data = request.json
        task = data.get('task')
        status = data.get('status')

        if task in tasks:
            tasks[task] = status
            return jsonify({'message': f'{task} updated to {status}', 'tasks': tasks})
        else:
            return jsonify({'message': 'Task not found'}), 400
    else:
        return jsonify({'message': 'You cannot modify tasks in Child Mode'}), 403

if __name__ == '__main__':
    app.run(debug=True)

