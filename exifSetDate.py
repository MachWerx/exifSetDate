#!/usr/bin/python
import argparse
import datetime
import os
import sys
import time

from PIL import Image

parser = argparse.ArgumentParser(description=
    'Sets modification date of the file to match the photo creation date.')
parser.add_argument(
    'files', metavar='file', type=str, nargs='+', help='File to update')
args = parser.parse_args()

for file in args.files:
  img = Image.open(file)
  exif = img.getexif()
  if 36867 in exif:
    timestamp = exif[36867]
    print file + ': ' + timestamp
    [date_string, time_string] = timestamp.split()
    [year, month, day] = date_string.split(':')
    [hour, minute, second] = time_string.split(':')
    date = datetime.datetime(
        year=int(year), month=int(month), day=int(day),
        hour=int(hour), minute=int(minute), second=int(second))
    modTime = time.mktime(date.timetuple())
    os.utime(file, (modTime, modTime))
  else:
    print file + ': missing EXIF data.'
