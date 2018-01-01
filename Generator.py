# -*- coding: UTF-8 -*-
import re
import sys
import os
# import time
import csv
import argparse
# import codecs

from shutil import move
# from shutil import copyfile
# from docx import Document

import VerdictAnalyser
# import CourtList


def get_report(folder, year, trial):
    analyse_result = []
    file_list = os.listdir(folder)
    i = 0
    for file in file_list:
        print('{} Begin to analyse...    {}'.format(i, file))
        i += 1
        file_name = folder + '\\' + file
        if trial == '2':
            verdict = VerdictAnalyser.VerdictAnalyser2(file_name, year)
        else:
            verdict = VerdictAnalyser.VerdictAnalyser(file_name, year)
        results = verdict.analyse_doc()
        if results is not None:
            analyse_result.extend(results)
    verdict.dump2csv(analyse_result, folder)


def get_report_single(path_2_file, year, trial):
    if trial == '2':
        verdict = VerdictAnalyser.VerdictAnalyser2(path_2_file, year)
    else:
        verdict = VerdictAnalyser.VerdictAnalyser(path_2_file, year)
    results = verdict.analyse_doc()
    if results:
        for i in verdict.analyse_doc():
            for k, v in i.items():
                print('%s ----> %s' % (k, v))
            print('')

def main():
    desc = " [ -F|--folder folder ] [ -f|--file file]."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-F', '--folder', action='store')
    parser.add_argument('-f', '--file', action='store')
    parser.add_argument('-y', '--year', action='store')
    parser.add_argument('-t', '--trial', action='store')
    
    args = parser.parse_args()
    trial = 2 if args.trial == 2 else 1

    if args.file:
        get_report_single(args.folder + '\\' + args.file, args.year, trial)
    elif args.folder:
        get_report(args.folder, args.year, trial)
    else:
        print(sys.argv[0] + desc)

if __name__ == "__main__":
    main()
