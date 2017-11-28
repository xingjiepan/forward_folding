#!/usr/bin/python3
#$ -S /usr/bin/python3             #-- the shell for the job                                                                                                          
#$ -cwd                            #-- tell the job that it should start in your working directory
#$ -r y                            #-- tell the system that if a job crashes, it should be restarted
#$ -l mem_free=3G                  #-- submits on nodes with enough free memory (required)
#$ -l arch=linux-x64               #-- SGE resources (CPU type)
#$ -l netapp=1G,scratch=1G         #-- SGE resources (home and scratch disks)
#$ -l h_rt=1:00:00                 #-- runtime limit 
''' Copy this script to forward_folding.py, configure the 
    paramters and run:
        ./forward_folding.py flags fasta frag3 frag9 native_pdb psipred_ss2_file data_output_path nstruct 
'''

import sys
import os
import subprocess
import shutil


def forward_folding(ab_initio_app, extract_pdb_app, flags, fasta, frag3, frag9, native, psipred_ss2, data_output_path, nstruct):
    '''Run Rosetta forward_folding'''
    task_id = os.environ['SGE_TASK_ID']

    pdb_path = os.path.abspath(os.path.join(data_output_path, 'pdbs'))
    scratch_path = os.path.join(data_output_path, 'scratches')
    my_scratch_path = os.path.join(scratch_path, task_id)

    for p in [pdb_path, scratch_path, my_scratch_path]:
        try:
            if not os.path.exists(p):
                os.mkdir(p)
        except:
            continue

    # Run ab initio

    rosetta_command = [ab_initio_app,
                       '@' + flags,
                       '-in:file:fasta', fasta,
                       '-in:file:frag3', frag3,
                       '-in:file:frag9', frag9,
                       '-in:file:native', native,
                       '-psipred_ss2', psipred_ss2,
                       '-nstruct', nstruct,
                       '-out:sf', os.path.join(my_scratch_path, 'score.fsc'),
                       '-out:file:silent', os.path.join(my_scratch_path, 'default.out'),
                       '-seed_offset', task_id] 

    subprocess.check_call(rosetta_command)

    # Extract pdbs

    os.chdir(my_scratch_path)

    extract_command = [extract_pdb_app,
                      '-in:file:silent', 'default.out']

    subprocess.check_call(extract_command)

    for f in os.listdir('.'):
        if f.endswith('.pdb'):
            subprocess.check_call(['gzip', f])
            shutil.move(f + '.gz', os.path.join(pdb_path, task_id + '_' + f + '.gz'))


if __name__ == '__main__':
    ab_initio_app = 'AbinitioRelax.linuxgccrelease' # The ab initio relax application
    extract_pdb_app = 'extract_pdbs.linuxgccrelease' # The application to extract pdbs from a silent file
    flags = 'flags/standard_flags' # flag file
    
    fasta = sys.argv[1] # input fasta sequence
    frag3 = sys.argv[2] # 3mers fragment set
    frag9 = sys.argv[3] # 9mers fragment set
    native = sys.argv[4] # native pdb
    psipred_ss2 = sys.argv[5] # secondary structure predictions by PsiPred
    
    data_output_path = sys.argv[6] # path to output the data
    nstruct = sys.argv[7] # number of structures to generate for each job

    
    forward_folding(ab_initio_app, extract_pdb_app, flags, fasta, frag3, frag9, native, psipred_ss2, data_output_path, nstruct)
