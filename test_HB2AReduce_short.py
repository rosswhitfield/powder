from mantid.simpleapi import HB2AReduce
import glob

failed=[]
failed_msg = []

for filename in glob.iglob('/HFIR/HB2A/IPTS-*/exp6[56]*/Datafiles/HB2A_exp*_scan????.dat'):
    try:
        ws=HB2AReduce(filename)
    except Exception as e:
        failed.append(filename)
        failed_msg.append(e)

for a, b in zip(failed, failed_msg):
    print(a,b)
print(len(failed))
