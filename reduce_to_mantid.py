#!/usr/bin/env python
from mantid.simpleapi import CreateWorkspace, Rebin, Divide, SaveFocusedXYE
import numpy as np
import sys
import os

filename = sys.argv[1]

indir, data_filename = os.path.split(filename)
_, exp, scan = data_filename.replace(".dat", "").split('_')

gaps_filename = 'HB2A_{}__gaps.txt'.format(exp)

data = np.genfromtxt(filename)
gaps = np.cumsum(np.genfromtxt(os.path.join(indir, gaps_filename), usecols=(0)))

counts = data[:, 5:49].T

twotheta = data[:, 1]

monitor = data[:, 3]
normalization_monitor = 20000

m1 = data[0, 49]    # m1 = 0 -> Ge 115, 1.54A
                    # m1 = 9.45 -> Ge 113, 2.41A

colltrans = data[0, 53]     # colltrans = 0 -> IN
                            # colltrans = +/-80 -> OUT

vcorr_filename = 'HB2A_{}__Ge_{}_{}_vcorr.txt'.format(exp,
                                                      115 if np.isclose(m1, 0, atol=0.1) else 113,
                                                      "IN" if np.isclose(colltrans, 0, atol=0.1) else "OUT")

vcorr = np.genfromtxt(os.path.join(indir, vcorr_filename))

xarray = twotheta+gaps.reshape(1, -1).T
yarray = counts/vcorr.reshape(1, -1).T*normalization_monitor/monitor

anodes = CreateWorkspace(DataX=xarray,
                         DataY=yarray,
                         DataE=np.sqrt(yarray),
                         NSpec=len(xarray))

index_array = np.argsort(xarray.ravel())

d = (counts/monitor).ravel()
data = CreateWorkspace(DataX=xarray.ravel()[index_array],
                       DataY=d[index_array])

n = np.repeat(vcorr, len(xarray.T)).ravel()/normalization_monitor
norm = CreateWorkspace(DataX=xarray.ravel()[index_array],
                       DataY=n[index_array])

data = Rebin(data, Params='0.05')
norm = Rebin(norm, Params='0.05')

ws = Divide(data, norm)

SaveFocusedXYE(ws, Filename='out.xye', SplitFiles=False, IncludeHeader=False)
