# file paths within following tsv files need to have a name conervsion:
# BIDS_Data/sub-*/*/sub-*_scans.tsv

from adie import convert
import os
import glob

dataloc = '/research/cisc2/projects/critchley_adie/BIDS_data/'
# access conversion dict 
conversion_file = 'sourcedata/adie_idconvert.txt'
rename = convert.convert_dict(os.path.join(dataloc, conversion_file))

# get all file paths to .tsvs 
files_to_conv = glob.glob(os.path.join(dataloc, 'sub-*/ses-*/sub-*_scans.tsv'))
print('Files to be converted:','\n',files_to_conv)

# open and read in files, one per participant 
for fl in files_to_conv:
    fin = open(fl)
    # save all lines as string in list 
    l = fin.readlines()    
    # open output file 
    fout = open(fl, "wt")
    # loop through each line (entry in list) and replace CISC with ADIE ID 
    for line in l:
        # this function should return both cisc and adie id if found in string 
        newid, oldid = convert.idmatch(str(l), rename)
        print('OLD LINE = ', line)
        # remove 'sub-' to avoid duplicaton
        line = line.replace('sub-','')
        line = line.replace(oldid, newid)
        print('NEW LINE = ', line)
        # fout
        fout.write(line)
    # close file
    fin.close()
    fout.close()







