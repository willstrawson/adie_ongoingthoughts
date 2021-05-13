# Script to add Age and Gender variables to the master participants.tsv

import glob
import pandas as pd

# read in demographics.tsv files as pd data frames
data = ['/research/cisc2/projects/critchley_adie/BIDS_data/derivatives/phenotype/controls/demographics.tsv', \
'/research/cisc2/projects/critchley_adie/BIDS_data/derivatives/phenotype/patients/demographics.tsv']
# concatanate these data frames into one
df = pd.concat([pd.read_csv(data[0]), pd.read_csv(data[1])])

# read in target dataframe
target = pd.read_csv('/research/cisc2/projects/critchley_adie/BIDS_data/participants.tsv')

