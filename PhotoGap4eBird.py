#!/usr/bin/python3

import os
import csv
import argparse

photoFile = 'required.csv'
listFile = 'ebird_world_life_list.csv'
missingFile = 'missing_photos.csv'

def parseArgs():
    # Process command line arguments
    global photoFile
    global listFile
    global missingFile

    # Create an argument parser
    parser = argparse.ArgumentParser(
        prog='PhotoGap4eBird.py',
        description = 'Compare 2 eBird csv files (the world life list and the list of birds with photos) to identify birds without photos')

    # Define the arguments
    parser.add_argument("-p","--photo-file",help='exported file with list of photos (required)',required=True,action='store')
    parser.add_argument("-l","--life-list-file",help='exported world life list (optional)',default='ebird_world_life_list.csv',required=False,action='store')
    parser.add_argument("-m","--missing-photos-file",help='output csv file (optional)',default='missing_photos.csv',required=False,action='store')

    # Parse the arguments
    args = parser.parse_args()

    # use the arguments to define the file names
    photoFile   = args.photo_file
    listFile    = args.life_list_file
    missingFile = args.missing_photos_file

    # check for file existance
    if not os.path.isfile(photoFile):
        print("Missing file:",photoFile)
        exit()
    if not os.path.isfile(photoFile):
        print("Missing file:",photoFile)
        exit()


# Main script start here with parsing the arguments
parseArgs()

count = 0 # Used to identify the first line of each file
PhotoSet = set()
print("Reading photos file (",photoFile,")",sep='')
with open(photoFile, mode ='r') as file:
   
  csvFile = csv.reader(file)
 
  for line in csvFile:
      count = count + 1
      if count == 1:
          # first line have the header, and field 0 is 'ML Catalog Number', field 1 is 'Format', and field 3 is 'Common Name'
          assert(line[1].strip() == 'Format' and line[2].strip() == 'Common Name')
          continue
      # This script only process 'Photo' in the 'Format' field
      if line[1].strip() == 'Photo':
          PhotoSet.add(line[2].strip()) # Add the 'Common Name' to the set of photos
          # Note that species with subspecies in parenthesis must be added twice to the set
          parenthesis = line[2].find('(')
          if parenthesis > 0: # Note that a specie name cannot start with '('
              PhotoSet.add(line[2][:parenthesis].strip())

count = 0
heading = [] # used to preserve the header line
MissingPhotos = []
print("Reading worls life list file (",listFile,")",sep='')
with open(listFile, mode ='r') as file:
   
  csvFile = csv.reader(file)
 
  for line in csvFile:
      count = count + 1
      if count == 1:
          # first line have the header, and field 3 is 'Common Name'
          assert(line[3].strip() == 'Common Name')
          heading = line # save the heading line (first line of the file)
          continue
      # if the 'Common Name' is not in the set, then we found a specie without photos
      if not line[3].strip() in PhotoSet:
          MissingPhotos.append(line)

count = 0
# If we found missing photos then let generate a new csv file
if MissingPhotos:
    with open(missingFile, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(heading)
        for line in MissingPhotos:
            count = count + 1
            writer.writerow(line)

print("\nTOTAL missing photos", count,"\nWriting output file:",missingFile)

