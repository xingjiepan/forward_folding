#!/usr/bin/env python3
'''Extract the lowest energy model for a forward folding result.
Usage:
    ./extract_lowest_energy_model.py data_path1 [data_path2 ...]
'''

import os
import sys
import subprocess

import numpy as np


def get_data_tuples_for_a_data_set(data_path):
    '''Return a list of data tuples for a data set.'''
    scratch_path = os.path.join(data_path, 'outputs', 'scratches')
    
    data = []

    for sd in os.listdir(scratch_path):
        score_file = os.path.join(scratch_path, sd, 'score.fsc')
        data += get_data_tuples_for_a_score_file(sd, score_file)

    return data

def get_data_tuples_for_a_score_file(score_file_id, score_file_path):
    '''Return a list of data tuples for a score file.'''
    if not os.path.exists(score_file_path):
        return []
    
    data = []

    with open(score_file_path, 'r') as f:
        for i, line in enumerate(f.readlines()):
            if i == 0: continue
            sl = line.split()
            
            description = sl[31]
            rms = float(sl[26])
            score = float(sl[1])

            data.append((score_file_id, description, score, rms))

    return data

def extract_lowest_energy_model(data_path):
    '''Extract the lowest energy model'''
    extract_pdb_app = 'extract_pdbs.linuxgccrelease' # The application to extract pdbs from a silent file
  
    # Get the ID of the lowest scoring model

    data = get_data_tuples_for_a_data_set(data_path)
    lowest_energy_model_tuple = min(data, key=lambda x : x[2])
    print('The lowest energy model for {0} is {1}'.format(data_path, lowest_energy_model_tuple))
    lowest_rms_model_tuple = min(data, key=lambda x : x[3])
    print('The lowest RMSD model for {0} is {1}'.format(data_path, lowest_rms_model_tuple))

    # Extract the lowest scoring model

    cwd = os.getcwd()
    os.chdir(data_path)

    subprocess.call([extract_pdb_app, '-in:file:silent', 
        os.path.join('outputs', 'scratches', lowest_rms_model_tuple[0], 'default.out')])

    subprocess.call([extract_pdb_app, '-in:file:silent', 
        os.path.join('outputs', 'scratches', lowest_energy_model_tuple[0], 'default.out')])

    for f in os.listdir('.'):   
        if not f.endswith('.pdb'):
            continue

        if f.startswith(lowest_rms_model_tuple[1]):
            os.rename(f, 'lowest_rmsd_model.pdb')

        elif f.startswith(lowest_energy_model_tuple[1]):
            os.rename(f, 'lowest_energy_model.pdb')

        elif f.startswith('S_00'):
            os.remove(f)

        elif f.startswith('F_00'):
            os.remove(f)

    os.chdir(cwd)

def extract_lowest_energy_model_for_multiple_data_sets(data_paths):
    '''Extract the lowest energy models for multiple data sets'''
    for data_path in data_paths:
        extract_lowest_energy_model(data_path)

if __name__ == '__main__':
    data_paths = sys.argv[1:]

    extract_lowest_energy_model_for_multiple_data_sets(data_paths) 
