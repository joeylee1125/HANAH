# -*- coding: UTF-8 -*-
import os
import time
import Spider
import CourtList
import FileOperations


def get_total_number(search_criteria):
    wenshu = Spider.WenShu()
    wenshu.set_search_criteria(search_criteria)
    return wenshu.get_total_item_number()


def download_caselist(search_criteria, index, csv_file):
    cases = dict()
    wenshu = Spider.WenShu()
    wenshu.set_search_criteria(search_criteria)
    cases = wenshu.get_case_list(index)
    FileOperations.MyCsvFile(csv_file).write(cases)
    print('dump {} items into {}'.format(len(cases['doc_id']), cases))
    print('Sleep 10s.....')
    time.sleep(10)


def download_caselists(search_criteria, case_folder):
    file_list = os.listdir(case_folder)
    if not file_list:
        csv_file = case_folder + '\\' + 'case_list_1.csv'
        total_number = get_total_number(search_criteria)
        f = open(case_folder + '\\total_number_' + str(total_number), 'x')
        f.close()
    else:
        for file in file_list:
            if 'total_number' in file:
                total_number = file[13:]

    max_page = int(total_number) // 20
    if int(total_number) % 20:
        max_page += 1

    for index in range(1, max_page + 1):
        csv_file = case_folder + '\\' + 'case_list_' + str(index) + '.csv'
        if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
            download_caselist(search_criteria, index, csv_file)
        else:
            dl = FileOperations.MyCsvFile(csv_file).read_dict()
            if len(dl['doc_id']) < 20 and int(index) != int(max_page):
                print('original {} only contain {} cases, download again.'.format(csv_file, len(dl['doc_id'])))
                download_caselist(search_criteria, index, csv_file)


def debug_download_single_list(wenshu, search_criteria, case_folder, index):
    csv_file = case_folder + '\\' + 'case_list_' + index + '.csv'
    wenshu.set_search_criteria(search_criteria)
    wenshu.get_case_list(index)
    FileOperations.MyCsvFile(csv_file).write(wenshu.case_brief)


def download_case(wenshu, case_id):
    return wenshu.get_case(case_id)


def debug_download_case(wenshu, doc_id):
    t = download_case(wenshu, doc_id)
    print(t)


def main():
    year = '2014'
    base_dir = 'C:\\Users\\lij37\\Cases'
    # case_list_dir = base_dir + '\\' + year + '\\' + court
    case_dir = base_dir + '\\' + year + '\\' + '案件'
    debug_case_id = '2db9117a-d235-4f8d-8bd7-57f7029f2546'
    # path = 'C:\\Users\\lij37\\Code\\NewHan' + year + '\\'
    # court = '黑水县人民法院'
    # wenshu = Spider.WenShu()
    # # debug_download_case(wenshu, debug_case_id)
    # search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:" + year + ",文书类型:判决书," + "基层法院:" + court
    # case_list_dir = base_dir + '\\' + year + '\\' + court
    # debug_download_single_list(wenshu, search_criteria, case_list_dir, '2')
    # return None

    for court in CourtList.court_list_all:
        search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:" + year + ",文书类型:判决书," + "基层法院:" + court
        case_list_dir = base_dir + '\\' + year + '\\' + court
        FileOperations.MyFolder(case_list_dir).create()
        download_caselists(search_criteria, case_list_dir)
    return None

    # refresh_total_number(wenshu, search_criteria, case_list_dir)
    case_list = FileOperations.MyCsvFile('C:\\Users\\lij37\\Code\\NewHan2017\\自贡市自流井区人民法院\\case_list_1.csv').read_dict()
    # case_name = '周某某危险驾驶一案一审判决书'
    # case_id = 'a9a069cd-832a-4f22-a576-a74d0123ca00'
    FileOperations.MyFolder(case_dir).create()
    file_list = os.listdir(case_list_dir)
    for file in file_list:
        if 'csv' in file:
            case_list = FileOperations.MyCsvFile(case_list_dir + '\\' + file).read_dict()
            for i in range(len(case_list['name'])):
                # if case_list['download'][i] != 'Y':
                case_file = case_dir + '\\' + case_list['name'][i] + '_' + case_list['doc_id'][i] + '.txt'
                if not os.path.exists(case_file) or os.path.getsize(case_file) < 1000:
                    print("Case {} in {}: {} {} is downloading...".format(i, file, case_list['name'][i],
                                                                          case_list['doc_id'][i]))
                    t = download_case(wenshu, case_list['doc_id'][i])
                    if t:
                        try:
                            FileOperations.MyTextFile(case_file).write(t)
                            case_list['download'][i] = 'Y'
                            time.sleep(3)
                        except Exception as e:
                            print(e)
                            case_list['download'][i] = 'Invalid'
                    else:
                        case_list['download'][i] = 'Invalid'
            FileOperations.MyCsvFile(case_list_dir + '\\' + file).write(case_list)

if __name__ == "__main__":
    main()
