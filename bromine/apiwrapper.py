import requests

class BbApiWrapper:
    def __init__(self, tt):
        self.tt = tt
        self.userdata = None
        self.uid = self.get_uid()
        self.rawresult = None
    def get_uid(self):
        ff=requests.get("https://hunterschools.myschoolapp.com/api/webapp/context", headers={"cookie": f"t={self.tt}", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"})
        ffj=ff.json()
        self.userdata = ffj['UserInfo']
        self.rawresult = ffj
        return self.userdata['UserId']
    def update_tt(self, tt):
        self.tt = tt
        return self.tt # Why not
    
