# -*- coding: UTF-8 -*-

import sys
import os
import re
import argparse

import StaticUtils
import VerdictAnalyser
import FileOperations
import VerdictAnalyserv2

BASE_DIR = "C:\\Users\\lij37\\Cases"
YEAR = 2017
CASE_DIR = BASE_DIR + '\\' + str(YEAR) + '\\Cases'

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


def get_report(case_folder):
    print("Generate report for {}".format(case_folder))
    analyse_result = list()
    path_2_folder = BASE_DIR + '\\' + str(YEAR) + '\\Cases\\' + case_folder
    my_folder = FileOperations.MyFolder(path_2_folder)
    case_list = my_folder.get_file_list()
    report_path = BASE_DIR + '\\' + str(YEAR) + '\\reports'
    report_name = report_path + '\\' + os.path.basename(my_folder.name) + ".csv"
    i = 0
    for case in case_list:
        #print('{} Begin to analyse...    {}'.format(i, case))
        i += 1
        verdict = VerdictAnalyserv2.VerdictAnalyser(my_folder.name + '\\' + case, YEAR)
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

def test_pre_charge(path_2_file):
    verdict = VerdictAnalyserv2.VerdictAnalyser(path_2_file, YEAR)
    if verdict.size < 100 or "附带民事" in verdict.content:
        return None
    #verdict.divide_2_mul_sections()
    #defendant_info_list = verdict.get_defendant_info_list()
    #convict_info_list = verdict.get_convict_info_list()
    print(verdict.content)
    print(verdict.get_pre_charge())
    #print(convict_info_list)

def test_convict_section(path_2_file):
    verdict = VerdictAnalyserv2.VerdictAnalyser(path_2_file, YEAR)
    if verdict.size < 100 or "附带民事" in verdict.content:
        return None
    verdict.divide_2_mul_sections()
    defendant_info_list = verdict.get_defendant_info_list()
    convict_info_list = verdict.get_convict_info_list()
    print(verdict.content)
    print(defendant_info_list)
    print(convict_info_list)
    print('---------------AFTER---------------------------')
    defendant_info_list, defendant_name_list = verdict.get_defendant_name_list(defendant_info_list)
    defendant_list = [dict() for x in range(len(defendant_info_list))]
    for index, defendant_info in enumerate(defendant_name_list):
        defendant_list[index]['name'] = defendant_name_list[index]
        bail = verdict.get_defendant_bail(defendant_info)
    convict_info_list = verdict.clean_defendant_charge(defendant_list, convict_info_list)
    print(defendant_name_list)
    print(convict_info_list)
    for i in range(len(defendant_list)):
        prison = verdict.get_defendant_prison(defendant_list[i]['name'], convict_info_list)
        charge = verdict.get_defendant_charge(defendant_list[i]['name'], convict_info_list)
        charge_class = verdict.get_charge_class(charge)
        prison_l = verdict.get_prison_len(prison)
        probation = verdict.get_defendant_probation(defendant_list[i]['name'], convict_info_list)
        probation_l = verdict.get_prison_len(probation)
        fine = verdict.get_defendant_fine(defendant_list[i]['name'], convict_info_list)
        print("{:-<20} {}".format("Prison", prison))
        print("{:-<20} {}".format("Prison length", prison_l))
        print("{:-<20} {}".format("Charge", charge))
        print("{:-<20} {}".format("Charge class", charge_class))
        print("{:-<20} {}".format("Probation", probation))
        print("{:-<20} {}".format("Probation length", probation_l))
        print("{:-<20} {}".format("Fine", fine))
        print("{:-<20} {}".format("Bail", bail))
    print("")




def read(path_2_file):
    verdict = VerdictAnalyserv2.VerdictAnalyser(path_2_file, YEAR)
    print(verdict.content)

def run_a_file(func, path_2_file):
    func(path_2_file)

def run_a_folder(func, folder):
    my_folder = FileOperations.MyFolder(CASE_DIR + '\\' + folder)
    for case in my_folder.get_file_list():
        func(my_folder.name + '\\' + case)

def run_all_folder(func, starter=None):
    if starter:
        skip = True
    else:
        skip = False
    my_cases_folder = FileOperations.MyFolder(BASE_DIR + '\\' + str(YEAR) + '\\cases')
    for region in my_cases_folder.get_file_list():
        if starter == region:
            skip = False
        if skip:
            continue
        my_region_folder = FileOperations.MyFolder(my_cases_folder.name + '\\' + region)
        #run_a_folder(func, my_region_folder.get_basename())
        func(region)

def main():
    folder = '成都高新技术产业开发区人民法院'
    path_2_file = "C:\\Users\\lij37\\Cases\\2017\\cases\\都江堰市人民法院\\马某冒充军人招摇撞骗罪一审刑事判决书_7742721d-3d4f-4195-ba6d-a76f00c1854f.txt"
    #f = test_convict_section
    #f = read
    #f = test_pre_charge
    f = get_report
    #run_a_file(f, path_2_file)
    #run_a_folder(f, folder)
    run_all_folder(f,"岳池县人民法院")
    #get_report(folder)
    return None




    base_dir = "C:\\Users\\lij37\\Cases"
    year = 2017
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
        if "荥经县人民法院" in region:
            check = True
        if not check:
            continue
        my_region_folder = FileOperations.MyFolder(my_cases_folder.name + '\\' + region)
        print(i, my_region_folder.name)

        #j = j + get_invalid(my_region_folder.name, year)
        #print(j)
        #get_report(my_region_folder.name, base_dir, year)

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
