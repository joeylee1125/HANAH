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


def test_get_sue_date(path_2_file):
    verdict = VerdictAnalyserv2.VerdictAnalyser(path_2_file, YEAR)
    if verdict.size < 100 or "附带民事" in verdict.content:
        return None
    year, month, day = verdict.get_sue_date()

def test_get_judge_date(path_2_file):
    verdict = VerdictAnalyserv2.VerdictAnalyser(path_2_file, YEAR)
    if verdict.size < 100 or "附带民事" in verdict.content:
        return None
    year, month, day = verdict.get_judge_date()
    print(year, month, day)

def run_a_folder(func, folder):
    my_folder = FileOperations.MyFolder(CASE_DIR + '\\' + folder)
    for case in my_folder.get_file_list():
        print(my_folder.name + '\\' + case)
        func(my_folder.name + '\\' + case)
        print("")

def main():
    folder = '成都高新技术产业开发区人民法院'
    #f = test_get_sue_date
    f = test_get_judge_date
    run_a_folder(f, folder)


if __name__ == "__main__":
    main()