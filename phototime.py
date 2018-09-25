import argparse
import os
import exifread
import datetime
import collections

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('dirs', metavar='DIR', type=str, nargs='+',
                    help='directory to scan')

args = parser.parse_args()
timeslots = collections.defaultdict(set)

for dir in args.dirs:
    for root, dirs, filenames in os.walk(dir):
        for filename in filenames:
            try:
                if filename[-3:].lower() in ["dng", "tif", "arw","psd"]:
                    with open(os.path.join(root, filename),'rb') as file:
                        tags = exifread.process_file(file)
                        time = datetime.datetime.strptime(str(tags['Image DateTime']), "%Y:%m:%d %H:%M:%S")
                        round_time = time.strftime("%Y-%m-%d %H:")+str((time.minute//15)*15)
                        if round_time[-2:] == ":0":
                            round_time=round_time+"0"
                        timeslots[str(time.date())].add(round_time)
            except OSError as err:
                pass

print("\n\n Dates:")
total = 0
for d in sorted(timeslots.keys()):
    print(d+"\t"+str(len(timeslots[d])*.25))
    total += len(timeslots[d])*.25
print("\n\nTotal time: "+str(total))
                
