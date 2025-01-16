import bromine.apiwrapper as apiwrapper
import bromine.authwrapper as authwrapper
import bromine.googleauth as googleauth
from flask import Flask, render_template, redirect, send_from_directory, send_file, abort
import io
import json
import threading 
import base64
import bromine.CONFIG as CONFIG
import os
def add_to_path(bin_path):
    os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]
add_to_path(__file__)
app = Flask(__name__)

# Global variables
username = ""
authWrapper = None
google_auth_process = None
google_auth_url = None

def init_api(username):
    """
    Initialize the API wrapper with the bearer token.

    Args:
        username (str): The username for authentication.

    Returns:
        BbApiWrapper: An instance of the API wrapper.
        int: -1 if initialization fails.
    """
    try:
        authWrapper.get_bearer_token()
        token = authWrapper.get_tt()
        print(token)
        return apiwrapper.BbApiWrapper(token)
    except:
        return -1

def run_google_auth_server():
    """
    Run the Google authentication server.
    """
    global google_auth_process
    google_auth_process = googleauth.goog_megaauth()

app.jinja_env.filters['b64encode'] = base64.b64encode

@app.route('/seturl/<encoded_url>')
def set_google_auth_url(encoded_url):
    """
    Set the Google authentication URL and terminate the server.

    Args:
        encoded_url (str): The base64 encoded URL.

    Returns:
        Response: Redirect to the home page.
    """
    global google_auth_url
    google_auth_url = base64.b64decode(encoded_url).decode("utf-8")
    print("Terminating server...")
    google_auth_process.terminate()
    return redirect("/")

@app.route('/')
def index():
    """
    Render the index page with classes if authenticated, otherwise redirect to auth.

    Returns:
        Response: Rendered template or redirect response.
    """
    if authWrapper is not None:
        try:
            authWrapper.goog_code(google_auth_url)
            authWrapper.get_authsvctoken()
        except:
            return redirect("/auth")
    if authWrapper is not None:
        if authWrapper.asvc is not None:
            api = init_api(username)
            if api == -1:
                return redirect("/auth")
            classes = api.get_classes()
            return render_template("lms.html", classes=classes)
        else:
            return redirect("/auth")
    else:
        return redirect("/auth")

@app.route('/grades')
def grades():
    """
    Handle the grades route (not implemented).

    Returns:
        Response: 501 Not Implemented.
    """
    abort(501)

@app.route('/calendar')
def calendar():
    """
    Handle the calendar route (not implemented).

    Returns:
        Response: 501 Not Implemented.
    """
    abort(501)

@app.route('/class/<class_id>')
def class_details(class_id):
    """
    Render the class details page.

    Args:
        class_id (str): The class ID.

    Returns:
        Response: Rendered template or redirect response.
    """
    if authWrapper.asvc is not None:
        api = init_api(username)
        class_details = api.get_class(class_id)
        if len(class_details) == 2:
            for c in class_details:
                if c['Current'] == 1:
                    class_details = c
        else:
            class_details = class_details[0]
        class_info = {}
        assignments = {
            "past": api.get_assignments(class_id, 0),
            "present": api.get_assignments(class_id, 1),
            "future": api.get_assignments(class_id, 2)
        }
        return render_template("class.html", classd=class_info, classds=class_details, assp=assignments)
    else:
        return redirect("/")

@app.route('/assignment/<class_id>/<assignment_id>')
def assignment_details(class_id, assignment_id):
    """
    Render the assignment details page.

    Args:
        class_id (str): The class ID.
        assignment_id (str): The assignment ID.

    Returns:
        Response: Rendered template or redirect response.
    """
    if authWrapper.asvc is not None:
        api = init_api(username)
        class_details = api.get_class(class_id)
        if len(class_details) == 2:
            for c in class_details:
                if c['Current'] == 1:
                    class_details = c
        else:
            class_details = class_details[0]
        return render_template("assignment.html", classds=class_details, assignment=api.get_assignment(assignment_id))
    else:
        return redirect("/")

@app.route('/auth')
def auth():
    """
    Render the authentication page and start the Google auth server.

    Returns:
        Response: Rendered template.
    """
    server_thread = threading.Thread(target=run_google_auth_server)
    server_thread.start()
    return render_template("auth.html")

@app.route('/oauth/<username>')
def oauth(username):
    """
    Handle OAuth authentication.

    Args:
        username (str): The username for authentication.

    Returns:
        Response: Redirect to Google OAuth URL.
    """
    global authWrapper, uname
    uname = username
    authWrapper = authwrapper.BbAuthWrapper(username)
    return redirect(googleauth.goog_murl(username))

@app.route('/static/<path:path>')
def send_static_file(path):
    """
    Serve static files.

    Args:
        path (str): The file path.

    Returns:
        Response: Static file response.
    """
    return send_from_directory('static', path)

@app.route('/logout')
def logout():
    """
    Handle user logout.

    Returns:
        Response: Redirect to home page.
    """
    global authWrapper
    authWrapper = None
    return redirect("/")

@app.route('/update_assignment_status/<assignment_id>/<status>', methods=['POST'])
def update_assignment_status(assignment_id, status):
    """
    Update the status of an assignment.

    Args:
        assignment_id (str): The assignment ID.
        status (str): The new status.

    Returns:
        Response: JSON response with the update result.
    """
    api = init_api(username)
    return api.update_assstatus(assignment_id, status).json()

@app.route('/getfile/<filename>/<path>')
def get_file(filename, path):
    """
    Serve a file for download.

    Args:
        filename (str): The name of the file.
        path (str): The file path.

    Returns:
        Response: File download response.
    """
    api = init_api(username)
    file_contents = api.get_file(path).content
    return send_file(io.BytesIO(file_contents), as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True, port=7272)
