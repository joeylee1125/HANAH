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

def dump2csv(results, folder_name):
    file = folder_name + 'report.csv'
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
                  'd_has_lawyer',\
                  'd_charge', \
                  'd_charge_c',\
                  'd_prison',\
                  'd_prison_l',\
                  'd_probation',\
                  'd_probation_l',\
                  'd_fine']
    with open(file, 'w', newline='', encoding='utf-8_sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

def get_report(folder, year, trial):
    analyse_result = []
    file_list = os.listdir(folder)
    i = 0
    for file in file_list:
        print('{} Begin to analyse...    {}'.format(i, file))
        i += 1
        file_name = folder + file
        if trial == '2':
            verdict = VerdictAnalyser.VerdictAnalyser2(file_name, year)
        else:
            verdict = VerdictAnalyser.VerdictAnalyser(file_name, year)
        results = verdict.analyse_doc()
        if results is not None:
            analyse_result.extend(results)
    dump2csv(analyse_result, folder)

            
def main():    
    desc = " [ -F|--folder folder ] [ -f|--file file]."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-F', '--folder', action='store')
    parser.add_argument('-f', '--file', action='store')
    parser.add_argument('-m', '--move', action='store')
    parser.add_argument('-y', '--year', action='store')
    parser.add_argument('-t', '--trial', action='store')
    
    args = parser.parse_args()
    
    # This is for debug only
    #file_path = "C:\\Users\\lij37\\Code\\RAW_Han2016\\NEW\\"
    #file_path = "C:\\Users\\lij37\\Cases\\2016\\案件\\"
    file_path = "C:\\ttt\\"
    
    if args.file:
        file_name = file_path + args.file
        if args.trial == '2':
            verdict = VerdictAnalyser.VerdictAnalyser2(file_name, args.year)
        else:
            verdict = VerdictAnalyser.VerdictAnalyser(file_name, args.year)
        results = verdict.analyse_doc()
        if results:
            for i in verdict.analyse_doc():
                for k, v in i.items():
                    print('%s ----> %s' % (k, v))
                print('')
        #print(verdict.content)
    elif args.folder:
        get_report(file_path, args.year, args.trial)
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

    
    
        #verdict.analyse_doc()
        #if re.search('附带民事', file):
        #    print(file)
        #    move(args.folder + '\\' + file, args.folder + '\\..\\附带民事\\' + file)
        
        
        #verdict.analyse_doc()
        #try:
        #    analyse_result.extend(verdict.analyse_doc())
        #except:
        #    print("Failed to analyse %s" % (args.folder + '\\' + file))
        #    move(args.folder + '\\' + file, args.folder + '\\..\\EXCEPT1\\' + file)    