#!/usr/bin/env python
import numpy as np
import sys
import os
import datetime
import re

filename = sys.argv[1]

with open(filename) as f:
    metadata = dict([np.char.strip(re.split('#(.*?)=(.*)', line, flags=re.U)[1:3]) for line in f if re.match('^#.*=', line)])


with open(filename) as f:
    lines = f.readlines()

metadata = dict([np.char.strip(re.split('#(.*?)=(.*)', line, flags=re.U)[1:3]) for line in lines if re.match('^#.*=', line)])

header = np.argmax([not bool(re.match('^#', line)) for line in lines])-1
header = np.argmax([bool(re.match('(?!^#)', line)) for line in lines])-1

data = np.genfromtxt(lines, names=True, skip_header=header)
