## Backend (Flask) ##
The backend of the Kids' Visual Communication App is built using Flask, a Python web framework. Here's a quick overview of how it works:

# Mode Management:
The app has two modes: Child Mode and Parent Mode. The mode is toggled using the /toggle_mode route. The backend stores the current mode and returns it to the frontend when requested.

# Tasks:
The app tracks three types of tasks: Food, Emotion, and Activity. Each task has a status (e.g., completed or not).
Parent Mode allows parents to update the status of these tasks using the /update_task route.
The backend stores the current status of these tasks in a dictionary (tasks), and this status is sent to the frontend when needed.

# File Uploads:
The backend handles file uploads through the /static/uploads route. Parents can upload images, audio, or video files related to tasks like Daily Living, Nutrition, Emotions, and Activities.
Files are stored in designated directories (static/uploads/<category>).

# Routes:
/: Serves the homepage with information about the current mode and task status.
/toggle_mode: Switches between Parent Mode and Child Mode.
/tasks: Returns the current status of the tasks.
/update_task: Updates the task status (e.g., marking a task as complete).
/static/uploads: Handles file uploads for each category.

## Frontend (HTML + JavaScript) ##
The frontend is built using HTML for structure, CSS for styling, and JavaScript for interactivity.

# Mode Display:
The frontend displays the current mode (either Child Mode or Parent Mode) and changes the background accordingly.
It includes a mode toggle button, which, when clicked, sends a request to the /toggle_mode route to switch modes.

# Task Management:
In Child Mode, buttons are displayed to allow the child to select different tasks (e.g., Daily Living, Nutrition, Emotions, Recreational Activities).

In Parent Mode, parents can upload files (images, audio, video) for different categories and update the status of tasks (e.g., marking them as done).

# Interactivity (JavaScript):

# Mode Switching: 
The toggleMode() function sends a POST request to /toggle_mode to switch between modes.
# Task Updates: 
The updateTask() function sends a POST request to /update_task to update the status of tasks (e.g., marking tasks as completed or checked).
# File Upload: 
The upload form allows parents to submit files, which are sent to the backend and saved in the correct folder.

# Summary:
Backend (Flask): Manages modes, tracks task statuses, handles file uploads, and provides data to the frontend via routes.
Frontend (HTML + JS): Displays tasks and modes, allows interaction (like toggling modes and updating tasks), and communicates with the backend using AJAX requests.