# -*- coding: UTF-8 -*-
# import re
import sys
import os
# import time
# import csv
import argparse
# import codecs

# from shutil import copyfile
# from docx import Document

import VerdictAnalyser
# import CourtList


def main():    
    desc = " [ -F|--folder folder ] [ -f|--file file]."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-F', '--folder', action='store')
    parser.add_argument('-f', '--file', action='store')
    args = parser.parse_args()

    if args.file:
        verdict = VerdictAnalyser.VerdictAnalyser(args.file)
        verdict.analyse_doc()
        #print(verdict.content)
    elif args.folder:
        file_list = os.listdir(args.folder)
        for file in file_list:
            print('')
            print(file)
            verdict = VerdictAnalyser.VerdictAnalyser(args.folder + '\\' + file)
            verdict.analyse_doc()
        #print(os.listdir(args.folder))
    else:
        print(sys.argv[0] + desc)

if __name__ == "__main__":
    main()
