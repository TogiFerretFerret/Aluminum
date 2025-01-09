import bromine.googleauth as googleauth
import bromine.apiwrapper as apiwrapper
import bromine.authwrapper as authwrapper
import time
if __name__=="__main__":
    print(googleauth.goog_murl("hudsonreich"))
    das=googleauth.goog_megaauth()
    time.sleep(0.2)
    v=authwrapper.BbAuthWrapper("hudsonreich")
    v.goog_code(das)
    v.get_authsvctoken()
    v.get_bearer_token()
    tt=v.get_tt()
    print(tt)
    api=apiwrapper.BbApiWrapper(tt)
    api.get_rawdata()
    test=api.update_assstatus(35917947,1)
    print(test)
    print(test.json())
    print(api.get_assignment(35917947))
