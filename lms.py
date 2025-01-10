import bromine.apiwrapper as apiwrapper
import bromine.authwrapper as authwrapper
import bromine.googleauth as googleauth
from flask import Flask, render_template, redirect, send_from_directory
import time # THIS IS FUCKING JANK. I'M SORRY.
import json
import threading 
name=""
authz = None
ac=None
app = Flask(__name__)
def init_api(username):
    authz.get_bearer_token()
    tt = authz.get_tt()
    print(tt)
    return apiwrapper.BbApiWrapper(tt)
def run_server():
    global ac
    ac = googleauth.goog_megaauth()
@app.route('/')
def index():
    time.sleep(0.001)
    if authz is not None:
        authz.goog_code(ac)
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
    print(api.get_assignment(id))
    return api.update_assstatus(id, status).json()
@app.route('/getfile/<path:path>')
def getfile(path):
    api = init_api(name)
    return api.get_file(path).content
if __name__ == '__main__':
    app.run(debug=True,port=5050)
