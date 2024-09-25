#!/usr/bin/python

'''
This script builds a naïve Bayesian classifier which is able to classify text fragments according
to their language.
'''

import argparse
import os
import math

# build unigram language models
def build_lang_model(lang_model_files):
    lang_index_dict = dict() # store language code and the total word count of its model
    unigram_models = dict() # store language code and its unigram model
    for file_name in sorted(lang_model_files):
        lang_code = file_name[-14:-11] # extract the three-letter language code
        lang_index_dict[lang_code] = None
        unigram_models[lang_code] = dict()
        # define and store unigram models
        with open(file_name, 'r', encoding='utf-8') as model_infile:
            total_word_count = 0
            for line in model_infile:
                cur_line = line.split()
                cur_word = cur_line[0]
                cur_word_count = int(cur_line[1])
                unigram_models[lang_code][cur_word] = cur_word_count
                total_word_count = total_word_count + cur_word_count
            lang_index_dict[lang_code] = total_word_count
    return lang_index_dict, unigram_models

if __name__ == '__main__':
    # take in 3 arguments of file paths
    parser = argparse.ArgumentParser()
    parser.add_argument('file_paths', nargs = 3)
    args = parser.parse_args()
    lang_model_path = args.file_paths[0]
    infile_path = args.file_paths[1]
    outfile_path = args.file_paths[2]
    lang_model_files = [os.path.join(lang_model_path, file) for file in os.listdir(lang_model_path)]
    
    lang_index_dict, unigram_models = build_lang_model(lang_model_files)

    with open(infile_path, 'r', encoding='utf-8') as infile, open(outfile_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            words = line.split('\t')[1].split()
            result_dict = dict() # 
            max_prob_value = (str(), float('-inf')) # initialize and keep track of the maximum value
            # calculate probabilities for each language
            for lang in unigram_models:
                sum = float()
                for w in words:
                    if w not in unigram_models[lang].keys():
                        w = '<UNK>'
                    p_w = math.log((unigram_models[lang][w] / lang_index_dict[lang]), 10) # formula
                    sum = sum + p_w
                result_dict[lang] = sum
                if sum > max_prob_value[1]:
                    max_prob_value = (lang, sum)
            outfile.write(line)
            for k,v in result_dict.items():
                outfile.write(k + '\t' + str(v) + '\n')
            outfile.write('result' + '\t' + str(max_prob_value[0]) + '\n')
            outfile.write('\n')