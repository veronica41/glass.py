# Libs imports
import flask
import rauth
import json
import os
import sys

# Local imports
from user import User
from subscriptions import Subscriptions

SSL_KEY_FILE = "keys/vm012.elijah.cs.cmu.edu.key.pem"
SSL_CRT_FILE = "keys/vm012.elijah.cs.cmu.edu.crt.pem"

OAUTH_ACCESS_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
OAUTH_AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth"
OAUTH_REDIRECT_URI = "authentification/google"
OAUTH_API_BASE_URL = "https://www.googleapis.com/"
OAUTH_SCOPES = [
    'https://www.googleapis.com/auth/glass.location',
    'https://www.googleapis.com/auth/glass.timeline',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]

class Application(object):
    def __init__(self, 
                name="",
                client_id=None,
                client_secret=None,
                scopes=OAUTH_SCOPES,
                debug=True,
                template_folder='templates',
                **flaskargs):
        self.name = name
        self.debug = debug
        self.web = flask.Flask(self.name, **flaskargs)
        self.template_folder = template_folder
        self.logger = self.web.logger
        self.scopes = scopes
        self.subscriptions = Subscriptions(app=self)
        self.oauth = rauth.OAuth2Service(name=self.name,
                                  client_id=client_id,
                                  client_secret=client_secret,
                                  access_token_url=OAUTH_ACCESS_TOKEN_URL,
                                  authorize_url=OAUTH_AUTHORIZE_URL,
                                  base_url=OAUTH_API_BASE_URL)

    @property
    def oauth_redirect_uri(self):
        return "%s://%s/glass/oauth/callback" % ("https" if self.secure else "http", self.host)

    def _oauth_authorize(self):
        """
        (view) Display the authorization window for Google Glass
        """
        params = {
            'approval_prompt': 'force',
            'scope': " ".join(self.scopes),
            'state': '/profile',
            'redirect_uri': self.oauth_redirect_uri,
            'response_type': 'code'
        }
        url = self.oauth.get_authorize_url(**params)
        return flask.redirect(url)

    def _oauth_callback(self):
        """
        (view) Callback for the oauth
        """
        token = self.oauth.get_access_token(data={
            'code': flask.request.args.get('code', ''),
            'redirect_uri': self.oauth_redirect_uri,
            'grant_type': 'authorization_code'
        }, decoder=json.loads)
        user = User(token=token, app=self)

        # Add subscriptions
        self.subscriptions.init_user(user)

        # Call endpoint for user login
        return self.subscriptions.call_endpoint("login", user) or ""

    def prepare(self, host="localhost", port=8080, debug=None, secure=False, public=False):
        """
        Prepare the application server
        """
        self.port = port
        self.host = host
        self.secure = secure
        self.public = public

        if port != 80:
            self.host = "%s:%i" % (self.host, self.port)

        # OAUTH
        self.web.add_url_rule('/glass/oauth/authorize', 'oauth_authorize', self._oauth_authorize)
        self.web.add_url_rule('/glass/oauth/callback', 'oauth_callback', self._oauth_callback)

        self.web.debug = debug or self.debug

        self.ssl_context = None
        if self.secure:
            from OpenSSL import SSL
            self.ssl_context = SSL.Context(SSL.TLSv1_METHOD)
            dir = os.path.dirname(sys.argv[0])
            if dir == '':
                dir = os.curdir
            self.ssl_context.use_privatekey_file(os.path.join(dir, SSL_KEY_FILE))
            self.ssl_context.use_certificate_file(os.path.join(dir, SSL_CRT_FILE))

    def run(self, **kwargs):
        self.prepare(**kwargs)
        self.web.run(port=self.port, host=("0.0.0.0" if self.public else "127.0.0.1"),
            ssl_context = self.ssl_context)


