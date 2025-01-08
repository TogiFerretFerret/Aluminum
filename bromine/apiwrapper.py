import requests
import datetime
class BbApiWrapper:
    """
    A wrapper class for interacting with the Bb API.

    Attributes:
        tt (str): The authentication token.
        userdata (dict): The user data retrieved from the API.
        uid (str): The user ID.
        rawresult (dict): The raw data retrieved from the API.
        classes (list): The list of classes.

    Methods:
        get_rawdata():
            Retrieves raw data from the API and returns it.
        
        get_uid():
            Retrieves and returns the user ID from the raw data.
        
        update_tt(tt):
            Updates the authentication token and returns it.
        
        get_classes():
            Retrieves and returns a list of classes, excluding certain categories and fields.
    """
    def __init__(self, tt):
        """
        Initializes the APIWrapper instance with the provided parameters.

        Args:
            tt: The parameter to be assigned to the instance variable `tt`.

        Attributes:
            tt: Stores the provided `tt` parameter.
            userdata: Initialized to None, can be used to store user data.
            uid: Initialized to None, can be used to store user ID.
            rawresult: Stores the result of the `get_rawdata` method.
            classes: Initialized to None, can be used to store class information.
        """
        self.tt = tt
        self.rawresult = self.get_rawdata()
        self.userdata = None
        self.uid = self.get_uid()
        self.classes=None
    def get_rawdata(self):
        """
        Fetches raw data from the specified API endpoint.

        This method sends a GET request to the "https://hunterschools.myschoolapp.com/api/webapp/context" URL
        with the appropriate headers, including a cookie and user-agent. The response is then parsed as JSON
        and stored in the `rawresult` attribute.

        Returns:
            dict: The raw data retrieved from the API response.
        """
        ff=requests.get("https://hunterschools.myschoolapp.com/api/webapp/context", headers={"cookie": f"t={self.tt}", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"})
        ffj=ff.json()
        self.rawresult = ffj
        return self.rawresult
    def get_uid(self):
        """
        Extracts and returns the user ID from the raw result.

        Returns:
            str: The user ID extracted from the 'UserInfo' section of the raw result.
        """
        self.userdata = self.rawresult['UserInfo']
        return self.userdata['UserId']
    def update_tt(self, tt):
        """
        Updates the tt attribute with the provided value.

        Args:
            tt: The new value to set for the tt attribute.

        Returns:
            The updated value of the tt attribute.
        """
        self.tt = tt
        return self.tt # Why not?
    def get_class(self,sid):
        url=f"https://hunterschools.myschoolapp.com/api/datadirect/SectionInfoView/?format=json&sectionId={sid}&associationId=1"
        headers={"cookie": f"t={self.tt}", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
        return requests.get(url,headers=headers).json()
    def get_classes(self):
        """
        Retrieves and processes class groups from the raw result data.

        This method filters out specific categories of groups and removes duplicate
        groups based on their 'LeadSectionId'. It then removes certain keys from each
        group dictionary before returning the processed list of classes.

        Returns:
            list: A list of dictionaries, each representing a class group with specific
                  keys removed.
        """
        cg=self.rawresult['Groups']
        self.classes = []
        for group in cg:
            if group['Category'] not in ["External Program", "Academic Department Groups","","School Wide","Faculty & Staff"]:
                if group['LeadSectionId'] not in [lsid['LeadSectionId'] for lsid in self.classes]:
                    self.classes.append(group)
        topop=['SectionBlock','SchoolYear','CurrentSectionId','Association','OfferingId','PublishGroupToUser','CurrentEnrollment']
        for cl in self.classes:
            for popper in topop:
                if popper in cl:
                    cl.pop(popper)
            axl=self.get_class(cl['SectionId'])
            cl['OfferingId']=axl[0]['OfferingId']
            # Parse the time
            stimestring=axl[0]['StartDate'].split(" ")[0].split("/")
            etimestring=axl[0]['EndDate'].split(" ")[0].split("/")
            if len(axl)==2:
                etimestring=axl[1]['EndDate'].split(" ")[0].split("/")
            # Parse the strings in format month/day/YYYY IGNORE
            stime=datetime.date(int(stimestring[2]),int(stimestring[0]),int(stimestring[1]))
            etime=datetime.date(int(etimestring[2]),int(etimestring[0]),int(etimestring[1]))
            ttime=etime-stime
            passedtime=datetime.date.today()-stime
            # Progress is the percentage of time passed. If 50%, then 50 is returned.
            cl['Progress']=int((passedtime/ttime)*100)
            if (cl['Progress']<0):
                cl['Progress']=0
            cl['Description']=axl[0]['Description']

        return self.classes
    def get_assignments(self, lsid):
        """
        Retrieves and returns a list of assignments for a given lead section ID.

        Args:
            lsid: The lead section ID for which to retrieve assignments.

        Returns:
            list: A list of dictionaries, each representing an assignment.
        """
        url = f"https://hunterschools.myschoolapp.com/api/assignment/forsection/{lsid}/?format=json&dateSort=0&personaId=2"
        headers={"cookie": f"t={self.tt}", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers)
        return response.json()
    def get_headers(self):
        headers={"cookie": f"t={self.tt}", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
        return headers
    def get_assignment(self, aii):
        url=f"https://hunterschools.myschoolapp.com/api/assignment2/UserAssignmentDetailsGetAllStudentData?assignmentIndexId={aii}&studentUserId={self.uid}&personaId=2"
        headers=self.get_headers()
        return requests.get(url,headers=headers).json()