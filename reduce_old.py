#!/usr/bin/env python

import numpy as np
import sys
import os

filename = sys.argv[1]
outdir = sys.argv[2]

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

corr_filename = 'HB2A_{}__Ge_{}_{}_vcorr.txt'.format(exp,
                                                     115 if np.isclose(m1, 0, atol=0.1) else 113,
                                                     "IN" if np.isclose(colltrans, 0, atol=0.1) else "OUT")

corr = np.genfromtxt(os.path.join(indir, corr_filename))

xarray = twotheta+gaps.reshape(1, -1).T
yarray = counts/corr.reshape(1, -1).T*normalization_monitor/monitor

np.savetxt(os.path.join(outdir, '{}.dat'.format(scan)),
           np.transpose((xarray.flatten(), yarray.flatten(), np.ones_like(xarray.flatten()))),
           fmt='%.3f')

index_array = np.argsort(xarray.flatten())

x = xarray.flatten()
y = yarray.flatten()

tolerance = 0.0505

x_out = []
y_out = []
e_out = []

while True:
    x_store = np.nanmin(x)
    mask = np.logical_and(x >= x_store, x <= x_store+tolerance)
    x_out.append(np.nanmean(x[mask]))
    y_out.append(np.nanmean(y[mask]))
    e_out.append(np.sqrt(np.nansum(y[mask]))/np.sum(mask))
    x[mask]=np.nan
    y[mask]=np.nan
    if np.nansum(x) == 0:
        break


np.savetxt(os.path.join(outdir, '{}_binned_old.dat'.format(scan)),
                      np.transpose((x_out, y_out, e_out)),
                      fmt='%.3f')
