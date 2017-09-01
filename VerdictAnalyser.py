# -*- coding: UTF-8 -*-
import re
import sys
#import os
#import time
#import codecs
#from datetime import date, datetime

#from shutil import copyfile
from docx import Document

#import CourtList


class VerdictAnalyser:
    def __init__(self, doc_name):
        self.content = ''
        self.doc_name = doc_name
        self.case_id_pattern = re.compile('[(（]\d\d\d\d[）)].*?号')
        self.verdict_pattern = re.compile(".*?判决书")
        self.prosecutor_pattern = re.compile('(?<=公诉机关).*?人民检察院')
        self.court_pattern = re.compile('\w+中级(?:人民)?法院')

    def _remove_space(self):
        self.content = self.content.replace(' ', '')

    def read_doc(self):
        try:
            document = Document(self.doc_name) if self.doc_name else sys.exit(0)
            l = [paragraph.text for paragraph in document.paragraphs]
            self.content = ''.join(str(e) for e in l)
        except:
            print("Document %s is invalid" % self.doc_name)

    def analyse_doc(self):
        self.read_doc()
        self._remove_space()
