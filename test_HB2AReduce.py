from mantid.simpleapi import HB2AReduce
import glob

failed=[]

for filename in glob.iglob('/HFIR/HB2A/IPTS-*/exp6*/Datafiles/HB2A_exp*_scan*.dat'):
    try:
        ws=HB2AReduce(filename)
    except:
        failed.append(filename)

print(failed)
print(len(failed))
