#!/usr/bin/env python3
'''Print the RMSDs of the lowest energy models for forward folding results.
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

def print_lowest_energy_model_rmsd(data_path):
    '''Print the RMSD of the lowest energy model'''
  
    data = get_data_tuples_for_a_data_set(data_path)
    lowest_energy_model_tuple = min(data, key=lambda x : x[2])
    print('The lowest energy model from {0} predictions for {1} is {2}'.format(len(data), data_path, lowest_energy_model_tuple))
    lowest_rms_model_tuple = min(data, key=lambda x : x[3])
    print('The lowest RMSD model from {0} predictions for {1} is {2}'.format(len(data), data_path, lowest_rms_model_tuple))

def print_lowest_energy_model_rmsd_for_multiple_data_sets(data_paths):
    '''Print the RMSDs of lowest energy models for multiple data sets'''
    for data_path in data_paths:
        print_lowest_energy_model_rmsd(data_path)

if __name__ == '__main__':
    data_paths = sys.argv[1:]

    print_lowest_energy_model_rmsd_for_multiple_data_sets(data_paths) 
