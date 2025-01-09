import bromine.authwrapper as authwrapper
import bromine.apiwrapper as apiwrapper
import base64
from flask import Flask, request, redirect
from waitress import serve
import multiprocessing
import os
import signal
import bromine.CONFIG as CONFIG
PORT=5420
def finish_auth(oauth_url):
        """
        Writes the provided OAuth URL to a temporary file.

        Args:
            oauth_url (str): The OAuth URL to be written to the file.

        Writes:
            The OAuth URL to a file named 'tmp.txt' in the current working directory.
        """
        with open("tmp.txt", "w") as f:
            f.write(oauth_url)
app = Flask(__name__)
@app.route('/seturl')
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
    shutdown_server()
    finish_auth(oauth_url=oauth_url)
    return redirect(CONFIG.lms_url)
def shutdown_server():
    """
    Shuts down the server by sending a SIGINT signal to the current process.

    This function retrieves the current process ID using os.getpid() and then
    sends a SIGINT signal to it using os.kill(). This effectively stops the
    server by interrupting its execution.

    Raises:
        OSError: If the signal could not be sent.
    """
    os.kill(os.getpid(), signal.SIGINT)
def run_server():
    """
    Starts the server to serve the application.

    This function initializes and runs the server on host '0.0.0.0' and port 5000,
    making the application accessible on the specified host and port.

    Args:
        None

    Returns:
        None
    """
    serve(app, host='0.0.0.0', port=PORT)
def goog_murl(uid):
    """
    Generates a Google OAuth URL for the given user ID.

    This function creates an instance of BbAuthWrapper with the provided user ID,
    retrieves the Google OAuth URL, and then constructs a new URL that includes
    a proxy and redirector.

    Args:
        uid (str): The user ID for which the Google OAuth URL is generated.

    Returns:
        str: The constructed Google OAuth URL with proxy and redirector.
    """
    wrap = authwrapper.BbAuthWrapper(uid)
    gurl = wrap.goog_oauthurl()
    gurl = f"{CONFIG.proxyurl}/?redirector={CONFIG.self_url}&url={gurl}"
    return gurl
def goog_megaauth():
    """
    Handles the OAuth authentication process for Google.

    This function initiates a local server to handle the OAuth callback,
    writes a temporary file to communicate the OAuth URL, and waits for
    the URL to be updated before terminating the server process.

    Returns:
        str: The OAuth URL after the user logs in.
    """
    with open("tmp.txt", "w") as f:
        f.write("None")
    oauth_url = "None"
    server_process = multiprocessing.Process(target=run_server)
    server_process.start()
    while not oauth_url.startswith("http"):
        with open("tmp.txt", "r") as f:
            oauth_url = f.read()
    import time
    time.sleep(0.2) # Time to return
    server_process.terminate()
    # After the user logs in, you can use the oauth_url variable
    return oauth_url
