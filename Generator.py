# -*- coding: UTF-8 -*-

import sys
import os
import re
import argparse

import CourtList
import VerdictAnalyser
import FileOperations
import VerdictAnalyserv2

def get_sp_list(folder):
        file_list = os.listdir(folder)
        i, j = 0, 0
        for file in file_list:
            i += 1
            file_name = folder + '\\' + file
            if get_sp(file_name):
                j += 1
                print(j, file_name)

def get_sp(doc_name):
    if 'doc' in doc_name:
        content = FileOperations.MyDocFile(doc_name).read()
        if re.search('自诉人', content):
            return doc_name
        else:
            return None

def get_report(folder, year, trial):
    analyse_result = []
    file_list = os.listdir(folder)
    report_name = folder + "_report.csv"
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
    FileOperations.MyCsvFile(report_name).write_dict(CourtList.report_col_names, analyse_result)

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
    path_2_file = "C:\\Users\\lij37\\Cases\\2017\\Cases\\成都市双流区人民法院\\严德玉盗窃罪一审刑事判决书_d0bb7fdb-b936-4b4e-9cbe-a7380113c897.txt"
    verdict = VerdictAnalyserv2.VerdictAnalyser(path_2_file, '2017')
    print(verdict.dir_name)
    print(verdict.file_name)
    for key, value in verdict.analyse_doc().items():
        print("{:-<30} {}".format(key, value))
    return None
    base_dir = "C:\\Users\\lij37\\Cases"
    year = 2017
    my_cases_folder = FileOperations.MyFolder(base_dir + '\\'  + str(year) + '\\cases')
    check = True
    for region in my_cases_folder.get_file_list():
        my_region_folder = FileOperations.MyFolder(my_cases_folder.name + '\\' + region)
        print(my_region_folder.name)
        if "江油市人民法院" in my_region_folder.name:
            check = True
        if not check:
            continue
        for my_file in my_region_folder.get_file_list():
            path_2_file = my_region_folder.name + '\\' + my_file
            verdict = VerdictAnalyserv2.VerdictAnalyser(path_2_file, year)
            #print(verdict)
            #print(verdict.content)
            if verdict.analyse_doc():
                if verdict.defendent_section is None:
                    print("defendent section not found.")
                    print(verdict)
                    print(verdict.content)
                    return None
                if verdict.convict_section is None:
                    print("convict section not found.")
                    print(verdict)
                    print(verdict.content)
                    return None
                if verdict.head_section is None:
                    print("head section not found.")
                    print(verdict)
                    print(verdict.content)
                    return None
    return None

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
        get_sp_list(args.folder)
        #get_report(args.folder, args.year, trial)
    else:
        print(sys.argv[0] + desc)

if __name__ == "__main__":
    main()
