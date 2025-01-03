import authwrapper
import apiwrapper
import base64
from flask import Flask, request
from waitress import serve
import multiprocessing
import os
import signal
import CONFIG
# test
def finish_auth(oauth_url):
        with open("tmp.txt", "w") as f:
            f.write(oauth_url)
app = Flask(__name__)
@app.route('/seturl')
def seturl():
    oauth_url = base64.b64decode(request.args.get('url')).decode("utf-8")
    shutdown_server()
    finish_auth(oauth_url=oauth_url)
    return "You may now leave this page and return to the client."
def shutdown_server():
    os.kill(os.getpid(), signal.SIGINT)
def run_server():
    serve(app, host='0.0.0.0', port=5000)
def goog_murl(uid):
    wrap = authwrapper.BbAuthWrapper(uid)
    gurl = wrap.goog_oauthurl()
    gurl = f"{CONFIG.proxyurl}/?redirector={CONFIG.self_url}&url={gurl}"
    return gurl
def goog_megaauth():
    with open("tmp.txt", "w") as f:
        f.write("None")
    oauth_url = "None"
    server_process = multiprocessing.Process(target=run_server)
    server_process.start()
    while not oauth_url.startswith("http"):
        with open("tmp.txt", "r") as f:
            oauth_url = f.read()
    import time
    time.sleep(0.1) # Time to return
    server_process.terminate()
    # After the user logs in, you can use the oauth_url variable
    return oauth_url
