import base64
import json
import requests


class HTAuthorizationController:
    """The controller used to authorize access to HyperThought through
    the API.
    """

    def __init__(self, access_str):
        """Initialize the HyperThought authorization controller by grabbing and
        initializing all the necessary values from the access string.

        Parameters
        ----------
        access_str
            A string that is encoded in base-64 that has all the information
            needed to authorize calls to HyperThought
        """

        access_obj = json.loads(base64.b64decode(access_str))

        required_fields = ('baseUrl', 'clientId', 'accessToken',
                           'expiresIn', 'expiresAt', 'refreshToken')
        for item in required_fields:
            assert item in access_obj

        self.cookies = {'dodAccessBanner': 'true'}
        self.user_details = None
        self.base_url = access_obj['baseUrl'].rstrip('/')
        self.token_url = f'{self.base_url}/openid/token/'
        self.access_token = access_obj['accessToken']
        self.refresh_token = access_obj['refreshToken']
        self.client_id = access_obj['clientId']

    def get_auth_header(self):
        """Get the authorization header to use with HyperThought API calls.

        Parameters
        ----------
        None

        Returns
        -------
        Dict
            A dict that contains the authorization header.
        """

        auth_header = {'Authorization': f'Bearer {self.access_token}'}
        return auth_header

    def load_user_details(self):
        """Get the user details and set the user_details member variable.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        auth_header = self.get_auth_header()

        url = f'{self.base_url}/api/auth/userinfo/'
        r = requests.get(url, cookies=self.cookies,
                         headers=auth_header, verify=False)

        if r.status_code >= 400:
            raise Exception('Could not load user details!')

        self.user_details = r.json()

    def get_username(self):
        """Get the username of the current HyperThought user.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if not self.user_details:
            self.load_user_details()

        return self.user_details['username']
