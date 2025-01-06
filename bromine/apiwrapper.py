import requests

class BbApiWrapper:
    def __init__(self, tt):
        self.tt = tt
        self.userdata = None
        self.uid = None
        self.rawresult = self.get_rawdata()
        self.classes=None
    def get_rawdata(self):
        ff=requests.get("https://hunterschools.myschoolapp.com/api/webapp/context", headers={"cookie": f"t={self.tt}", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"})
        ffj=ff.json()
        self.rawresult = ffj
        return self.rawresult
    def get_uid(self):
        self.userdata = self.rawresult['UserInfo']
        return self.userdata['UserId']
    def update_tt(self, tt):
        self.tt = tt
        return self.tt # Why not?
    def get_classes(self):
        cg=self.rawresult['Groups']
        self.classes = []
        for group in cg:
            if group['Category'] not in ["External Program", "Academic Department Groups","","School Wide","Faculty & Staff"]:
                if group['LeadSectionId'] not in [lsid['LeadSectionId'] for lsid in self.classes]:
                    self.classes.append(group)
        topop=['SectionBlock','SchoolYear','LeadSectionId','CurrentSectionId','Association','OfferingId','PublishGroupToUser','CurrentEnrollment']
        for cl in self.classes:
            for popper in topop:
                if popper in cl:
                    cl.pop(popper)
        return self.classes
                