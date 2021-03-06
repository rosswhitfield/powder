#!/usr/bin/env python2
import os
import sys
import pyoncat
import getpass
try:
    from postprocessing.publish_plot import publish_plot
except ImportError:
    from finddata import publish_plot

sys.path.insert(0, "/opt/mantidnightly/bin")
from mantid.simpleapi import HB2AReduce, SaveFocusedXYE, SavePlot1D

filename = sys.argv[1]
output_file = os.path.split(filename)[-1].replace('.dat', '.xye')
outdir = sys.argv[2]

ws = HB2AReduce(filename)
SaveFocusedXYE(ws, Filename=os.path.join(outdir, output_file), SplitFiles=False, IncludeHeader=False)

div = SavePlot1D(ws, OutputType='plotly')

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

datafile = oncat.Datafile.retrieve(
    filename,
    facility="HFIR",
    instrument="HB2A",
    experiment=ipts,
    projection=["indexed.run_number",
                "metadata.scan_title",
                "metadata.time",
                "metadata.date",
                "metadata.Sum of Counts",
                "metadata.experiment",
                "metadata.experiment_number",
                "metadata.proposal",
                "metadata.scan"],
)

datadict = datafile.to_dict()

# create summary table

table ='<div></div><p></p><table class="info display">'
row = '<tr><td>{}</td><td>{}</td></tr>'
table += row.format('Scan', '<b>{} - {}</b>'.format(datadict.get('metadata').get('scan',''), datadict.get('metadata').get('scan_title','')))
table += row.format('Experiment', '{} - {}'.format(datadict.get('metadata').get('experiment_number',''), datadict.get('metadata').get('experiment','')))
table += row.format('IPTS', datadict.get('metadata').get('proposal',''))
table += row.format('Run start', datadict.get('metadata').get('date','') + ' ' + datadict.get('metadata').get('time',''))
table += row.format('Total counts', datadict.get('metadata').get('Sum of Counts',''))
table += '</table><p></p>'

try:
    runNumber = datafile.indexed['run_number']
    request = publish_plot('HB2A', runNumber, files={'file': table+div}, config='/SNS/users/rwp/post_processing.conf')
except KeyError:
    print("This file doesn't have a run number")
