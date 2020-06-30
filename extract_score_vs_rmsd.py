#!/usr/bin/env python3
'''Extract the scores and rmsds of forward folding results.
Usage:
    ./extract_score_vs_rmsd.py data_path1 [data_path2 ...]
'''

import os
import sys
import json


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

def extract_score_vs_rmsd(data_path):
    '''Extract the score vs rmsd data into a json file.'''
    relaxed_score_and_rmsd_file = os.path.join(data_path, 'scores_and_rmsds.json')

    data = get_data_tuples_for_a_data_set(data_path)
    forward_folding = [[d[2], d[3]] for d in data] 

    relaxed_designs = []
    if os.path.exists(relaxed_score_and_rmsd_file):
        with open(relaxed_score_and_rmsd_file, 'r') as f:
            relaxed_designs = json.load(f)
   
    with open(os.path.join(data_path, 'all_scores_vs_rmsds.json'), 'w') as f:
        json.dump( 
            {'forward_folding':forward_folding,
             'relaxed_designs':relaxed_designs},
            f)


if __name__ == '__main__':
    data_paths = sys.argv[1:]

    for data_path in data_paths:
        extract_score_vs_rmsd(data_path)
