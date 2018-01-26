# -*- coding: UTF-8 -*-
import argparse
import datetime
import json
import re
import time
import Spider
import CourtList
import FileOperations


def get_total_number(search_criteria):
    wenshu = Spider.WenShu()
    wenshu.set_search_criteria(search_criteria)
    return wenshu.get_total_item_number()


def get_court_list(mid_court_list):
    wenshu = Spider.WenShu()
    for mid_court in mid_court_list:
        wenshu.get_court_list(mid_court)

def download_caselist(search_criteria, index, csv_file):
    cases = dict()
    wenshu = Spider.WenShu()
    wenshu.set_search_criteria(search_criteria)
    cases = wenshu.get_case_list(index)
    csv_file.write(cases)
    print('dump {} items into {}'.format(len(cases['doc_id']), cases))
    print('Sleep 10s.....')
    time.sleep(2)

def download_all_caselist(search_criteria, max_page, csv_file):
    cases = dict()
    wenshu = Spider.WenShu()
    wenshu.set_search_criteria(search_criteria)
    for index in range(1, max_page + 1):
        tmp_case_list = wenshu.get_case_list(index)
        if not cases:
            cases = tmp_case_list
        else:
            for key, value in tmp_case_list.items():
                cases[key] += value
    csv_file.write(cases)
    print('dump {} items into {}'.format(len(cases['doc_id']), cases))
    print('Sleep 10s.....')
    time.sleep(2)

def download_caselists(search_criteria, case_folder):
    update = False
    cf = FileOperations.MyFolder(case_folder)
    if not cf.get_file_list():
        total_number = get_total_number(search_criteria)
        txt_file = FileOperations.MyTextFile(case_folder + '\\total_number_' + str(total_number))
        txt_file.create()
    else:
        for file in cf.get_file_list():
            if 'total_number' in file:
                total_number = file[13:]
        if False:  #Check Update Here, Update later to receive inputs parameter.
            new_total_number = get_total_number(search_criteria)
            print("Total number is: {} \n New total number is: {} \n".format(total_number, new_total_number))
            if int(new_total_number) > int(total_number):
                txt_file = FileOperations.MyTextFile(case_folder + '\\total_number_' + str(total_number))
                txt_file.delete()
                new_txt_file = FileOperations.MyTextFile(case_folder + '\\total_number_' + str(new_total_number))
                new_txt_file.create()
                total_number = new_total_number
                update = True
            if int(total_number) == 0:
                print('-------------------------------------------------------->{}\n\n\n\n'.format(case_folder))
    max_page = int(total_number) // 20 if int(total_number) % 20 == 0 else (int(total_number) // 20) + 1
    for index in range(1, max_page + 1):
        csv_file = FileOperations.MyCsvFile(case_folder + '\\' + 'case_list_' + str(index) + '.csv')
        if not csv_file.exists() or csv_file.get_size() == 0:
            download_caselist(search_criteria, index, csv_file)
        else:
            dl = csv_file.read_dict()
            if len(dl['doc_id']) < 20 and int(index) != int(max_page):
                print('original {} only contain {} cases, download again.'.format(csv_file.name, len(dl['doc_id'])))
                download_caselist(search_criteria, index, csv_file)
    if update:
        print('Max page updated. Download page {}.'.format(max_page))
        csv_file = FileOperations.MyCsvFile(case_folder + '\\' + 'case_list_' + str(max_page) + '.csv')
        download_caselist(search_criteria, max_page, csv_file)


def debug_download_single_list(wenshu, search_criteria, case_folder, index):
    csv_file = FileOperations.MyCsvFile(case_folder + '\\' + 'case_list_' + index + '.csv')
    wenshu.set_search_criteria(search_criteria)
    wenshu.get_case_list(index)
    csv_file.write(wenshu.case_brief)


def download_case(case_id):
    wenshu = Spider.WenShu()
    return wenshu.get_case(case_id)


def debug_download_case(wenshu, doc_id):
    t = download_case(wenshu, doc_id)
    print(t)

def download_1st_level_case_list(year, base_dir):
    for court in CourtList.court_list_all:
        search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:" + year + ",文书类型:判决书," + "基层法院:" + court
        case_list_dir = base_dir + '\\' + year + '\\CaseLists\\' + court
        FileOperations.MyFolder(case_list_dir).create()
        download_caselists(search_criteria, case_list_dir)
    return None

def download_mid_level_case_list(year, base_dir):
    court = '中级'
    search_criteria = "案件类型:刑事案件,法院地域:四川省,裁判年份:2017,法院层级:中级法院,文书类型:判决书,审判程序:一审"
    case_list_dir = base_dir + '\\' + year + '\\CaseLists\\' + court
    FileOperations.MyFolder(case_list_dir).create()
    download_caselists(search_criteria, case_list_dir)

def download_cases(year, base_dir):
    case_lists_folder = base_dir + '\\' + year + '\\CaseLists'
    for dir_r in FileOperations.MyFolder(case_lists_folder).get_file_list():
        if dir_r == "date":
            continue
        print("Downloading cases from {}".format(dir_r))
        download_a_folder_cases(year, base_dir, dir_r)

def download_a_folder_cases(year, base_dir, region_folder):
    caselists_region_folder = base_dir + '\\' + year + '\\CaseLists\\' + region_folder
    cases_region_folder = base_dir + '\\' + year + '\\Cases\\' + region_folder
    FileOperations.MyFolder(cases_region_folder).create()
    for file in FileOperations.MyFolder(caselists_region_folder).get_file_list():
        if file.endswith('csv'):
            csv_file = FileOperations.MyCsvFile(caselists_region_folder + '\\' + file)
            print(csv_file.name)
            case_list = csv_file.read_dict()
            for i in range(len(case_list['name'])):
                # Remove ? in case name, it's invalide in windows.
                case_file = FileOperations.MyTextFile(
                    cases_region_folder + '\\' + re.sub('[?#]', '', case_list['name'][i]) + '_' + case_list['doc_id'][
                        i] + '.txt')
                #if not case_file.exists() and case_list['download'][i] != 'Invalid':
                if not case_file.exists():
                    #                    if not case_file.exists() or case_file.get_size() < 1000 or  or case_list['download'][i] == 'N':
                    print("Trying to download case {} in {}: {}...".format(i, file, case_list['name'][i]))
                    t = download_case(case_list['doc_id'][i])
                    if t:
                        case_file.write(t)
                        case_list['download'][i] = 'Y'
                        print("Case {} in {}: {} is downloaded.".format(i, file, case_list['name'][i]))
                        if len(t) < 100:
                            case_list['download'][i] = 'Invalid'
                            print("Case {} in {}: {} download failed. The content size is less than 100 bytes.".format(i, file, case_list['name'][i]))
                    else:
                        print("Case {} in {}: {} download failed. The content is empty.".format(i, file, case_list['name'][i]))
                        case_list['download'][i] = 'N'
                    print("Sleep 2s ...")
                    time.sleep(2)
            csv_file.write(case_list)

def download_case_list_by_upload_date(year, base_folder, start_date, stop_date):
        search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:" + year + ",文书类型:判决书,上传日期:" + start_date + " TO " + stop_date
        case_list_dir = base_folder + '\\' + year + '\\CaseLists\\date'
        FileOperations.MyFolder(case_list_dir).create()
        total_number = get_total_number(search_criteria)
        if int(total_number) == 0:
            return None
        max_page = int(total_number) // 20 if int(total_number) % 20 == 0 else (int(total_number) // 20) + 1
        csv_file = FileOperations.MyCsvFile(case_list_dir + '\\' + 'case_list_' + start_date + " TO " + stop_date + '.csv')
        download_all_caselist(search_criteria, max_page, csv_file)

def download_case_by_upload_date(year, base_folder):
    caselists_folder = base_folder + '\\' + year + '\\caselists\\date'
    for case_list_csv in FileOperations.MyFolder(caselists_folder).get_file_list():
        csv_file = FileOperations.MyCsvFile(caselists_folder + '\\' + case_list_csv)
        print(csv_file.name)
        case_list = csv_file.read_dict()
        for i in range(len(case_list['name'])):
            cases_region_folder = base_folder + '\\' + year + '\\Cases\\' + case_list['court'][i]
            FileOperations.MyFolder(cases_region_folder).create()
            # Remove ? in case name, it's invalide in windows.
            case_file = FileOperations.MyTextFile(
                    cases_region_folder + '\\' + re.sub('[?#]', '', case_list['name'][i]) + '_' + case_list['doc_id'][
                        i] + '.txt')
            # if not case_file.exists() and case_list['download'][i] != 'Invalid':
            if not case_file.exists():
                    #                    if not case_file.exists() or case_file.get_size() < 1000 or  or case_list['download'][i] == 'N':
                print("Trying to download case {} in {}: {}...".format(i, case_list_csv, case_list['name'][i]))
                t = download_case(case_list['doc_id'][i])
                print("Sleep 2s ...")
                time.sleep(2)
                if t:
                    case_file.write(t)
                    print("Case {} in {}: {} is downloaded.".format(i, case_list_csv, case_list['name'][i]))
                else:
                    print("Case {} in {}: {} download failed. The content is empty.".format(i, file,
                                                                                                case_list['name'][i]))
    return None

def main():
    #year = '2018'
    base_dir = 'C:\\Users\\lij37\\Cases'
    years = ['2017', '2018']
    yesterday = datetime.date.today() - datetime.timedelta(1)

    for year in years:
        upload_date = '{}'.format(yesterday.year) + '-' + '{0:02d}'.format(yesterday.month) + '-' + '{0:02d}'.format(yesterday.day)
        #print(upload_date)
        download_case_list_by_upload_date(year, base_dir, upload_date, upload_date)
        download_case_by_upload_date(year, base_dir)
    return None

#    for year in ['2017', '2018']:
#        for mon in range(1, 2):
#            for day in range(26, 27):
#                upload_date = '2018-' + '{0:02d}'.format(mon) + '-' + '{0:02d}'.format(day)
#                download_case_list_by_upload_date(year, base_dir, upload_date, upload_date)
#        download_case_by_upload_date(year, base_dir)
#    return None
    #download_1st_level_case_list(year, base_dir)
    #download_mid_level_case_list(year, base_dir)
    #get_court_list(CourtList.court_list['zhongji'])
    #return None

    #download_cases(year, base_dir)
    desc = ""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-F', '--folder', action='store')
    parser.add_argument('-I', '--index', action='store')

    args = parser.parse_args()
    if args.folder:
        download_a_folder_cases(year, base_dir, args.folder)
    elif args.index:
        cases_list = FileOperations.MyFolder(base_dir + '\\' + year + '\\CaseLists').get_file_list()
        for index in range(int(args.index), int(args.index) + 10):
            download_a_folder_cases(year, base_dir, cases_list[index])
    else:
        download_cases(year, base_dir)

    return None
    # case_list_dir = base_dir + '\\' + year + '\\' + court
    case_folder = FileOperations.MyFolder(base_dir + '\\' + year + '\\' + '案件')
    debug_case_id = '2db9117a-d235-4f8d-8bd7-57f7029f2546'
    # path = 'C:\\Users\\lij37\\Code\\NewHan' + year + '\\'
    # court = '黑水县人民法院'
    # wenshu = Spider.WenShu()
    # # debug_download_case(wenshu, debug_case_id)
    # search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:" + year + ",文书类型:判决书," + "基层法院:" + court
    # case_list_dir = base_dir + '\\' + year + '\\' + court
    # debug_download_single_list(wenshu, search_criteria, case_list_dir, '2')
    # return None





    # refresh_total_number(wenshu, search_criteria, case_list_dir)
    case_list = FileOperations.MyCsvFile('C:\\Users\\lij37\\Code\\NewHan2017\\自贡市自流井区人民法院\\case_list_1.csv').read_dict()
    # case_name = '周某某危险驾驶一案一审判决书'
    # case_id = 'a9a069cd-832a-4f22-a576-a74d0123ca00'



if __name__ == "__main__":
    main()
