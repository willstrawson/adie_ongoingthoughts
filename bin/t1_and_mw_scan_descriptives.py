"""
Author: Will Strawson and Hao-Ting Wang, last updated 22/03/2021

Aim: to reveal basic descriptives of the BIDS data set re: mind wandering and T1 scans
Usage: running the script in terminal will reveal important details and also relevent dataframe.
Must be run from within SN analysis server due to paths.
Script is self-contained i.e. no imported user functions.

"""

import glob
import os
import pandas as pd


# Save - set to True if updating output
SAVE = False

pd.set_option("display.max_rows", 1000)

bids = glob.glob("/research/cisc2/projects/critchley_adie/BIDS_data/sub-*")
neuro_baseline = glob.glob(
    "/research/cisc2/projects/critchley_adie/BIDS_data/sub-*/ses-baseline/neuro"
)
neuro_posttraining = glob.glob(
    "/research/cisc2/projects/critchley_adie/BIDS_data/sub-*/posttraining/neuro"
)
t1_baseline = glob.glob(
    "/research/cisc2/projects/critchley_adie/BIDS_data/sub-*/ses-baseline/neuro/anat/sub-*_run-00*_T1w.nii.gz"
)
t1_posttraining = glob.glob(
    "/research/cisc2/projects/critchley_adie/BIDS_data/sub-*/posttraining/neuro/anat/sub-*_run-00*_T1w.nii.gz"
)
mw_baseline = glob.glob(
    "/research/cisc2/projects/critchley_adie/BIDS_data/sub-*/ses-baseline/neuro/func/sub-*_task-mw_run-00*_bold.nii.gz"
)
mw_posttraining = glob.glob(
    "/research/cisc2/projects/critchley_adie/BIDS_data/sub-*/posttraining/neuro/func/sub-*_task-mw_run-00*_bold.nii.gz"
)


def adie_con_split(paths):
    """function to reveal how many paths are from experimental and control subjects"""
    controls = [i for i in paths if "sub-CON" in i]
    n_controls = len(controls)
    adie = [i for i in paths if "sub-ADIE" in i]
    n_adie = len(adie)
    print(
        "Total = {}, ADIE = {}, Controls = {}\n".format(
            n_controls + n_adie, n_adie, n_controls
        )
    )


print("Number of subs in BIDS directory: {}".format(len(bids)))
adie_con_split(bids)

print(
    "Number of subs with baseline/neuro directory: {}".format(
        len(neuro_baseline)
    )
)
adie_con_split(neuro_baseline)
print(
    f"Number of subs with posttraining/neuro directory: {len(neuro_posttraining)}"
)
adie_con_split(neuro_posttraining)

print(f"Number of T1s in ses-baseline: {len(t1_baseline)}")
adie_con_split(t1_baseline)
print(f"Number of T1s in posttraining: {len(t1_posttraining)}")
adie_con_split(t1_posttraining)

print(f"Number of MW funcs in ses-baseline: {len(mw_baseline)}")
adie_con_split(mw_baseline)
print(f"Number of MW funcs in posttraining: {len(mw_baseline)}")
adie_con_split(mw_posttraining)

# Create dataframe
# Row = sub
# Colums = Baseline T1, Posttraining T1, Mindwandering baseline, Mind-wandering postrtaining

# get sub names
subs = [os.path.basename(i) for i in bids]
df = pd.DataFrame(subs)
df.rename(columns={0: "subjects"}, inplace=True)


# Create dictionaries for columns
# create dictionary where key = sub & val = number of niftis
t1_bl = {}
t1_pt = {}

mw_bl = {}
mw_pt = {}

# Create empty columns
df["t1_bl"] = 0
df["t1_pt"] = 0
df["mw_bl"] = 0
df["mw_pt"] = 0

# Create columns showing how many of each nifti each subject has
for i in subs:
    t1_bl[i] = [lst for lst in t1_baseline if i in lst]
    df["t1_bl"].loc[df["subjects"] == i] = len(t1_bl[i])

    t1_pt[i] = [lst for lst in t1_posttraining if i in lst]
    df["t1_pt"].loc[df["subjects"] == i] = len(t1_pt[i])

    mw_bl[i] = [lst for lst in mw_baseline if i in lst]
    df["mw_bl"].loc[df["subjects"] == i] = len(mw_bl[i])

    mw_pt[i] = [lst for lst in mw_posttraining if i in lst]
    df["mw_pt"].loc[df["subjects"] == i] = len(mw_pt[i])


# How many subjects are there with at least one T1 scan and both pre-and post-training mind wandering scans?
full = df[
    (df["mw_bl"] != 0)
    & (df["mw_pt"] != 0)
    & ((df["t1_bl"] != 0) | (df["t1_pt"] != 0))
]
print(
    f"Number of subjects with (i) both baseline and post-training MW and (ii) at least one T1: {len(full)}"
)


# How many subjects with at least one T1 and a baseline MW scan?
partial = df[(df["mw_bl"] != 0) & ((df["t1_bl"] != 0) | (df["t1_pt"] != 0))]
print(
    f"Number of subjects with (i) baseline MW and (ii) at least one T1: {len(partial)}"
)

print(df)

# Merge with existing participants.tsv df
if SAVE:
    # import participants.tsv
    participants = pd.read_csv(
        "/research/cisc2/projects/critchley_adie/BIDS_data/participants.tsv",
        sep="\t",
    )
    # change participant column to match
    df.rename(columns={"subjects": "participant_id"}, inplace=True)
    # remove 'sub-' from df
    df["participant_id"] = df["participant_id"].str.replace("sub-", "")
    # merge
    df_master = df.merge(participants, on="participant_id", how="outer")
    df_master.to_csv(
        "/research/cisc2/projects/critchley_adie/BIDS_data/participants.tsv",
        index=False, sep="\t"
    )
