# file paths within following tsv files need to have a name conervsion:
# BIDS_Data/sub-*/*/sub-*_scans.tsv

from adie import convert
import os
import glob

dataloc = '/research/cisc2/projects/critchely_adie/BIDS_data/'

# access conversion dict 
conversion_file = 'sourcedata/adie_idconvert.txt'
rename = adie.convert.convert_dict(os.path.join(dataloc, conversion_file))

# get all file paths to .tsvs 
files_to_conv = glob.glob(os.path.join(dataloc, 'sub-*/ses-*/sub-*_scans.tsv'))

# open and read in files
for fl in files_to_conv:
    f = open(fl)
    # save all lines as string in list 
    l = f.readlines()


# identify and save lines containing names 
idmatch(string-from-txt-file, rename) # this function should return both cisc and adie id if found in string 

# replace cisc names wth ADIE names 

# save files 






