import argparse
import os
import exifread
import datetime
import collections
import csv
from collections import defaultdict

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('dirs', metavar='DIR', type=str, nargs='+',
                    help='directory to scan')

args = parser.parse_args()
timeslots = collections.defaultdict(set)
count = defaultdict(list)

for dir in args.dirs:
    for root, dirs, filenames in os.walk(dir):
        for filename in filenames:
            try:
                # print(filename)
                if filename[-3:].lower() in ["dng", "tif", "arw","psd","jpg"]:
                    with open(os.path.join(root, filename),'rb') as file:
                        tags = exifread.process_file(file)
                        # print(tags)
                        time = datetime.datetime.strptime(str(tags['EXIF DateTimeOriginal']), "%Y:%m:%d %H:%M:%S")
                        # print(time)
                        round_time = time.strftime("%Y-%m-%d %H:")+str((time.minute//15)*15)
                        if round_time[-2:] == ":0":
                            round_time=round_time+"0"
                        timeslots[str(time.date())].add(round_time)
                        count[time.strftime("%Y-%m-%d")].append(filename)
            except OSError as err:
                print(OSError)
                pass

print("\n\nDates:")
total = 0
for d in sorted(timeslots.keys()):
    print(d+"\t"+str(len(timeslots[d])*.25))
    print("   ",)
    total += len(timeslots[d])*.25
print("\n\nTotal time: "+str(total))

print("\n\nCount")
total = 0
for d in sorted(count):
    print("\t"+d+": "+str(len(count[d])))
    total += len(count[d])
    # print("\t\t",count[d])
print("Total:" + str(total))

with open('timesheet.csv', 'w') as f:
    f.write("Date,Photography,Processing\n")
    for d in sorted(timeslots.keys()):
        f.write(d+", "+str(len(timeslots[d])*.25)+", "+str(len(timeslots[d])*.25)+"\n")
    f.write("\nTotal:,"+str(total*2)+" hours")