#!/usr/bin/env python

import numpy as np
import sys
import os

filename = sys.argv[1]
outdir = sys.argv[2]
vanadium_filename = sys.argv[3]

vanadium = np.genfromtxt(vanadium_filename)
vanadium_count = vanadium[:, 5:49].sum(axis=0)
vanadium_monitor = vanadium[:, 3].sum()

indir, data_filename = os.path.split(filename)
_, exp, scan = data_filename.replace(".dat", "").split('_')

gaps_filename = 'HB2A_{}__gaps.txt'.format(exp)

data = np.genfromtxt(filename)
gaps = np.cumsum(np.genfromtxt(os.path.join(indir, gaps_filename), usecols=(0)))

counts = data[:, 5:49].T

twotheta = data[:, 1]

monitor = data[:, 3]

xarray = twotheta+gaps[:, np.newaxis]
yarray = counts/vanadium_count[:, np.newaxis]*vanadium_monitor/monitor
earray = np.sqrt(1/counts + 1/vanadium_count[:, np.newaxis] + 1/vanadium_monitor + 1/monitor)*yarray

np.savetxt(os.path.join(outdir, '{}.dat'.format(scan)),
           np.transpose((xarray.flatten(), yarray.flatten(), earray.flatten())),
           fmt='%.3f')

tolerance = 0.06

bins = np.arange(xarray.min(), xarray.max()+tolerance, tolerance)
inds = np.digitize(xarray.ravel(), bins)

# because np.broadcast_to is not in numpy 1.7.1 we use stride_tricks
vanadium_count=np.lib.stride_tricks.as_strided(vanadium_count, shape=counts.shape, strides=(vanadium_count.strides[0],0))
monitor=np.lib.stride_tricks.as_strided(monitor, shape=counts.shape, strides=(monitor.strides[0],0))

counts_binned = np.bincount(inds, weights=counts.ravel(), minlength=len(bins))
vanadium_binned = np.bincount(inds, weights=vanadium_count.ravel(), minlength=len(bins))
monitor_binned = np.bincount(inds, weights=monitor.ravel(), minlength=len(bins))
vanadium_monitor_binned = np.bincount(inds, minlength=len(bins))*vanadium_monitor

y = counts_binned/vanadium_binned*vanadium_monitor_binned/monitor_binned
e = np.sqrt(1/counts_binned + 1/vanadium_binned + 1/vanadium_monitor + 1/monitor_binned)*y

np.savetxt(os.path.join(outdir, '{}_binned.dat'.format(scan)),
           np.transpose(((bins[1:]+bins[:-1])/2, np.nan_to_num(y[1:]), np.nan_to_num(e[1:]))),
           fmt='%.5f')
