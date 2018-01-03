# -*- coding: UTF-8 -*-

import csv
import argparse
import os
import sys
import time
import json
import Spider
import CourtList
import FileUtils
import re


def refresh_total_number(wenshu, case_folder):
    total_number = wenshu.get_total_item_number()
    if total_number:
        try:
            f = open(case_folder + '\\total_number_' + str(total_number), 'x')
            f.close()
        except Exception as e:
            print(e)


def download_caselist(wenshu, index, csv_file):
    cases = dict()
    cases = wenshu.get_case_list(index)
    FileUtils.dump2csv(cases, csv_file)
    print('dump {} items into {}'.format(len(cases['doc_id']), cases))
    print('Sleep 10s.....')
    time.sleep(10)


def download_caselists(wenshu, case_folder):
    file_list = os.listdir(case_folder)
    if not file_list:
        csv_file = case_folder + '\\' + 'case_list_1.csv'
        total_number = wenshu.get_total_item_number()
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
            download_caselist(wenshu, index, csv_file)
        else:
            dl = FileUtils.read_csv(csv_file)
            if len(dl['doc_id']) < 20 and int(index) != int(max_page):
                print('original {} only contain {} cases, download again.'.format(csv_file, len(dl['doc_id'])))
                download_caselist(wenshu, index, csv_file)


def debug_download_single_list(wenshu, search_criteria, case_folder, index):
    csv_file = case_folder + '\\' + 'case_list_' + index + '.csv'
    wenshu.set_search_criteria(search_criteria)
    wenshu.get_case_list(index)
    FileUtils.dump2csv(wenshu.case_brief, csv_file)


def download_case(wenshu, case_id):
    return wenshu.get_case(case_id)


def debug_download_case(wenshu, doc_id):
    t = download_case(wenshu, doc_id)
    print(t)


def main():
    year = '2014'
    # court = '自贡市自流井区人民法院'
    # court = '黑水县人民法院'
    # court = '二审'
    base_dir = 'C:\\Users\\lij37\\Cases'
    # case_list_dir = base_dir + '\\' + year + '\\' + court
    case_dir = base_dir + '\\' + year + '\\' + '案件'
    debug_case_id = '2db9117a-d235-4f8d-8bd7-57f7029f2546'
    # path = 'C:\\Users\\lij37\\Code\\NewHan' + year + '\\'
    court = '金堂县人民法院'
    # court = '黑水县人民法院'
    # search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:" + year +",文书类型:判决书," + "基层法院:" + court
    # search_criteria = "案件类型:刑事案件,审判程序:二审,法院地域:四川省,裁判年份:" + year + ",文书类型:判决书"
    court_list = ['成都市锦江区人民法院', '成都市青羊区人民法院', '成都市金牛区人民法院',
                  '成都市武侯区人民法院', '成都市成华区人民法院', '成都市龙泉驿区人民法院', '成都市青白江区人民法院',
                  '成都市温江区人民法院', '金堂县人民法院', '双流区人民法院', '郫县人民法院',
                  '大邑县人民法院', '蒲江县人民法院', '新津县人民法院', '都江堰市人民法院', '彭州市人民法院',
                  '邛崃市人民法院', '崇州市人民法院', '成都高新技术产业开发区人民法院', '自贡市自流井区人民法院', '自贡市贡井区人民法院', '自贡市大安区人民法院', '自贡市沿滩区人民法院',
                  '荣县人民法院', '富顺县人民法院', '攀枝花市东区人民法院', '攀枝花市西区人民法院', '攀枝花市仁和区人民法院', '米易县人民法院', '盐边县人民法院', '泸州市江阳区人民法院',
                  '泸州市纳溪区人民法院', '泸州市龙马潭区人民法院', '泸县人民法院', '合江县人民法院', '叙永县人民法院', '古蔺县人民法院', '德阳市旌阳区人民法院', '中江县人民法院',
                  '罗江县人民法院', '广汉市人民法院', '什邡市人民法院', '绵竹市人民法院', '绵阳市涪城区人民法院', '绵阳市游仙区人民法院', '三台县人民法院', '盐亭县人民法院',
                  '绵阳市安州区人民法院', '梓潼县人民法院', '北川羌族自治县人民法院', '平武县人民法院', '江油市人民法院', '四川省科学城人民法院', '绵阳高新技术产业开发区人民法院',
                  '广元市利州区人民法院', '广元市昭化区人民法院', '广元市朝天区人民法院', '旺苍县人民法院', '青川县人民法院', '剑阁县人民法院', '苍溪县人民法院', '遂宁市船山区人民法院',
                  '船山区人民法院', '遂宁市安居区人民法院', '蓬溪县人民法院', '射洪县人民法院', '大英县人民法院', '内江市市中区人民法院', '内江市东兴区人民法院', '威远县人民法院',
                  '资中县人民法院', '隆昌县人民法院', '乐山市市中区人民法院', '乐山市沙湾区人民法院', '乐山市五通桥区人民法院', '乐山市金口河区人民法院', '犍为县人民法院', '井研县人民法院',
                  '夹江县人民法院', '沐川县人民法院', '峨边彝族自治县人民法院', '马边彝族自治县人民法院', '峨眉山市人民法院', '南充市顺庆区人民法院', '南充市高坪区人民法院',
                  '南充市嘉陵区人民法院', '南部县人民法院', '营山县人民法院', '蓬安县人民法院', '仪陇县人民法院', '西充县人民法院', '阆中市人民法院', '眉山市东坡区人民法院',
                  '眉山市彭山区人民法院', '仁寿县人民法院', '彭山县人民法院', '洪雅县人民法院', '丹棱县人民法院', '青神县人民法院', '宜宾市翠屏区人民法院', '宜宾市南溪区人民法院',
                  '宜宾县人民法院', '江安县人民法院', '长宁县人民法院', '高县人民法院', '珙县人民法院', '筠连县人民法院', '兴文县人民法院', '屏山县人民法院', '广安市广安区人民法院',
                  '广安市前锋区人民法院', '岳池县人民法院', '武胜县人民法院', '邻水县人民法院', '华蓥市人民法院', '达州市通川区人民法院', '达州市达川区人民法院', '宣汉县人民法院',
                  '开江县人民法院', '大竹县人民法院', '渠县人民法院', '万源市人民法院', '雅安市雨城区人民法院', '雅安市名山区人民法院', '荥经县人民法院', '汉源县人民法院',
                  '石棉县人民法院', '天全县人民法院', '芦山县人民法院', '宝兴县人民法院', '巴中市巴州区人民法院', '巴中市恩阳区人民法院', '通江县人民法院', '南江县人民法院',
                  '平昌县人民法院', '资阳市雁江区人民法院', '安岳县人民法院', '乐至县人民法院', '简阳市人民法院', '汶川县人民法院', '理县人民法院', '茂县人民法院', '松潘县人民法院',
                  '九寨沟县人民法院', '金川县人民法院', '小金县人民法院', '黑水县人民法院', '马尔康市人民法院', '马尔康县人民法院', '壤塘县人民法院', '阿坝县人民法院', '若尔盖县人民法院',
                  '红原县人民法院', '康定市人民法院', '康定县人民法院', '泸定县人民法院', '丹巴县人民法院', '九龙县人民法院', '雅江县人民法院', '道孚县人民法院', '炉霍县人民法院',
                  '甘孜县人民法院', '新龙县人民法院', '德格县人民法院', '白玉县人民法院', '石渠县人民法院', '色达县人民法院', '理塘县人民法院', '巴塘县人民法院', '乡城县人民法院',
                  '稻城县人民法院', '得荣县人民法院', '西昌市人民法院', '木里藏族自治县人民法院', '盐源县人民法院', '德昌县人民法院', '会理县人民法院', '会东县人民法院', '宁南县人民法院',
                  '普格县人民法院', '布拖县人民法院', '金阳县人民法院', '昭觉县人民法院', '喜德县人民法院', '冕宁县人民法院', '越西县人民法院', '甘洛县人民法院', '美姑县人民法院',
                  '雷波县人民法院']

    # wenshu = Spider.WenShu()
    # # debug_download_case(wenshu, debug_case_id)
    # # court = '自贡市大安区人民法院'
    # search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:" + year + ",文书类型:判决书," + "基层法院:" + court
    # case_list_dir = base_dir + '\\' + year + '\\' + court
    # debug_download_single_list(wenshu, search_criteria, case_list_dir, '2')
    # return None

    for court in court_list:
        wenshu = Spider.WenShu()
        search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:" + year + ",文书类型:判决书," + "基层法院:" + court
        wenshu.set_search_criteria(search_criteria)
        case_list_dir = base_dir + '\\' + year + '\\' + court
        FileUtils.validate_path(case_list_dir)
        download_caselists(wenshu, case_list_dir)
    return None

    # refresh_total_number(wenshu, search_criteria, case_list_dir)
    # case_list = FileUtils.read_csv('C:\\Users\\lij37\\Code\\NewHan2017\\自贡市自流井区人民法院\\case_list_1.csv')
    # case_name = '周某某危险驾驶一案一审判决书'
    # case_id = 'a9a069cd-832a-4f22-a576-a74d0123ca00'
    FileUtils.validate_path(case_dir)
    file_list = os.listdir(case_list_dir)
    for file in file_list:
        if 'csv' in file:
            case_list = FileUtils.read_csv(case_list_dir + '\\' + file)
            for i in range(len(case_list['name'])):
                # if case_list['download'][i] != 'Y':
                case_file = case_dir + '\\' + case_list['name'][i] + '_' + case_list['doc_id'][i] + '.txt'
                if not os.path.exists(case_file) or os.path.getsize(case_file) < 1000:
                    print("Case {} in {}: {} {} is downloading...".format(i, file, case_list['name'][i],
                                                                          case_list['doc_id'][i]))
                    t = download_case(wenshu, case_list['doc_id'][i])
                    if t:
                        try:
                            FileUtils.write_text(case_file, t)
                            case_list['download'][i] = 'Y'
                            time.sleep(3)
                        except Exception as e:
                            print(e)
                            case_list['download'][i] = 'Invalid'
                    else:
                        case_list['download'][i] = 'Invalid'
            FileUtils.dump2csv(case_list, case_list_dir + '\\' + file)


if __name__ == "__main__":
    main()
