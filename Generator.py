# -*- coding: UTF-8 -*-
# import re
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

def dump2csv(results, folder_name):
    file = folder_name + '_report.csv'
    print('dump 2 file %s' % file)
    fieldnames = ['file_name', \
                  'verdict', \
                  'id', \
                  'court', \
                  'region',\
                  'court_level',\
                  'prosecutor', \
                  'procedure', \
                  'year', \
                  'd_name', \
                  'd_age', \
                  'd_sex', \
                  'd_nation', \
                  'd_education', \
                  'd_job', \
                  'd_lawyer', \
                  'd_lawyer_n',\
                  'd_s_lawyer', \
                  'd_s_lawyer_n',\
                  'd_charge', \
                  'd_charge_c']
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
    parser.add_argument('-m', '--move', action='store')
    args = parser.parse_args()

    if args.file:
        verdict = VerdictAnalyser.VerdictAnalyser(args.file)
        print(verdict.analyse_doc())
        #print(verdict.content)
    elif args.folder:
        analyse_result = []
        file_list = os.listdir(args.folder)
        i = 0
        for file in file_list:
            print('')
            print(file)
            i += 1
            print(i)
            
            verdict = VerdictAnalyser.VerdictAnalyser(args.folder + '\\' + file)
            analyse_result.extend(verdict.analyse_doc())
            #verdict.analyse_doc()
            #try:
            #    analyse_result.extend(verdict.analyse_doc())
            #except:
            #    print("Failed to analyse %s" % (args.folder + '\\' + file))
                #move(args.folder + '\\' + file, args.folder + '\\..\\EXCEPT\\' + file)
            
        #print(analyse_result)
        dump2csv(analyse_result, args.folder)
    elif args.move:
        folder_list = os.listdir(args.move)
        for folder in folder_list:
            file_list = os.listdir(args.move + '\\' + folder)
            for file in file_list:
                move(args.move + '\\' + folder + '\\' + file, args.move + '\\NEW\\' + file)
                print(file)
    else:
        print(sys.argv[0] + desc)

if __name__ == "__main__":
    main()
