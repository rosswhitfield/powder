import pyoncat
import getpass
import sys

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
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    token_getter=token_store.get_token,
    token_setter=token_store.set_token,
    flow=pyoncat.RESOURCE_OWNER_CREDENTIALS_FLOW
)

if token_store.get_token() is None:
    username = getpass.getuser()
    password = getpass.getpass()
    oncat.login(username, password)

filename = sys.argv[1]
ipts = filename.split('/')[3]

projection=["location", "metadata.completed", "metadata.command", "metadata.scan_title", "indexed.scan_number", "metadata.samplename"]

datafiles = oncat.Datafile.list(
    facility="HFIR",
    instrument="HB2A",
    experiment=ipts,
    projection=projection
)

import csv

def extract_value(datafile, proj):
    output = datafile.to_dict()
    proj = proj.split('.')
    try:
        while len(proj) > 0:
            output = output.get(proj.pop(0))
        if output is None:
            return ''
        else:
            return output
    except AttributeError:
        return ''


with open(ipts+'.csv', 'w') as f:
    # Header
    f.write(','.join(proj.split('.')[-1] for proj in projection)+'\n')
    # datafiles
    for datafile in datafiles:
        if len(datafile.indexed) == 0:
            continue
        f.write(', '.join(str(extract_value(datafile, proj)) for proj in projection)+'\n')
