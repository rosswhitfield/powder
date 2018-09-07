#!/usr/bin/env python
from mantid.simpleapi import CreateWorkspace, Rebin, Divide, SaveFocusedXYE
import numpy as np
import datetime
import sys
import os

filename = sys.argv[1]

regexp = '#(.*)=(.*)'
metadata = dict(np.char.strip(np.fromregex(filename, regexp, dtype='str')))
start_time = datetime.datetime.strptime(metadata['time'] + ' ' + metadata['date'], '%I:%M:%S %p %m/%d/%Y')

indir, data_filename = os.path.split(filename)
_, exp, scan = data_filename.replace(".dat", "").split('_')

gaps_filename = 'HB2A_{}__gaps.txt'.format(exp)
exclude_filename = 'HB2A_{}__exclude_detectors.txt'.format(exp)

gaps = np.cumsum(np.genfromtxt(os.path.join(indir, gaps_filename), usecols=(0)))
exclude_detectors = np.loadtxt(os.path.join(indir, exclude_filename), ndmin=1, dtype=int)

data = np.genfromtxt(filename, skip_header=28, names=True)
counts = np.array([data['anode{}'.format(n)] for n in range(1,45) if n not in exclude_detectors])

twotheta = data['2theta']

monitor = data['monitor']
normalization_monitor = 20000

m1 = data['m1'][0]  # m1 = 0 -> Ge 115, 1.54A
                    # m1 = 9.45 -> Ge 113, 2.41A

colltrans = data['colltrans'][0]    # colltrans = 0 -> IN
                                    # colltrans = +/-80 -> OUT

vcorr_filename = 'HB2A_{}__Ge_{}_{}_vcorr.txt'.format(exp,
                                                      115 if np.isclose(m1, 0, atol=0.1) else 113,
                                                      "IN" if np.isclose(colltrans, 0, atol=0.1) else "OUT")

vcorr = np.genfromtxt(os.path.join(indir, vcorr_filename))

xarray = twotheta+gaps.reshape(1, -1).T
yarray = counts/vcorr.reshape(1, -1).T*normalization_monitor/monitor

# Separate spectrum per anode
anodes = CreateWorkspace(DataX=xarray,
                         DataY=yarray,
                         DataE=np.sqrt(yarray),
                         NSpec=len(xarray))

# All in one spectrum, sorted
index_array = np.argsort(xarray.ravel())
intermediate = CreateWorkspace(DataX=xarray.ravel()[index_array],
                               DataY=yarray.ravel()[index_array],
                               DataE=np.sqrt(yarray.ravel()[index_array]))

# Binned data
binning = 0.05

d = (counts/monitor).ravel()
e = (np.sqrt(counts)/monitor).ravel()
data = CreateWorkspace(DataX=xarray.ravel()[index_array],
                       DataY=d[index_array],
                       DataE=np.sqrt(d[index_array]))

n = np.repeat(vcorr, len(xarray.T)).ravel()/normalization_monitor
norm = CreateWorkspace(DataX=xarray.ravel()[index_array],
                       DataY=n[index_array],
                       DataE=np.sqrt(n[index_array]))

data = Rebin(data, Params=binning)
norm = Rebin(norm, Params=binning)

ws = Divide(data, norm)

SaveFocusedXYE(ws, Filename='out.xye', SplitFiles=False, IncludeHeader=False)

c = CreateWorkspace(DataX=xarray.ravel()[index_array],
                    DataY=counts.ravel()[index_array],
                    DataE=np.sqrt(counts.ravel()[index_array]))

n = CreateWorkspace(DataX=xarray.ravel()[index_array],
                    DataY=n[index_array],
                    DataE=np.sqrt(n[index_array]))

#data = Rebin(data, Params=binning)
#norm = Rebin(norm, Params=binning)

d = Divide(c, n)

