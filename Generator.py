# -*- coding: UTF-8 -*-
#import re
#import sys
#import os
#import time
#import csv
import argparse
#import codecs

#from shutil import copyfile
#from docx import Document

import VerdictAnalyser
#import CourtList


def main():    
    desc = ""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-F', '--folder', action='store')
    parser.add_argument('-f', '--file', action='store')
    args = parser.parse_args()

    verdict = VerdictAnalyser.VerdictAnalyser(args.file)
    verdict.analyse_doc()
    print(verdict.content)

if __name__ == "__main__":
    main()