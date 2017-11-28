#!/usr/bin/env python3

import os
import re
import subprocess
import shutil


def generate_fragments(input_pdb, data_path):
    '''Generate fragments and save the fragments into the data_path.
    Return the job id.
    '''
    cwd = os.getcwd()
    os.chdir(data_path)
    
    output_path = 'fragments'
    if os.path.exists('fragments'):
      shutil.rmtree(output_path)

    proc = subprocess.Popen(['klab_generate_fragments',
                           '-m', '100',
                           '-x', '10',
                           '-r', '48',
                           '-d', output_path,
                           input_pdb],
                           stdout=subprocess.PIPE)
   
    if proc.stdout:
      stdout = proc.stdout.read().decode()
      print(stdout)
    if proc.stderr:
      print(proc.stderr.read().decode())    
    
    for line in stdout.split('\n'): 
        m = re.match(r"Fragment generation jobs started with job ID (\d+).", line)
        if m:
          break

    os.chdir(cwd)

    return m.group(1) 
   
def submit_forward_folding_jobs(input_pdb, data_path, frag_job_id, num_jobs, nstruct_per_job):
    '''Submit the forward folding jobs'''
    
    # Gather the input files

    input_dir = os.path.join(data_path, 'inputs')
    frag_data_dir = os.path.join(data_path, 'fragments', 'inpuA')

    for f in ['inpuA.200.3mers.gz', 'inpuA.200.9mers.gz', 'inpuA.fasta', 'inpuA.psipred_ss2']:
        if os.path.exists(os.path.join(input_dir, f)):
            os.remove(os.path.join(input_dir, f))
        os.symlink(os.path.abspath(os.path.join(frag_data_dir, f)), os.path.join(input_dir, f))

    cmd = ['qsub',
           '-e', os.path.join(data_path, 'job_outputs'),
           '-o', os.path.join(data_path, 'job_outputs'),
           '-t', '1-{0}'.format(num_jobs),
           '-hold_jid', frag_job_id,
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

    input_pdb = os.path.abspath(input_pdb)
    local_input_pdb = os.path.abspath(os.path.join(data_path, 'inputs', 'input.pdb'))
    
    if os.path.normpath(input_pdb) != os.path.normpath(local_input_pdb):
        shutil.copy(input_pdb, local_input_pdb)

    # Generate fragments

    frag_job_id = generate_fragments(local_input_pdb, data_path)

    # Run forward folding

    submit_forward_folding_jobs(local_input_pdb, data_path, frag_job_id, num_jobs, nstruct_per_job)


if __name__ == '__main__':
  
  for i in [788, 549, 631, 915, 231]:
      forward_folding('/netapp/home/xingjiepan/Softwares/precise_backbone_design/data/design_antiparallel_3_8_helix_20_100_4genBB/{0}/design.pdb'.format(i),
          'data/design_antiparallel_3_8_helix_20_100_4genBB_{0}'.format(i), 2000, 10)

  for i in [837, 991, 358, 842, 627]:
      forward_folding('/netapp/home/xingjiepan/Softwares/precise_backbone_design/data/design_antiparallel_3_8_helix_20_120_4genBB/{0}/design.pdb'.format(i),
          'data/design_antiparallel_3_8_helix_20_120_4genBB_{0}'.format(i), 2000, 10)

  for i in [185, 298, 24, 939, 286]:
      forward_folding('/netapp/home/xingjiepan/Softwares/precise_backbone_design/data/design_antiparallel_3_8_helix_20_140_4genBB/{0}/design.pdb'.format(i),
          'data/design_antiparallel_3_8_helix_20_140_4genBB_{0}'.format(i), 2000, 10)


