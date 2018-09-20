#!/usr/bin/env python2
import os
import sys
import pyoncat
import client
import numpy as np
try:
    from postprocessing.publish_plot import publish_plot
except ImportError:
    from finddata import publish_plot

sys.path.insert(0, "/opt/mantidnightly/bin")
from mantid.simpleapi import HB2AReduce, SaveFocusedXYE, SavePlot1D, SaveAscii

filename = sys.argv[1]
output_file = os.path.split(filename)[-1].replace('.dat', '.xye')
outdir = sys.argv[2]

ws = HB2AReduce(filename)

def_y = ws.getRun().getLogData('def_y').value
def_x = ws.getRun().getLogData('def_x').value

anode=None
if 'anode' in def_y: # Plot anode intensity instead
    try:
        anode = int(def_y.replace('anode',''))
    except ValueError:
        pass

if anode: # Re-reduce data for anode plot
    ws = HB2AReduce(filename, IndividualDetectors=True)
    SaveAscii(ws, Filename=os.path.join(outdir, output_file), SpectrumList=anode-1, Separator='Space', ColumnHeader=False, WriteSpectrumID=False)
    div = SavePlot1D(ws, OutputType='plotly', SpectraList=anode)
else:
    # Check binning is correct, if not re-reduce
    if ws.getRun().hasProperty(def_x):
        x = ws.getRun().getLogData(def_x).value
        if len(x)>1:
            step_size = (x[-1]-x[0])/(len(x)-1)
            if not np.isclose(step_size, 0.05, atol=0.001):
                ws = HB2AReduce(filename,BinWidth=step_size)
    SaveFocusedXYE(ws, Filename=os.path.join(outdir, output_file), SplitFiles=False, IncludeHeader=False)
    div = SavePlot1D(ws, OutputType='plotly')

oncat = pyoncat.ONCat(
    'https://oncat.ornl.gov',
    client_id=client.ID,
    client_secret=client.SECRET,
    flow=pyoncat.CLIENT_CREDENTIALS_FLOW
)

oncat.login()

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
    runNumber = datafile.to_dict()['indexed']['run_number']
    request = publish_plot('HB2A', runNumber, files={'file': table+div})
except KeyError:
    print("This file doesn't have a run number")
