import bromine.apiwrapper as apiwrapper
import bromine.authwrapper as authwrapper
import bromine.googleauth as googleauth
from flask import Flask, render_template, redirect, send_from_directory
import time # THIS IS FUCKING JANK. I'M SORRY.
import json
import threading 
name="hudsonreich"
authz = authwrapper.BbAuthWrapper(name)
app = Flask(__name__)
def init_api(username):
    authz.get_bearer_token()
    tt = authz.get_tt()
    print(tt)
    return apiwrapper.BbApiWrapper(tt)
def run_server():
    auth_code = googleauth.goog_megaauth()
    authz.goog_code(auth_code)
    authz.get_authsvctoken()
@app.route('/')
def index():
    if authz.asvc is not None:
        api = init_api(name)
        classes = api.get_classes()
        return render_template("lms.html", classes=classes)
    else:
        time.sleep(0.1)
        if authz.asvc is not None:
            api = init_api(name)
            classes = api.get_classes()
            return render_template("lms.html", classes=classes)
        else:
            return redirect("/auth")
@app.route('/grades')
def grades():
    if authz.asvc is not None:
        api = init_api(name)
        classes = api.get_classes()
        uid = {}
        data={}
        for cl in classes:
            uid[cl['LeadSectionId']] = api.get_assignments(cl["LeadSectionId"])
            assp=uid[cl['LeadSectionId']]
            for assignment in assp:
                data[cl['LeadSectionId']]={}
                data[cl['LeadSectionId']][assignment['AssignmentIndexId']]=api.get_assignment(assignment['AssignmentIndexId'])
        return render_template("grades.html", uid=uid, classes=classes,data=data)
    else:
        return redirect("/")
@app.route('/auth')
def auth():
    # Create a new thread to run the server
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    return redirect(googleauth.goog_murl(name))
@app.route('/static/<path:path>')
def send_report(path):
    # Using request args for path will expose you to directory traversal attacks
    return send_from_directory('static', path)
if __name__ == '__main__':
    app.run(debug=True,port=5050)
