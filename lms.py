import bromine.apiwrapper as apiwrapper
import bromine.authwrapper as authwrapper
import bromine.googleauth as googleauth
from flask import Flask, render_template, redirect, send_from_directory, send_file
import io
import time # THIS IS FUCKING JANK. I'M SORRY.
import json
import threading 
import base64
import bromine.CONFIG as CONFIG
name=""
authz = None
GoogleAuthProc=None
GoogleAuthUrl=None
app = Flask(__name__)
def init_api(username):
    authz.get_bearer_token()
    tt = authz.get_tt()
    print(tt)
    return apiwrapper.BbApiWrapper(tt)
def run_server():
    global GoogleAuthProc
    GoogleAuthProc = googleauth.goog_megaauth()
app.jinja_env.filters['b64encode'] = base64.b64encode
@app.route('/seturl/<namez>')
def seturl(namez):
    global GoogleAuthUrl
    GoogleAuthUrl = base64.b64decode(namez).decode("utf-8")
    print("Terminating server...")
    GoogleAuthProc.terminate()
    return redirect("/")
@app.route('/')
def index():
    if authz is not None:
        authz.goog_code(GoogleAuthUrl)
        authz.get_authsvctoken()
    if authz is not None:
        if authz.asvc is not None:
            api = init_api(name)
            classes = api.get_classes()
            return render_template("lms.html", classes=classes)
        else:
            time.sleep(0.01)
            if authz.asvc is not None:
                api = init_api(name)
                classes = api.get_classes()
                return render_template("lms.html", classes=classes)
            else:
                return redirect("/auth")
    else:
        time.sleep(0.01)
        if authz is not None:
            if authz.asvc is not None:
                api = init_api(name)
                classes = api.get_classes()
                return render_template("lms.html", classes=classes)
            else:
                time.sleep(0.01)
                if authz.asvc is not None:
                    api = init_api(name)
                    classes = api.get_classes()
                    return render_template("lms.html", classes=classes)
                else:
                    return redirect("/auth")
        else:
            return redirect("/auth")
@app.route('/grades')
def grades():
    pass
@app.route('/class/<id>')
def classd(id):
    if authz.asvc is not None:
        api = init_api(name)
        classds=api.get_class(id)
        if len(classds)==2:
            for c in classds:
                if c['Current']==1:
                    classds=c
        else:
            classds=classds[0]
        classd={}
        assp={"past":api.get_assignments(id,0),"present":api.get_assignments(id,1),"future":api.get_assignments(id,2)}
        return render_template("class.html", classd=classd, classds=classds, assp=assp)
    else:
        return redirect("/")
@app.route('/assignment/<classid>/<assignmentid>')
def assignment(classid, assignmentid):
    if authz.asvc is not None:
        api = init_api(name)
        classds=api.get_class(classid)
        if len(classds)==2:
            for c in classds:
                if c['Current']==1:
                    classds=c
        else:
            classds=classds[0]
        return render_template("assignment.html", classds=classds, assignment=api.get_assignment(assignmentid))
    else:
        return redirect("/")
@app.route('/auth')
def auth():
    # Create a new thread to run the server
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    return render_template("auth.html")
@app.route('/oauth/<namez>')
def auth_name(namez):
    global authz, name
    name = namez
    authz = authwrapper.BbAuthWrapper(name)
    return redirect(googleauth.goog_murl(name))
@app.route('/static/<path:path>')
def send_report(path):
    # Using request args for path will expose you to directory traversal attacks
    return send_from_directory('static', path)
@app.route('/logout')
def logout():
    global authz
    authz = None
    return redirect("/")
@app.route('/update_assignment_status/<id>/<status>', methods=['POST'])
def update_assignment_status(id, status):
    api = init_api(name)
    return api.update_assstatus(id, status).json()
@app.route('/getfile/<fname>/<path>')
def getfile(fname,path):
    api = init_api(name)
    filecontents = api.get_file(path).content
    # Convert to byte string
    #download file to user
    # Write file to disk
    return send_file(io.BytesIO(filecontents), as_attachment=True, download_name=fname)
if __name__ == '__main__':
    app.run(debug=True,port=7272)
