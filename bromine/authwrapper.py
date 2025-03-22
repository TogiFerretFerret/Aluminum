import requests

class BbAuthWrapper:
    """
    A class to handle authentication with Blackbaud services.

    Attributes:
        name (str): The username for authentication.
        tt (str): The tt token.
        asvc (str): The authentication service token.
        bearer (str): The bearer token.

    Methods:
        __init__(name):
            Initializes the BbAuthWrapper with the given username.
        
        goog_oauthurl():
            Generates the Google OAuth URL for authentication.
        
        goog_code(oauth_url_final):
            Extracts the Google OAuth code from the final OAuth URL.
        
        get_authsvctoken():
            Retrieves the authentication service token.
        
        get_bearer_token():
            Retrieves the bearer token.
        
        get_tt():
            Retrieves the tt token.
    """
    def __init__(self, name):
        """
        Initializes the wrapper instance with the provided name and sets up the initial state.

        Args:
            name (str): The name to be used for login hint and other purposes.

        Attributes:
            name (str): The name provided during initialization.
            tt (str): Placeholder attribute, initially set to None.
            asvc (str): Placeholder attribute, initially set to None.
            bearer (str): Placeholder attribute, initially set to None.
        """
        self.name = name
        self.tt = None
        self.asvc = None
        self.asis = None
        self._gcode = None
        self.bearer = None
        url = f"https://sts.sky.blackbaud.com/azureadb2c/state?login_hint={name}%40hunterschools.org&redirectUrl=https%3A%2F%2Fhunterschools.myschoolapp.com%2Fapp%3FsvcId%3Dedu%26envId%3Dp-9A4jO0o5LESTJyyg7MVsCA%26bb_id%3D1%23login&bbcid=spa-signin"
        resp = requests.post(url, headers={"content-type": "application/json", "origin": "https://app.blackbaud.com", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}, data='{"redirect_url":"https://hunterschools.myschoolapp.com/app?svcId=edu&envId=p-9A4jO0o5LESTJyyg7MVsCA&bb_id=1#login","embedded":false,"custom_branding_present":true}')
        self.state=resp.json()['state']
        self.asis = resp.headers['set-cookie'].split(";")[0]
    def goog_oauthurl(self):
        """
        Generates the Google OAuth URL for authentication.

        This method constructs the OAuth URL required for Google authentication. Ensure user is NOT logged into blackbaud on browser being used.

        Returns:
            str: The constructed OAuth URL.
        """
        unfurl=f"https://id.blackbaud.com/bbid.onmicrosoft.com/B2C_1A_OIDC/oauth2/v2.0/authorize?response_type=code&response_mode=query&scope=openid&client_id=886aaf26-fc86-43b6-a838-fdc1eef0c3f9&redirect_uri=https%3a%2f%2fsts.sky.blackbaud.com%2fazureadb2c%2fcallback%2fbbid%2fB2C_1A_OIDC&state={self.state}&login_hint={self.name}%40Hunterschools.org&domain_hint=hunterschools-org"
        return unfurl
    def goog_code(self, oauth_url_final):
        """
        Extracts the authorization code from the given OAuth URL.

        Args:
            oauth_url_final (str): The final OAuth URL containing the authorization code. Must be post-login.

        Returns:
            str: The extracted authorization code.
        """
        self._gcode = oauth_url_final.split("code=")[1]
        return self._gcode
    def get_authsvctoken(self):
        """
        Retrieves the authentication service token by making a GET request to the specified URL.

        The method sends a GET request to the Azure AD B2C callback endpoint with the provided state and code.
        It includes specific headers for cookies and user-agent. The response is expected to contain a 
        "Set-Cookie" header from which the authentication service token is extracted.

        Returns:
            str: The authentication service token extracted from the response headers.
        """
        r=requests.get(f"https://sts.sky.blackbaud.com/azureadb2c/callback/bbid/B2C_1A_OIDC?state={self.state}&code={self._gcode}", headers={"cookie": self.asis, "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"},allow_redirects=False)
        self.asvc=r.headers["Set-Cookie"].split(";")[9].split(", ")[1]
        return self.asvc
    def get_bearer_token(self):
        """
        Retrieves a bearer token from the OAuth2 token endpoint.

        This method sends a POST request to the specified OAuth2 token endpoint
        with the necessary headers and data to obtain a bearer token. The token
        is then stored in the instance variable `self.bearer` and returned.

        Returns:
            str: The bearer token retrieved from the OAuth2 token endpoint.
        """
        resp = requests.post("https://sts-sso.myschoolapp.com/oauth2/token", headers={"cookie": self.asvc, "x-csrf": "token_needed","Content-Type": "application/json"}, data='{"environment_id":"p-9A4jO0o5LESTJyyg7MVsCA","permission_scope":"bem-legacy"}')
        self.bearer = resp.json()['access_token']
        return self.bearer
    def get_tt(self):
        """
        Retrieves the 'tt' value from the cookies of a GET request to a specified URL.

        Makes a GET request to the provided URL with authorization and user-agent headers.
        Extracts the 'tt' value from the 'Set-Cookie' header in the response.

        Returns:
            str: The 'tt' value extracted from the cookies.
        """
        url = "https://hunterschools.myschoolapp.com/api/bbid/login?loginTypeId=1"
        resp = requests.get(url, headers={"authorization": f"Bearer {self.bearer}", "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"})
        cookies = resp.headers['Set-Cookie']
        tt = cookies.split(";")[6]
        self.tt=tt.split("=")[1]
        return self.tt
