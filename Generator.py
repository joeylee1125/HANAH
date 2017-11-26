# -*- coding: UTF-8 -*-
# import re
import sys
import os
# import time
import csv
import argparse
# import codecs

# from shutil import copyfile
# from docx import Document

import VerdictAnalyser
# import CourtList

def dump2csv(results):
    file = 'report.csv'
    print('dump 2 file %s' % file)
    fieldnames = ['file_name', 'verdict', 'id', 'court', 'prosecutor', 'year', 'd_name', 'd_age', 'd_sex', 'd_nation', 'd_education', 'd_job', 'd_lawyer', 'd_charge']
    with open(file, 'w', newline='', encoding='utf-8_sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)
        
def main():    
    desc = " [ -F|--folder folder ] [ -f|--file file]."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-F', '--folder', action='store')
    parser.add_argument('-f', '--file', action='store')
    args = parser.parse_args()

    if args.file:
        verdict = VerdictAnalyser.VerdictAnalyser(args.file)
        verdict.analyse_doc()
        #print(verdict.content)
    elif args.folder:
        analyse_result = []
        file_list = os.listdir(args.folder)
        for file in file_list:
            print('')
            print(file)
            verdict = VerdictAnalyser.VerdictAnalyser(args.folder + '\\' + file)
            analyse_result.extend(verdict.analyse_doc())
        #print(analyse_result)
        dump2csv(analyse_result)
    else:
        print(sys.argv[0] + desc)

if __name__ == "__main__":
    main()
