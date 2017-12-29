# -*- coding: UTF-8 -*-
import re
import sys
import os
import time
import csv
import argparse
import codecs

from shutil import copyfile
from shutil import copytree
from shutil import move
from docx import Document

from PIL import Image
from io import BytesIO
#import pytesseract as ocr
#import tesserocr





def dump2csv(data_dict, file_name):
    with open(file_name, 'w', newline='', encoding='utf-8_sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_dict.keys())
        writer.writerows(zip(*data_dict.values()))
        

def read_csv(file_name):
    with open(file_name, encoding='utf-8_sig') as csvfile:
        reader = csv.DictReader(csvfile)
        data_dict = dict.fromkeys(reader.fieldnames)
        for key in data_dict:
            data_dict[key] = []
        for row in reader:
            for key in data_dict:
                data_dict[key].append(row[key])
    return data_dict


def transfer2doc(folder):
    file_list = os.listdir(folder)
    for file in file_list:
        move(folder + '\\' + file, folder + '\\' + file[:-4] + '.doc')
        
        
def validate_file_name(folder):
    if '•' in file:
        print(file)
        move(folder + '\\' + file, folder + '\\' + file.replace('•', ''))

def copy_folder(src, dst):
    print('copy %s to %s' % (src, dst))
    copytree(src, dst)
        
def delete_doc(folder):        
    file_list = os.listdir(folder)
    for file in file_list:
        if file[-5:] == '.docx':
            os.remove(folder + '\\' + file) 

def copy_csv(src, dst):
    copyfile(src, dst)

    
def move_file(src_folder, dst_folder):
    file_list = os.listdir(src_folder)
    for file in file_list:
        move(src_folder + '\\' + file, dst_folder + '\\' + file)
    
    
def validate_path(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        
        
def count_files(folder):
    return len(os.listdir(folder))
    
def download_invalid(court):
    case_matrix = read_csv('C:\\Users\\lij37\\Code\\Summer\\2016\\' + court + '_valid')
    count = len(case_matrix['name'])
    search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:2016,文书类型:判决书," + "基层法院:" + court
    wenshu = Spider.WenShu()
    wenshu.setSearchCriteria(search_criteria)
    for i in range(count):
        path = 'C:\\Users\\lij37\\Code\\Summer\\2016\\' + court + '\\'
        if case_matrix['valid'][i] == 'N':
            print('%s/%s' % (i, count))
            wenshu.downloadDocument(path,
                                    case_matrix['name'][i],
                                    case_matrix['doc_id'][i],
                                    case_matrix['date'][i])
            if os.path.getsize(path + case_matrix['name'][i] + case_matrix['date'][i] + '.txt') < 20000:
                wenshu.downloadDocument(path,
                                    case_matrix['name'][i],
                                    case_matrix['doc_id'][i],
                                    case_matrix['date'][i])
    
    file_list = os.listdir(path[:-1])
    for file in file_list:
        if 'txt' in file:
            move(path + file, 'C:\\Users\\lij37\\Code\\Summer\\2016\\TEMP\\' + file[:-4] + '.doc')
    
def add_cols_2_matrix(matrix, col_list):
    key_list = list(matrix.keys())
    for key in col_list:
        matrix[key] = [''] * len(matrix[key_list[0]])
    return matrix


def open_img():
    with open('0.jpg', 'rb') as f:
        img = Smooth(process_img(Image.open(f)))
        print(recognize(img))
    
def process_img(img, threshold=180):
    '''对图片进行二值化 255 是白色 0是黑色'''
    # 灰度转换
    img = img.convert('L')
    # 二值化
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            pixels[x,y] = 255 if pixels[x,y] > threshold else 0
    return img


def Smooth(Picture):
    '''平滑降噪
        二值化的图片传入 去除像噪小点
    '''
    Pixels = Picture.load()
    (Width, Height) = Picture.size

    xx = [1, 0, -1, 0]
    yy = [0, 1, 0, -1]

    for i in range(Width):
        for j in range(Height):
            if Pixels[i, j] != 255:
                Count = 0
                for k in range(4):
                    try:
                        if Pixels[i + xx[k], j + yy[k]] == 255:
                            Count += 1
                    except IndexError:  # 忽略访问越界的情况
                        pass
                if Count > 3:
                    Pixels[i, j] = 255
    return Picture

def recognize(img, lang='eng'):
    return ocr.image_to_string(img, lang)



    
    
    
    
def main():
    p1 = Image.open('0.jpg')
    tesserocr.image_to_text(p1)

    open_img()  
    sys.exit(0)
    desc = ""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-c', '--court', action='store')
    parser.add_argument('-m', '--move', action='store_true')
    parser.add_argument('-d', '--delete', action='store_true')
    parser.add_argument('-v', '--validate', action='store_true')
    parser.add_argument('-i', '--download_invalid', action='store_true')
    parser.add_argument('-t', '--transfer', action='store_true')
    args = parser.parse_args()
    # Move han1/Download_xxxx/*   2016/XXXX/*
    #print(CourtList.court_list)
    
    court = args.court
    src_folder_name = 'C:\\Users\\lij37\\Code\\Han1\\Download_' + court
    dst_folder_name = 'C:\\Users\\lij37\\Code\\Summer\\2016\\' + court
    src_csv_name = 'C:\\Users\\lij37\\Code\\Han1\\casephase1_' + court + '.csv'
    dst_csv_name = 'C:\\Users\\lij37\\Code\\Summer\\2016\\' + court + '.csv'
     
    
    #for court in CourtList.court_list:
    #    src_folder_name = 'C:\\Users\\lij37\\Code\\Han1\\Download_' + court
    #    dst_folder_name = 'C:\\Users\\lij37\\Code\\Summer\\2016\\' + court
    #    src_csv_name = 'C:\\Users\\lij37\\Code\\Han1\\casephase1_' + court + '.csv'
    #    dst_csv_name = 'C:\\Users\\lij37\\Code\\Summer\\2016\\' + court + '.csv'
    
    if args.move:
        copy_folder(src_folder_name, dst_folder_name)
        copy_csv(src_csv_name, dst_csv_name)
        #case_matrix = read_csv('C:\\Users\\lij37\\Code\\Summer\\2016\\' + court)
        #for idx in range(len(case_matrix['name'])):
        #    if '•' in case_matrix['name'][idx]:
        #        print(case_matrix['name'][idx])
        #        case_matrix['name'][idx] = case_matrix['name'][idx].replace('•', '')
        #dump2csv(case_matrix, 'C:\\Users\\lij37\\Code\\Summer\\2016\\' + court)
        transfer2doc(dst_folder_name)
        #validate_file_name(dst_folder_name)
    if not args.move and args.delete:
        file_list = os.listdir(dst_folder_name)
        for file in file_list:
            if file[-4:] == 'docx':
                #os.remove(tmp_folder + '\\' + file)
                os.remove(dst_folder_name + '\\' + file[:-4] + 'doc')
    
    if args.validate:
        validate(court)
        
    
    if args.download_invalid:
        download_invalid(court)
    
    if args.transfer:
        file_list = os.listdir('C:\\Users\\lij37\\Code\\Summer\\2016\\TEMP\\')
        for file in file_list:
            if file[-4:] == 'docx':
                os.remove('C:\\Users\\lij37\\Code\\Summer\\2016\\TEMP\\' + file[:-4] + 'doc')
        file_list = os.listdir('C:\\Users\\lij37\\Code\\Summer\\2016\\TEMP\\')
        for file in file_list:
            move('C:\\Users\\lij37\\Code\\Summer\\2016\\TEMP\\' + file, 'C:\\Users\\lij37\\Code\\Summer\\2016\\' + court + '\\' + file)
    
    
if __name__ == "__main__":
    main()