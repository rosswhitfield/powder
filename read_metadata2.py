#!/usr/bin/env python
import numpy as np
import sys
import os
import datetime
import re

filename = sys.argv[1]

metadata = dict([np.char.strip(re.split('#(.*?)=(.*)', line, flags=re.U)[1:3]) for line in open(filename) if re.match('^#.*=', line)])

