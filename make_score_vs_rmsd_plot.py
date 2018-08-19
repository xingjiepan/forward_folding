#!/usr/bin/env python3
'''Make score vs RMSD plot for a forward folding result.
Usage:
    ./make_score_vs_rmsd_plot.py data_path
'''

import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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

def make_score_vs_rmsd_plot_for_a_data_set(data_path):
    '''Make a score vs rmsd plot for a data set.'''
    data = get_data_tuples_for_a_data_set(data_path)

    X = [t[3] for t in data]
    Y = [t[2] for t in data]

    x_90 = np.percentile(X, 90)
    y_90 = np.percentile(Y, 90)

    plt.scatter(X, Y, s=2)
    
    x_min, x_max, y_min, y_max = plt.axis()
    plt.axis([0, x_90, min(Y) - 3, y_90])

    plt.show()


if __name__ == '__main__':
    data_path = sys.argv[1]

    make_score_vs_rmsd_plot_for_a_data_set(data_path)
