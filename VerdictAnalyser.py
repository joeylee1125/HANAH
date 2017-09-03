# -*- coding: UTF-8 -*-
import re
import sys
# import os
# import time
# import codecs
# from datetime import date, datetime

# from shutil import copyfile
from docx import Document
from docx.opc.exceptions import PackageNotFoundError
import CourtList


class VerdictAnalyser:
    def __init__(self, doc_name):
        self.content = ''
        self.doc_name = doc_name
        self.case_id_pattern = re.compile('[(（]\d\d\d\d[）)].*?号')
        self.verdict_pattern = re.compile(".*?判决书")
        self.prosecutor_pattern = re.compile('(?<=公诉机关).*?人民检察院')
        self.court_pattern = re.compile('\w+人民法院')
        self.judgement_pattern = re.compile('(?:判决|判处|决定)(?:结果|如下).*')
        self.charge_pattern = re.compile('(?<=犯).+?罪')
        self.accuse_pattern = re.compile('指控.*?审理终结')


        self.defendent_pattern = []
        self.defendent_pattern.append(re.compile('(?<=被告人).+?[，,（(。]'))
        self.defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.last_name + '\w{1,3}(?=[。，,（(]|201|犯)'))
        self.defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.ss_name))
        self.defendent_pattern.append(re.compile('(?<=被告人..情况姓名)' + CourtList.last_name + '\w{0,4}[，（|出生日期|性别]'))
        self.defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.last_name + '\w{0,4}成都市'))
        self.defendent_pattern.append(re.compile('(?<=被告人姓名)' + CourtList.last_name + '\w{0,4}出生日期'))
        self.defendent_pattern.append(re.compile('(?<=被告)人?[：:?]' + CourtList.last_name + '\w{0,4}(?=[。，,（(]|201)'))
        self.defendent_pattern.append(re.compile(CourtList.invalide_name))

    def _remove_space(self):
        self.content = self.content.replace(' ', '')

    def read_doc(self):
        try:
            document = Document(self.doc_name) if self.doc_name else sys.exit(0)
            l = [paragraph.text for paragraph in document.paragraphs]
            self.content = ''.join(str(e) for e in l)
        except PackageNotFoundError:
            print("Document %s is invalid" % self.doc_name)

    def _search_defendent(self):
        # Start to search from pattern 1.
        # Pattern 0 is reserved to search all.
        for p in self.defendent_pattern[1:]:
            d_list = re.findall(p, self.content)
            if d_list:
                break
        else:
            print(self.doc_name)
            print(re.findall(self.defendent_pattern[0], self.content))
            sys.exit(0)

        d_list.sort(key=lambda x: len(x))
        raw_list_c = len(d_list)
        if raw_list_c > 1:
            i = 0
            j = 1
            while i < j:
                j = i + 1
                while j < raw_list_c:
                    if d_list[i] in d_list[j]:
                        d_list.pop(j)
                        raw_list_c -= 1
                    else:
                        j += 1
                i += 1
        bl = []

        for b in d_list:
            for k in CourtList.not_a_name_list:
                if k in b:
                    # print(b)
                    break
            else:
                bl.append(b)
        return bl

    def _get_defendent(self):
        defendent_list = self._search_defendent()
        if defendent_list:
            return defendent_list
        else:
            print('--------------------->')
            print(self.doc_name)
            return ['']

    def _search(self, pattern, text=None):
        if text is None: text = self.content
        result = re.search(pattern, text)
        return result.group() if result is not None else None

    def _get_case_id(self):
        return self._search(self.case_id_pattern)

    def _get_verdict_name(self):
        return self._search(self.verdict_pattern)

    def _get_court_name(self,verdict_name):
        return self._search(self.court_pattern, verdict_name)

    def _get_prosecutor(self):
        return self._search(self.prosecutor_pattern)

    def _get_judgement(self):
        return self._search(self.judgement_pattern)

    def _get_accuse_section(self):
        return self._search(self.accuse_pattern)

    def _get_lawyer(self, defendent):
        if self.accuse_section:
            dl = re.search('.*被告人(.*)到庭', self.accuse_section).group(1)
            # print(dl)
            if dl:
                l = re.search('.*辩护人.*', dl)
                if l: print(l.group())

        else:
            # print('=[==================================================>%s' % self.doc_name)
            pass
        return None

    def _get_charge(self, defendent):
        # print(judgement_section)
        # return self._search(self.charge_pattern, judgement_section)
        return self._search('(?<=被告人' + defendent + '犯).+?罪', self.judgement_section)

    def analyse_doc(self):
        case_info = {}
        self.read_doc()
        self._remove_space()
        case_info['name'] = self._get_defendent()
        case_info['verdict'] = self._get_verdict_name()
        case_info['case_id'] = self._get_case_id()
        case_info['court'] = self._get_court_name(case_info['verdict'])
        case_info['prosecutor'] = self._get_prosecutor()
        case_info['nation'] = self._get_nation()
        case_info['defendent'] = []
        case_info['defendent'] = self._get_defendent()

        info_list = ['name','case_id','court','prosecutor','defendent','verdict']
        for i in info_list:
            print("Case " + i + " is %s" % case_info[i])
