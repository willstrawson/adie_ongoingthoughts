# Script to add Age and Gender variables to the master participants.tsv

import glob
import pandas as pd

# read in demographics.tsv files as pd data frames
data = ['/research/cisc2/projects/critchley_adie/BIDS_data/derivatives/phenotype/controls/demographics.tsv', \
'/research/cisc2/projects/critchley_adie/BIDS_data/derivatives/phenotype/patients/demographics.tsv']
# concatanate these data frames into one
df = pd.concat([pd.read_csv(data[0], sep='\t'), pd.read_csv(data[1], sep='\t')])

# read in target dataframe
target_path = ('/research/cisc2/projects/critchley_adie/BIDS_data/participants.tsv')
target = pd.read_csv(target_path)

# print dataframes
print(df)
print(target)

# merge gender columns from dfs into target on participant key 
merged=pd.merge(left=df[['participant_id','Age','GenderID','GenderBirth']], right=target, on=['participant_id'],how='outer')
print(merged)

#save 
merged.to_csv(target_path,sep='\t')
