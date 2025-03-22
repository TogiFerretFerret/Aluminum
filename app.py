import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
def add_to_path(bin_path):
    os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]
add_to_path(__file__)
from flask import Flask, render_template, redirect, send_from_directory, send_file, abort, request, make_response
import io
import json
import threading 
import base64
from bromine.CONFIG import app as app
import bromine.CONFIG as CONFIG
import os
app = Flask(__name__)
import bromine.apiwrapper as apiwrapper
import bromine.authwrapper as authwrapper
import base64
import os
import signal
import multiprocessing
from waitress import serve
from socket import SOL_SOCKET, SO_REUSEADDR
from licensing.models import *
from licensing.methods import Key, Helpers
import pickle
import zlib
class UserObject:
    def __init__(self):
        self.username =  ""
        self.authWrapper = None
        self.google_auth_url = None
        self.google_auth_process = None
        self.license = ""

def toObj(pstring):
    """
    Converts a pickled string back to a UserObject.

    Args:
        pstring (str): The pickled string representation of the UserObject.

    Returns:
        UserObject: The deserialized UserObject.
    """
    b64d= base64.b64decode(pstring.encode('utf-8'))
    zlibbed2 = zlib.decompress(b64d)
    base64bed = base64.b64decode(zlibbed2)
    zlibbed = zlib.decompress(base64bed)
    pickled = pickle.loads(zlibbed)
    return pickled
def toStr(obj):
    """
    Converts a UserObject to a pickled string.

    Args:
        obj (UserObject): The UserObject to serialize.

    Returns:
        str: The pickled string representation of the UserObject.
    """
    pickled= pickle.dumps(obj)
    zlibbed = zlib.compress(pickled)
    base64bed = base64.b64encode(zlibbed)
    zlibbed2 = zlib.compress(base64bed)
    b64d = base64.b64encode(zlibbed2).decode('utf-8')
    return b64d

@app.route('/gauth/seturl')
def seturl():
    """
    Handles the OAuth URL setting process.

    This function decodes a base64-encoded URL passed as a query parameter,
    shuts down the server, and completes the authentication process using
    the decoded URL.

    Returns:
        str: A message indicating that the user can leave the page and return to the client.
    """
    oauth_url = base64.b64decode(request.args.get('url')).decode("utf-8")
    print(oauth_url)
    print("Shutting down server...")
    print("Redirecting to OAuth URL...")
    return redirect(f"{CONFIG.lms_url}/seturl/{base64.b64encode(oauth_url.encode('utf-8')).decode('utf-8')}")

def goog_murl(uid, google_auth_url):
    """
    Generates a Google OAuth URL for the given user ID.

    This function creates an instance of BbAuthWapper with the provided user ID,
    retrieves the Google OAuth URL, and then constructs a new URL that includes
    a proxy and redirector.

    Args:
        uid (str): The user ID for which the Google OAuth URL is generated.

    Returns:
        str: The constructed Google OAuth URL with proxy and redirector.
    """
    print(uid)
    print(google_auth_url)
    wrap = authwrapper.BbAuthWrapper(uid)
    print(wrap.state)
    gauth_url = wrap.goog_oauthurl()
    goauth_url = f"{CONFIG.proxyurl}/?redirector={CONFIG.self_url}&url={gauth_url}"
    return goauth_url


def init_api(username,authWrapper):
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
    cookie = request.cookies.get("user")
    print(cookie)
    if cookie is None:
        print("wtfrick")
        return redirect("/auth")
    uobj = toObj(cookie)
    username = uobj.username
    authWrapper = uobj.authWrapper
    uobj.google_auth_url = base64.b64decode(encoded_url).decode("utf-8")
    uobj.authWrapper.goog_code(uobj.google_auth_url)
    uobj.authWrapper.get_authsvctoken()
    print("ASVC",uobj.authWrapper.asvc)
    resp= make_response(redirect("/"))
    resp.set_cookie("user", toStr(uobj), max_age=60*60*24*7)
    return resp

@app.route('/')
def index():
    """
    Render the index page with classes if authenticated, otherwise redirect to auth.

    Returns:
        Response: Rendered template or redirect response.
    """
    cookie = request.cookies.get("user")
    print(cookie)
    if cookie is None:
        return redirect("/auth")
    uobj = toObj(cookie)
    username = uobj.username
    authWrapper = uobj.authWrapper
    print(authWrapper)
    print(username)
    if authWrapper is not None:
        print(authWrapper.asvc)
        if authWrapper.asvc is not None:
            api = init_api(username, authWrapper)
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
        Response: 501 Not Implemented."""
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
    cookie = request.cookies.get("user")
    if cookie is None:
        return redirect("/auth")
    uobj = toObj(cookie)
    username = uobj.username
    authWrapper = uobj.authWrapper
    if authWrapper.asvc is not None:
        api = init_api(username, authWrapper)
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
    cookie = request.cookies.get("user")
    if cookie is None:
        return redirect("/auth")
    uobj = toObj(cookie)
    username = uobj.username
    authWrapper = uobj.authWrapper
    if authWrapper.asvc is not None:
        api = init_api(username, authWrapper)
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
    resp=make_response(render_template("auth.html"))
    uobj = UserObject()
    resp.set_cookie("user", toStr(uobj), max_age=60*60*24*7)
    return resp
@app.route('/oauth/<uname>')
def oauth(uname):
    """
    Handle OAuth authentication.

    Args:
        username (str): The username for authentication.

    Returns:
        Response: Redirect to Google OAuth URL.
    """
    try:
        vstr=base64.b64decode(uname).decode()
        tstr=vstr.split("**")
        cookie = request.cookies.get("user")
        likey=base64.b64decode(tstr[1]).decode()
        uobj = None
        if cookie is not None:
            uobj = toObj(cookie)
            uobj.username = tstr[0]
            uobj.authWrapper = authwrapper.BbAuthWrapper(uobj.username)
        RSAPubKey="<RSAKeyValue><Modulus>rTtOIv+f0zAPCeL4utA248R+edS2pw3EDt5OqwrwPX2+UjlUN+boozSohLAzGXLNGtR3qFV5otwxAo2TpWfHd5cJ8RESblfMoAnNI8LS6CLmn8iLM1P0gv5rDfOF1ibHg52f5pL4EgBSgcx4acbL1/MR//z5dRAigdC5SB703dpgbJjqU9cQ42/PslnYdAjcERm5zeQl9b5m8paeinkpzC7CBEDuu9Ms2N4eKLTtS6MD7t2y7YU/S9viFVc2wnGdcmEDOEUE7k/kQEuLgCdztFzIXNhIDag/AAIdplJGE0m2oR/1TXb5iu3lsM7UWLrE48JNa7VL8PuIDvbXQd0EVw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
        koth="WyIxMDU0NzY5OTIiLCJVb095MzVqOTM4TzRrUVBnVUdWbFU0eW9yaW9uOTRnQU9jK2U4WHlUIl0="
        result = Key.activate(token=koth,
                   rsa_pub_key=RSAPubKey,
                   product_id=29380,
                   key=likey,
                   machine_code=Helpers.GetMachineCode(v=2))
        print(result[0])
        if result[0]==None:
            return redirect("/")
        else:
            uobj.license = likey
            resp=make_response(redirect(goog_murl(uobj.username, uobj.google_auth_url)))
            resp.set_cookie("user", toStr(uobj), max_age=60*60*24*7)
            return resp
        return redirect("/auth")
    except Exception:
        return redirect("/")
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
    cookie = request.cookies.get("user")
    resp= make_response(redirect(f"{CONFIG.proxyurl}/?redirector={CONFIG.lms_url}&url=https://www.google.com/accounts/Logout"))
    resp.set_cookie("user", "", expires=0)
    return resp

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
    cookie = request.cookies.get("user")
    if cookie is None:
        return redirect("/auth")
    uobj = toObj(cookie)
    username = uobj.username
    api = init_api(username, uobj.authWrapper)
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
    cookie = request.cookies.get("user")
    if cookie is None:
        return redirect("/auth")
    uobj = toObj(cookie)
    username = uobj.username
    api = init_api(username, uobj.authWrapper)
    file_contents = api.get_file(path).content
    return send_file(io.BytesIO(file_contents), as_attachment=True, download_name=filename)
from socket import SOL_SOCKET, SO_REUSEADDR
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
