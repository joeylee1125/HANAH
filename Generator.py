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

def get_invalid(case_folder, year):
    case_folder = FileOperations.MyFolder(case_folder)
    case_list = case_folder.get_file_list()
    i = 0
    for case in case_list:
        #print('{} Begin to analyse...    {}'.format(i, case))
        #i += 1
        verdict = VerdictAnalyserv2.VerdictAnalyser(case_folder.name + '\\' + case, year)
        #print(verdict.dir_name + '\\' + verdict.file_name)
        if verdict.size < 100 or "附带民事" in verdict.content:
            i += 1
    return i

def get_defendant(case_folder, year):
    case_folder = FileOperations.MyFolder(case_folder)
    case_list = case_folder.get_file_list()
    for case in case_list:
        #print('{} Begin to analyse...    {}'.format(i, case))
        #i += 1
        verdict = VerdictAnalyserv2.VerdictAnalyser(case_folder.name + '\\' + case, year)
        #print(verdict.dir_name + '\\' + verdict.file_name)
        if verdict.size < 100 or "附带民事" in verdict.content:
            continue
        verdict.divide_2_mul_sections()
        defendant_info_list = verdict.get_defendant_info_list()
        info_list, name_list = verdict.get_defendant_name_list(defendant_info_list)


        if not name_list:
            print(verdict.dir_name + '\\' + verdict.file_name)
            print(verdict.content)
            print(defendant_info_list)
            return None
        else:
            if len(info_list) != len(name_list):
                print(verdict.dir_name + '\\' + verdict.file_name)
                print(len(info_list), len(name_list))
                print(info_list, name_list)
                return None
        #defendant_info_list = verdict.clean_defendant_info_list_v2(defendant_info_list)

        #for index, defendant in enumerate(defendant_info_list):
        #    if not verdict.get_defendant_name(defendant):
        #        print(verdict.file_name)
        #        print(defendant_info_list)
        #        return None
    return True


def get_report(case_folder, base_folder, year):
    analyse_result = list()
    case_folder = FileOperations.MyFolder(case_folder)
    case_list = case_folder.get_file_list()
    report_path = base_folder + '\\' + str(year) + '\\reports'
    report_name = report_path + '\\' + os.path.basename(case_folder.name) + ".csv"
    i = 0
    for case in case_list:
        #print('{} Begin to analyse...    {}'.format(i, case))
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
        for i in results:
            for k, v in i.items():
                print('%s ----> %s' % (k, v))
            print('')

def get_defendant_single(path_2_file, year):
    verdict = VerdictAnalyserv2.VerdictAnalyser(path_2_file, year)
    verdict.divide_2_mul_sections()
    defendant_info_list = verdict.get_defendant_info_list()
    info_list, name_list = verdict.get_defendant_name_list(defendant_info_list)
    print(len(info_list), info_list)
    print(len(name_list), name_list)

def test_prison(path_2_file, year):
    verdict = VerdictAnalyserv2.VerdictAnalyser(path_2_file, year)
    verdict.divide_2_mul_sections()
    defendant_info_list = verdict.get_defendant_info_list()
    convict_info_list = verdict.get_convict_info_list()
    print(convict_info_list)
    defendant_info_list, defendant_name_list = verdict.get_defendant_name_list(defendant_info_list)
    defendant_list = [dict() for x in range(len(defendant_info_list))]
    for index in range(len(defendant_name_list)):
        defendant_list[index]['name'] = defendant_name_list[index]
    convict_info_list = verdict.clean_defendant_charge(defendant_list, convict_info_list)
    for i in range(len(defendant_list)):
        print(defendant_list[i]['name'])
        print(convict_info_list)
        p = verdict.get_defendant_prison(defendant_list[i]['name'], convict_info_list)
        c = verdict.get_defendant_charge(defendant_list[i]['name'], convict_info_list)
        print(c)
        print(p)

def main():
    path_2_file = "C:\\Users\\lij37\\Cases\\2017\\cases\\长宁县人民法院\\王兴强犯非法持有枪支罪一审刑事判决书_01f14be5-5244-4dd5-83f0-a81900ab8ce9.txt"
    base_dir = "C:\\Users\\lij37\\Cases"
    year = 2014
    i = 0
    #test_prison(path_2_file, year)
    #get_defendant_single(path_2_file, year)
    #get_report_single(path_2_file, year)
    #return None
    my_cases_folder = FileOperations.MyFolder(base_dir + '\\'  + str(year) + '\\cases')
    check = False
    j = 0
    for region in my_cases_folder.get_file_list():
        i += 1
        print(i)
        if "荥经县人民法院" in region:
            check = True
        if not check:
            continue
        my_region_folder = FileOperations.MyFolder(my_cases_folder.name + '\\' + region)
        print(my_region_folder.name)

        #j = j + get_invalid(my_region_folder.name, year)
        #print(j)
        get_report(my_region_folder.name, base_dir, year)

        #return None
        #if get_defendant(my_region_folder.name, year):
        #   continue
        #else:
        #    return None
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
