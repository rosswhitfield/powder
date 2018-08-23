#!/usr/bin/env python

import numpy as np
import sys
import os

filename = sys.argv[1]

regexp = '#(.*)=(.*)'
metadata = dict(np.char.strip(np.fromregex(filename, regexp, dtype='str')))


