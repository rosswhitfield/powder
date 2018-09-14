#!/usr/bin/env python2
import os
import sys
sys.path.insert(0, "/opt/mantidnightly/bin")
from mantid.simpleapi import HB2AReduce, SaveFocusedXYE

filename = sys.argv[1]
output_file = os.path.split(filename)[-1].replace('.dat', '.xye')
outdir = sys.argv[2]

ws = HB2AReduce(filename)
SaveFocusedXYE(ws, Filename=os.path.join(outdir, output_file), SplitFiles=False, IncludeHeader=False)
