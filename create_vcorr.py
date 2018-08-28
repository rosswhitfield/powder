#!/usr/bin/env python
import numpy as np
import sys
import os

filename = sys.argv[1]

indir, data_filename = os.path.split(filename)
_, exp, scan = data_filename.replace(".dat", "").split('_')

data = np.genfromtxt(filename)

counts = data[:, 5:49].sum(axis=0)
vcorr = counts/counts[24]

m1 = data[0, 49]    # m1 = 0 -> Ge 115, 1.54A
                    # m1 = 9.45 -> Ge 113, 2.41A

colltrans = data[0, 53]     # colltrans = 0 -> IN
                            # colltrans = +/-80 -> OUT

vcorr_filename = 'HB2A_{}__Ge_{}_{}_vcorr.txt'.format(exp,
                                                     115 if np.isclose(m1, 0, atol=0.1) else 113,
                                                     "IN" if np.isclose(colltrans, 0, atol=0.1) else "OUT")

np.savetxt(vcorr_filename, vcorr, fmt='%.5g')
