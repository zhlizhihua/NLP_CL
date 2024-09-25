#!/usr/bin/python

'''
This script implements a finite state automaton (FSA) that identifies syllables in Thai text.
'''

import argparse

# define fsa with states and corresponded actions
# each action contains character category + next state
def define_fsa():
    fsa = {0: [('V1', 1), ('C1', 2)],
           1: [('C1', 2)],
           2: [('C2', 3), ('V2', 4), ('T', 5), ('V3', 6), ('C3', 9), ('V1', 7), ('C1', 8)],
           3: [('V2', 4), ('T', 5), ('V3', 6), ('C3', 9)],
           4: [('T', 5), ('V3', 6), ('C3', 9), ('V1', 7), ('C1', 8)],
           5: [('V3', 6), ('C3', 9), ('V1', 7), ('C1', 8)],
           6: [('C3', 9), ('V1', 7), ('C1', 8)],
           7: 1,
           8: 2,
           9: 0}
    return fsa

# map the category to a list of its members
def make_cat_dict(file):
    with open(file, 'r', encoding='utf-8') as f:
        cat2chars = dict()
        for line in f:
            cur_line = line.split()
            cur_key = cur_line.pop(0)
            cat2chars[cur_key] = cur_line
    return cat2chars

if __name__ == '__main__':
    # accepts three arguments that are paths of the files
    parser = argparse.ArgumentParser()
    parser.add_argument('file_paths', nargs=3)
    args = parser.parse_args()
    cat_file = args.file_paths[0]
    input_file = args.file_paths[1]
    out_file_name = args.file_paths[2]

    cat2chars = make_cat_dict(cat_file)
    fsa = define_fsa()

    # segment one line each time
    with open(input_file, 'r', encoding='utf-8') as infile, open(out_file_name, 'w', encoding='utf-8') as outfile:
        for line in infile:
            segmented = ''
            current_state = 0
            for char in line:
                for (category, next_state) in fsa[current_state]:
                    if char in cat2chars[category]:
                        current_state = next_state
                        break

                if current_state == 7 or current_state == 8:
                    segmented = segmented + ' ' + char
                    current_state = fsa[current_state]
                elif current_state == 9:
                    segmented = segmented + char + ' '
                    current_state = fsa[current_state]
                else:
                    segmented = segmented + char

            outfile.write(segmented.strip()+'\n')