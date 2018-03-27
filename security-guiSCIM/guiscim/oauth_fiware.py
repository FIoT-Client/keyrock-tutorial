import base64
import requests.auth
import requests

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

try:
    import simplejson as json
except ImportError:
    import json


class OAuth2(object):
    def __init__(self):

        self.client_id = '2654e443273140968d0f3465e65a3737'  # IDM APP CLIENT ID
        self.client_secret = '638e6766c6544077b37a612c0ae3ceb7'  # IDM APP CLIENT SECRET
   
        raw_auth_code = '{}:{}'.format(self.client_id, self.client_secret)
        self.base_64_auth_code = base64.b64encode(raw_auth_code.encode('utf-8')).decode('utf-8')

        self.redirect_uri = 'http://10.7.52.41:5055/guiscim/auth'  # CALLBACK URL REGISTERED ON IDM (UI APP AUTH ADDRESS)

        self.proxy_address = "http://10.7.52.41:80/"
        self.idm_address = 'http://10.7.52.41:8000/'  # IDM ADDRESS
        self.authorization_url = self.idm_address + 'oauth2/authorize'  # AUTHORIZATION URL
        self.token_url = self.idm_address + 'oauth2/token'  # TOKEN URL

    def authorize_url(self, **kwargs):
        oauth_params = {'response_type': 'code', 'redirect_uri': self.redirect_uri, 'client_id': self.client_id}
        oauth_params.update(kwargs)
        return '{}?{}'.format(self.authorization_url, urlencode(oauth_params))

    def get_token(self, code):
        headers = {'Authorization': 'Basic {}'.format(self.base_64_auth_code),
                   'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': self.redirect_uri}
        response = requests.post(self.token_url, headers=headers, data=data)
        str_response_content = response.content.decode('utf-8')
        token_dict = json.loads(str_response_content)
        return token_dict

    def get_user_info(self, token):
        headers = {"Authorization": "bearer " + token}
        response = requests.get(self.idm_address + 'user?access_token=' + token, headers=headers)
        me_json = response.json()
        return me_json
