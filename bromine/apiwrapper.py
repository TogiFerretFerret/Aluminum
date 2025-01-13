import base64
import requests
import datetime

class BbApiWrapper:
    def __init__(self, tt, session):
        self.session = session
        self.tt = tt
        self.rawresult = self.get_rawdata()
        self.userdata = None
        self.uid = self.get_uid()
        self.classes = None

    def get_rawdata(self):
        ff = self.session.get("https://hunterschools.myschoolapp.com/api/webapp/context", headers={"cookie": f"t={self.tt}", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"})
        ffj = ff.json()
        self.rawresult = ffj
        return self.rawresult

    def get_uid(self):
        self.userdata = self.rawresult['UserInfo']
        return self.userdata['UserId']

    def update_tt(self, tt):
        self.tt = tt
        return self.tt

    def get_class(self, sid):
        url = f"https://hunterschools.myschoolapp.com/api/datadirect/SectionInfoView/?format=json&sectionId={sid}&associationId=1"
        headers = {"cookie": f"t={self.tt}", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
        return self.session.get(url, headers=headers).json()

    def get_classes(self):
        cg = self.rawresult['Groups']
        self.classes = []
        for group in cg:
            if group['Category'] not in ["External Program", "Academic Department Groups", "", "School Wide", "Faculty & Staff"]:
                if group['LeadSectionId'] not in [lsid['LeadSectionId'] for lsid in self.classes]:
                    self.classes.append(group)
        topop = ['SectionBlock', 'SchoolYear', 'CurrentSectionId', 'Association', 'OfferingId', 'PublishGroupToUser', 'CurrentEnrollment']
        for cl in self.classes:
            for popper in topop:
                if popper in cl:
                    cl.pop(popper)
            axl = self.get_class(cl['SectionId'])
            cl['OfferingId'] = axl[0]['OfferingId']
            stimestring = axl[0]['StartDate'].split(" ")[0].split("/")
            etimestring = axl[0]['EndDate'].split(" ")[0].split("/")
            if len(axl) == 2:
                etimestring = axl[1]['EndDate'].split(" ")[0].split("/")
            stime = datetime.date(int(stimestring[2]), int(stimestring[0]), int(stimestring[1]))
            etime = datetime.date(int(etimestring[2]), int(etimestring[0]), int(etimestring[1]))
            ttime = etime - stime
            passedtime = datetime.date.today() - stime
            cl['Progress'] = int((passedtime / ttime) * 100)
            if cl['Progress'] < 0:
                cl['Progress'] = 0
            cl['Description'] = axl[0]['Description']
        return self.classes

    def get_assignments(self, lsid, dsort):
        url = f"https://hunterschools.myschoolapp.com/api/assignment/forsection/{lsid}/?format=json&dateSort={dsort}&personaId=2"
        headers = {"cookie": f"t={self.tt}", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
        response = self.session.get(url, headers=headers)
        return response.json()

    def get_headers(self):
        headers = {"cookie": f"t={self.tt}", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
        return headers

    def get_assignment(self, aii):
        url = f"https://hunterschools.myschoolapp.com/api/assignment2/UserAssignmentDetailsGetAllStudentData?assignmentIndexId={aii}&studentUserId={self.uid}&personaId=2"
        headers = self.get_headers()
        te = self.session.get(url, headers=headers).json()
        print(te)
        if te['PublishGrade'] and te['AssignmentGrade'] and 'GradebookGrade' in te['AssignmentGrade'].keys():
            grade = (te['AssignmentGrade']['GradebookGrade'] / te['MaxPoints']) * 100
            te['OverallGrade'] = grade
            te['IsGraded'] = True
        return te

    def update_assstatus(self, aii, state):
        url = "https://hunterschools.myschoolapp.com/api/assignment2/assignmentstatusupdate"
        headers = self.get_headers()
        headers['content-type'] = "application/json"
        headers['referer'] = "https://hunterschools.myschoolapp.com/lms-assignment/assignment-center/student"
        body = {"assignmentIndexId": aii, "assignmentStatus": state}
        return self.session.post(url, headers=headers, json=body)

    def get_file(self, path):
        path=base64.b64decode(path).decode("utf-8")
        session = requests.Session()
        h = self.get_headers()
        h["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        h['referer'] = "https://hunterschools.myschoolapp.com/lms-assignment/assignment-center/student"
        h['authority'] = "hunterschools.myschoolapp.com"
        session.headers.update(h)
        print(f"https://hunterschools.myschoolapp.com/{path}")
        return session.get(f"https://hunterschools.myschoolapp.com/{path}")
