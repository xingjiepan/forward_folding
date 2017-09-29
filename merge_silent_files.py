#!/usr/bin/env python
'''Merge all silent files in one directory into one single silent file. Run as
    ./merge_silent_files.py input_path output_file_name
'''

import os
import sys
import shutil


if __name__ == '__main__':

    input_path = sys.argv[1]
    output_file_name = sys.argv[2]

    input_files = [os.path.join(input_path, f) in os.listdir(input_path)]

    # Copy the fisrt silent file to the destinition file

    shutil.copyfile(input_files[0], output_file_name)

    # Append the rest of files to the output file

    with open(output_file_name, 'a') as fout:
        for i in range(1, len(input_files)):
            with open(input_files[i], 'r') as fin:

                for line in fin.readlines()[2:]:
                    fout.write(line + '\n')
