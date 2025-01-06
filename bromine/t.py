import googleauth
import apiwrapper
import authwrapper
print(googleauth.goog_murl("hudsonreich"))
das=googleauth.goog_megaauth()
v=authwrapper.BbAuthWrapper("hudsonreich")
v.goog_code(das)
v.get_authsvctoken()
v.get_bearer_token()
tt=v.get_tt()
#print(tt)
api=apiwrapper.BbApiWrapper(tt)
api.get_rawdata()
#print(api.rawresult)
print(api.get_classes())