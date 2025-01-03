import googleauth
import apiwrapper
import authwrapper
print(googleauth.goog_murl("hudsonreich"))
das=testspy.goog_megaauth()
v=authwrapper.BbAuthWrapper("hudsonreich")
v.goog_code(das)
v.get_authsvctoken()
v.get_bearer_token()
tt=wrap.get_tt()
print(tt)
api=apiwrapper.BbApiWrapper(tt)
api.get_uid()
with open("example.json", "w") as f:
    f.write(str(api.rawresult))