# Script to add session name into the name of all files under BIDS_dir
import glob
import os
import subprocess
os.chdir('/research/cisc2/projects/critchley_adie/BIDS_data')

subdirs = glob.glob('sub-*/ses-*/anat') #only perform on subjects with anatomical 
subdirs = [os.path.dirname(os.path.dirname(s)) for s in subdirs]

print(subdirs)

def seslist(sub):
    """
    list session for given partcipant 
    """ 
    seslist=glob.glob('{}/ses-*'.format(sub))
    return seslist

def listfiles(seslist,sub):
    """
    list files that need modifying
    """

    filelist=[]
    filelist_func=glob.glob('{}/{}/func/*'.format(sub,'ses-*'))
    filelist_anat=glob.glob('{}/{}/anat/*'.format(sub,'ses-*'))
    filelist.append(filelist_func)
    filelist.append(filelist_anat)
    filelist_flat = []
    print('FILELIST_FUNC:',filelist_func)
    print('FILELIST:',filelist)
    
    if len(filelist_func)!=0 and len(filelist_anat)!=0:
        for sublist in filelist:
            for item in sublist:
                filelist_flat.append(item)
                

    elif len(filelist_anat)==0:
        [filelist_flat.append(f) for f in filelist_func]

    elif len(filelist_func)==0:
        [filelist_flat.append(f) for f in filelist_anat]
    #print (filelist_flat)
    return filelist_flat
    
def replacement(filelist):
    replacements = []
    for f in filelist:
        target = os.path.basename(f)
        ses = f.split('/')[1]
        sub = f.split('/')[0]
        subses = sub + '_' + ses # create replacement bit
        replacement = target.replace(sub,subses)
        if str(ses) not in str(target): #only do this if modification hasn't already ccured i.e. no ses label in name
            replacements.append({f:os.path.join(os.path.dirname(f),replacement)})
        else:
            continue
    #print(replacements)    
    return replacements  

def replace(replacements):
    for pair in replacements:
        for target_path, replacement_path in pair.items():
            print('REPLACING',target_path,'WITH',replacement_path)    
            subprocess.call(['mv',target_path, replacement_path])
        print('')

# Loop through subdirs 
for sub in subdirs:
    # list sessions for this sub
    sessions = seslist(sub)    
    # for each session list all files that need to be modified 
    files = listfiles(seslist,sub)
    # for each file, create key:value target:replacement where 'sub-*' replaced with 'sub-*-ses-*'  
    replacements = replacement(files)
    # mv 
    replace(replacements)
