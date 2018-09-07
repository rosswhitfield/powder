#!/usr/bin/env python
import numpy as np
import sys
import os
import datetime

filename = sys.argv[1]

regexp = '#(.*?)=(.*)'
metadata = dict(np.char.strip(np.fromregex(filename, regexp, dtype='str')))

run_title = metadata['scan_title']
start_time = datetime.datetime.strptime(metadata['time'] + ' ' + metadata['date'], '%I:%M:%S %p %m/%d/%Y')

data = np.genfromtxt(filename, skip_header=28, names=True)
counts = np.array([data['anode{}'.format(n)] for n in range(1,45)])

names = data.dtype.names

pt = data['Pt']
twoTheta = data['2theta']
time = data['time']
time_array = [start_time + datetime.timedelta(seconds=s) for s in np.cumsum(time)]
monitor = data['monitor']
m1 = data['m1'][0]
colltrans = data['colltrans'][0]
hi_pressure = data['hi_pressure']
sample = data['sample']
temp = data['temp']
temp_2 = data['temp_2']
needlevalve_pressure = data['needlevalve_pressure']
needlevalve_setpoint = data['needlevalve_setpoint']
