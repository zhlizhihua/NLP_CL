#!/usr/bin/python

'''
This script takes in a corpus in SGML format.
Cleans the text, then counts and outputs the word frequency. 
'''

import os
import argparse
import re

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
    corpus = path_finder()
    word_dict = dict()
    for file in corpus:
        with open(file, encoding='utf8') as input_file:
            for line in input_file:
                line = re.sub('<.*?>', ' ', line) # filter out <...> tags, non-greedy
                line_parser = line.split()
                for word in line_parser:
                    if not re.search("[^a-zA-Z']", word): # filter out word with unwanted char
                        if not word.startswith("'") and not word.endswith("'"):
                            word = word.lower()
                            # store word with frequency counts
                            if word not in word_dict:
                                word_dict[word] = 1
                            else:
                                word_dict[word] += 1
    
    # use list of tuples to store b/c Condor does not support ordered Dictionary
    sorted_word_lst = list()
    # sort first by frequency value, then by alphabetic order using Dictionary
    for k, v in sorted(word_dict.items(), key=lambda item: (-item[1], item[0])):
        sorted_word_lst.append((k,v))
    
    for i in sorted_word_lst:
        print(i[0] + '\t' + str(i[1]))