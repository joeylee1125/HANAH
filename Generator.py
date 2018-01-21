# -*- coding: UTF-8 -*-

import sys
import os
import re
import argparse

import StaticUtils
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

def get_report(case_folder, base_folder, year):
    analyse_result = list()
    case_folder = FileOperations.MyFolder(case_folder)
    case_list = case_folder.get_file_list()
    report_path = base_folder + '\\' + str(year) + '\\reports'
    report_name = report_path + '\\' + os.path.basename(case_folder.name) + ".csv"
    i = 0
    for case in case_list:
        print('{} Begin to analyse...    {}'.format(i, case))
        i += 1
        verdict = VerdictAnalyserv2.VerdictAnalyser(case_folder.name + '\\' + case, year)
        results = verdict.analyse_doc()
        if results is not None:
            analyse_result.extend(results)
    FileOperations.MyCsvFile(report_name).write_dict(StaticUtils.report_col_names, analyse_result)

def get_report_single(path_2_file, year):
    verdict = VerdictAnalyserv2.VerdictAnalyser(path_2_file, year)
    print(verdict.content)
    results = verdict.analyse_doc()
    if results:
        for i in verdict.analyse_doc():
            for k, v in i.items():
                print('%s ----> %s' % (k, v))
            print('')

def main():
    path_2_file = "C:\\Users\\lij37\\Cases\\2017\\cases\\宜宾市翠屏区人民法院\\被告人肖玲、唐国强贩卖毒品罪一审刑事判决书_bc79bc85-3115-41a6-ad48-a86a00bafbe4.txt"
    base_dir = "C:\\Users\\lij37\\Cases"
    year = 2017
    #get_report_single(path_2_file, year)
    #return None
    my_cases_folder = FileOperations.MyFolder(base_dir + '\\'  + str(year) + '\\cases')
    check = False
    for region in my_cases_folder.get_file_list():
        if "宜宾市翠屏区人民法院" in region:
            check = True
        if not check:
            continue
        my_region_folder = FileOperations.MyFolder(my_cases_folder.name + '\\' + region)
        print(my_region_folder.name)
        get_report(my_region_folder.name, base_dir, year)
    return None

#        if "江油市人民法院" in my_region_folder.name:
#            check = True
#        if not check:
#            continue
#        for my_file in my_region_folder.get_file_list():
#            path_2_file = my_region_folder.name + '\\' + my_file
#            get_report_single(path_2_file, year)
#    return None

#    desc = " [ -F|--folder folder ] [ -f|--file file]."
#    parser = argparse.ArgumentParser(description=desc)
#    parser.add_argument('-F', '--folder', action='store')
#    parser.add_argument('-f', '--file', action='store')
#    parser.add_argument('-y', '--year', action='store')
#    parser.add_argument('-t', '--trial', action='store')
#
#    args = parser.parse_args()
#    trial = 2 if args.trial == 2 else 1
#
#    if args.file:
#        get_report_single(args.folder + '\\' + args.file, args.year, trial)
#    elif args.folder:
#        get_sp_list(args.folder)
#        #get_report(args.folder, args.year, trial)
#    else:
#        print(sys.argv[0] + desc)

if __name__ == "__main__":
    main()
