#!/usr/bin/env python3

import os
import re
import subprocess
import shutil


def generate_fragments(input_pdb, data_path):
    '''Generate fragments and save the fragments into the data_path.
    Return the job id.
    '''
    output_path = os.path.join(data_path, 'fragments')
   
    proc = subprocess.Popen(['klab_generate_fragments',
                           '-m', '100',
                           '-x', '10',
                           '-r', '48',
                           '-d', output_path,
                           input_pdb],
                           stdout=subprocess.PIPE)
   
    m = re.match(r"Fragment generation jobs started with job ID (\d+).", proc.stdout)

    return m.group(1) 
   
def submit_forward_folding_jobs(input_pdb, data_path, frag_job_id, num_jobs, nstruct_per_job):
    '''Submit the forward folding jobs'''
    
    # Gather the input files

    input_dir = os.path.join(data_path, 'inputs')
    frag_data_dir = os.path.join(data_path, 'fragments', 'inpuA')

    for f in ['inpuA.200.3mers.gz', 'inpuA.200.9mers.gz', 'inpuA.fasta', 'inpuA.psipred_ss2']:
        shutil.copy(os.path.join(frag_data_dir, f), input_dir)

    cmd = ['qsub',
           '-e', os.path.join(data_path, 'job_outputs'),
           '-o', os.path.join(data_path, 'job_outputs'),
           '-t', '1-{0}'.format(num_jobs),
           '-h', frag_job_id,
           './forward_folding.py',
           os.path.join(input_dir, 'inpuA.fasta'),
           os.path.join(input_dir, 'inpuA.200.3mers.gz'),
           os.path.join(input_dir, 'inpuA.200.9mers.gz'),
           os.path.join(input_dir, 'input.pdb'),
           os.path.join(input_dir, 'inpuA.psipred_ss2'),
           os.path.join(data_path, 'outputs'),
           str(nstruct_per_job)]

    subprocess.check_call(cmd)


def forward_folding(input_pdb, data_path, num_jobs, nstruct_per_job):
    '''Generate fragments and do forward folding.'''
    os.makedirs(os.path.join(data_path, 'inputs'), exist_ok=True)
    os.makedirs(os.path.join(data_path, 'outputs'), exist_ok=True)
    os.makedirs(os.path.join(data_path, 'job_outputs'), exist_ok=True)
  
    # Make a local copy of the input pdb

    local_input_pdb = os.path.join(data_path, 'inputs', 'input.pdb')
    
    if not os.path.samefile(input_pdb, local_input_pdb):
        shutil.copy(input_pdb, local_input_pdb)

    # Generate fragments

    frag_job_id = generate_fragments(input_pdb, data_path)

    # Run forward folding

    submit_forward_folding_jobs(input_pdb, data_path, frag_job_id, num_jobs, nstruct_per_job)


if __name__ == '__main__':
    pass
