import pyoncat
import getpass
import sys
import os

CLIENT_ID = '9e736eae-f90c-4513-89cf-53607eee5165'
CLIENT_SECRET = None

class InMemoryTokenStore(object):
    def __init__(self):
        self._token = None

    def set_token(self, token):
        self._token = token

    def get_token(self):
        return self._token

token_store = InMemoryTokenStore()

oncat = pyoncat.ONCat(
    'https://oncat.ornl.gov',
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    token_getter = token_store.get_token,
    token_setter = token_store.set_token,
    flow = pyoncat.RESOURCE_OWNER_CREDENTIALS_FLOW
)

if token_store.get_token() is None:
    username = getpass.getuser()
    password = getpass.getpass()        
    # If there is no previously-stored token for this user, then their login
    # credentials must be retrieved first.  It is up to you to decide the most
    # appropriate way to do this for your application, and how to display the
    # user's logged-in status (if at all).
    #
    # For the purposes of this example we have just hard-coded the credentials.
    oncat.login(username, password)

filename = sys.argv[1]
ipts = filename.split('/')[3]
_, exp, scan = data_filename.replace(".dat", "").split('_')

datafile = oncat.Datafile.retrieve(
    filename,
    facility = "HFIR",
    instrument = "HB2A",
    experiment = ipts,
    projection = ["indexed.run_number"],
)

print(datafile)
