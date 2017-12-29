# -*- coding: UTF-8 -*-

import csv
import argparse
import os
import sys

import Spider
import CourtList
import FileUtils

def download_caselist(search_criteria, csv_file):
    print('Downloading case list of court %s' % csv_file)
    case_matrix = dict()
    wenshu = Spider.WenShu()
    wenshu.setSearchCriteria(search_criteria)
    wenshu.get_total_item_number()
    wenshu.get_case_list()
    return None
    
    
    
    
    
    
    
    
    
    wenshu.get_cookie_str()


    print("Total case number is %s" % wenshu.total_items)
    if wenshu.total_items:
        get_case_info(wenshu)
    else:
        print("Failed to get total items.")
        sys.exit(1)
    case_matrix['name'] = wenshu.case['name']
    case_matrix['doc_id'] = wenshu.case['doc_id']
    case_matrix['date'] = wenshu.case['date']
    case_matrix['case_id'] = wenshu.case['case_id']
    case_matrix['procedure'] = wenshu.case['procedure']
    case_matrix['court'] = wenshu.case['court']
    
    print('%s %s' % (wenshu.total_items, len(case_matrix['name'])))

#    FileUtils.dump2csv(case_matrix, csv_file)

def main():
    year = '2017'
    path = 'C:\\Users\\lij37\\Code\\NewHan' + year + '\\'
    court = '自贡市自流井区人民法院'
    search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:" + year +",文书类型:判决书," + "基层法院:" + court
    csv_file = path + court + '.csv'
    case_folder = path + court
    download_caselist(search_criteria, csv_file)
    FileUtils.validate_path(path)
    FileUtils.dump2csv(wenshu.case_brief, csv_file)

   
    
if __name__ == "__main__":
    main()