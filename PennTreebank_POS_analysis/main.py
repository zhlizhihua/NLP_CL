#!/usr/bin/python

'''
This script takes in an annotated corpus of Penn Treebank, 
counts and outputs the number of syntactic constituent types.
'''

import os
import argparse

# takes the absolute path of the directory (corpus)
# return a list of absolute paths of every file in the directory
def path_finder():
    parser = argparse.ArgumentParser()
    parser.add_argument('corpusname') 
    args = parser.parse_args()
    corpus_path = args.corpusname
    files = [os.path.join(corpus_path, file) for file in os.listdir(corpus_path)]
    return files

if __name__ == '__main__':
    all_files = path_finder()

    s_count = 0
    np_count = 0
    vp_count = 0
    di_vp_count = 0
    in_vp_count = 0

    for f_path in all_files:
        with open(f_path, 'r') as infile:
            # read entire file as a string, check substring counts for S, NP, VP
            text_file = infile.read()
            s_count += text_file.count('(S ')
            np_count += text_file.count('(NP ')
            vp_count += text_file.count('(VP ')

            # check counts for ditransitive and intransitive VP
            text_lst = text_file.split('\n')
            for i in range(0, len(text_lst)):
                cur_line = text_lst[i].strip() # strip leading space to check immediate children
                if cur_line.startswith('(VP '):
                    next_line = text_lst[i+1].strip()
                    if next_line.startswith('(NP '):
                        next_next_line = text_lst[i+2].strip()
                        if next_next_line.startswith('(NP '):
                            di_vp_count += 1
                    else:
                        in_vp_count += 1

    result = {'Sentence': s_count, 'Noun Phrase': np_count, 'Verb Phrase': vp_count, 
              'Ditransitive Verb Phrase': di_vp_count, 'Intransitive Verb Phrase': in_vp_count}

    for k, v in result.items():
        print(k + '\t' + str(v))
