import base64
import os
import signal
import multiprocessing
from flask import Flask, request, redirect
from waitress import serve
import bromine.authwrapper as authwrapper
import bromine.CONFIG as CONFIG
from socket import SOL_SOCKET, SO_REUSEADDR
from bromine.CONFIG import app as app
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

def shutdown_server():
    """
    Shuts down the server by sending a SIGINT signal to the current process.

    This function retrieves the current process ID using os.getpid() and then
    sends a SIGINT signal to it using os.kill(). This effectively stops the
    server by interrupting its execution.

    Raises:
        OSError: If the signal could not be sent.
    """
    print("Shutting down server...")
    os.kill(os.getpid(), signal.SIGINT) # Can this be done in a more elegant way?

def run_server():
    """
    Starts the server to serve the application.

    This function initializes and runs the server on host '127.0.0.1' and port 7420,
    making the application accessible on the specified host and port.

    Args:
        None

    Returns:
        None
    """
    print("Starting server...")
    app.wsgi_app.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serve(app, host='0.0.0.0', port=PORT)
    print("Server started.")

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
    google_auth_url = wrap.goog_oauthurl()
    google_auth_url = f"{CONFIG.proxyurl}/?redirector={CONFIG.self_url}&url={google_auth_url}"
    return google_auth_url

def goog_megaauth():
    """
    Handles the OAuth authentication process for Google.

    This function initiates a local server to handle the OAuth callback,
    writes a temporary file to communicate the OAuth URL, and waits for
    the URL to be updated before terminating the server process.

    Returns:
        multiprocessing.Process: The server process handling the OAuth callback.
    """
    server_process = multiprocessing.Process(target=run_server)
    server_process.start()
    print("Server process started.")
    return server_process
