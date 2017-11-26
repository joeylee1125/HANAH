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
        self.accuse_section = ''
        self.content = ''
        self.year = ''
        self.doc_name = doc_name
        self.case_id_pattern = re.compile('[(（]\d\d\d\d[）)].*?号')
        self.verdict_pattern = re.compile(".*?判决书")
        self.prosecutor_pattern = re.compile('(?<=公诉机关).*?人民检察院')
        self.court_pattern = re.compile('\w+人民法院')
        self.year_pattern = re.compile('[12]\d{3}')
        self.judgement_pattern = re.compile('(?:判决|判处|决定)(?:结果|如下).*')
        self.charge_pattern = re.compile('(?<=犯).+?罪')
        self.accuse_pattern = re.compile('指控.*?审理终结')
        
        self.defendent_section_pattern = []
        self.defendent_section_pattern.append(re.compile('被告人.*?起诉书'))
        self.defendent_section_pattern.append(re.compile('被告人.*?人民检察院指控'))
        self.defendent_section_pattern.append(re.compile('被告人.*?自诉'))
        self.defendent_info_pattern = re.compile('被告人.*?(?=被告人|起诉书|人民检察院指控|自诉)')
        
        
        
        self.convict_section_pattern = []
        self.convict_section_pattern.append(re.compile('(?<=判决如下).*如不服本判决'))
        self.convict_info_pattern = re.compile('被告人.*?(?=被告人|如不服本判决)')
        
        self.defendent_sex_pattern = re.compile('(?<=，)[男女](?=，)')
        self.defendent_nation_pattern = re.compile('(?<=，)' + CourtList.nation_list + '族(?=，)')
        self.defendent_education_pattern = re.compile(CourtList.education_list)
        self.defendent_job_pattern = re.compile(CourtList.job_list)

        self.defendent_lawyer_pattern = re.compile('(?<!指定)辩护人.*?(?:事务所|法律援助中心|分所)律师')
        self.defendent_law_firm_pattern = re.compile('(?<=辩护人).*?事务所律师')
        
        self.defendent_pattern = []
        self.defendent_pattern.append(re.compile('(?<=被告人).+?[，,（(。]'))
        self.defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.last_name + '\w{1,3}(?=[。，,（(]|201|犯)'))
        self.defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.ss_name))
        self.defendent_pattern.append(re.compile('(?<=被告人..情况姓名)' + CourtList.last_name + '\w{0,4}[，（|出生日期|性别]'))
        self.defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.last_name + '\w{0,4}成都市'))
        self.defendent_pattern.append(re.compile('(?<=被告人姓名)' + CourtList.last_name + '\w{0,4}出生日期'))
        self.defendent_pattern.append(re.compile('(?<=被告)人?[：:?]' + CourtList.last_name + '\w{0,4}(?=[。，,（(]|201)'))
        self.defendent_pattern.append(re.compile(CourtList.invalid_name))

        self.born_date_pattern = []
        self.born_date_pattern.append(re.compile('(\d\d\d\d)年(\d{1,2})月(\d{1,2})日出生'))
        self.born_date_pattern.append(re.compile('出生于(\d\d\d\d)年(\d{1,2})月(\d{1,2})日'))
        
        
    def _remove_space(self):
        self.content = self.content.replace(' ', '')

    def read_doc(self):
        try:
            document = Document(self.doc_name) if self.doc_name else sys.exit(0)
            l = [paragraph.text for paragraph in document.paragraphs]
            self.content = ''.join(str(e) for e in l)
        except PackageNotFoundError:
            print("Document %s is invalid" % self.doc_name)

    def _search_defendent(self, context):
        # Start to search from pattern 1.
        # Pattern 0 is reserved to search all.
        for p in self.defendent_pattern[1:]:
            d_list = re.findall(p, context)
            if d_list:
                break
        else:
            print(self.doc_name)
            print(re.findall(self.defendent_pattern[0], context))
            sys.exit(0)
        print(d_list)
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
        if text is None:
            text = self.content
        result = re.search(pattern, text)
        return result.group() if result is not None else None

    def _get_case_id(self):
        return self._search(self.case_id_pattern)

    def _get_verdict_name(self):
        return self._search(self.verdict_pattern)

    def _get_court_name(self, verdict_name):
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

    def _get_year(self, id):
        self.year = self._search(self.year_pattern, id)
        return self.year

    def _get_section(self, section_name):
        if section_name == "defendent":
            for p in self.defendent_section_pattern:
                defendent_section = self._search(p, self.content)
                if defendent_section: break
            #print(defendent_section)
            return defendent_section
        if section_name == "convict":
            for p in self.convict_section_pattern:
                convict_section = self._search(p, self.content)
                if convict_section: break
            #print(convict_section)
            return convict_section    
            
    def _get_defendent_name(self, context):
        for p in self.defendent_pattern[1:]:
            d = re.search(p, context)
            if d: break
        if d: return d.group()
        
    def _get_defendent_age(self, df_sec):
        for p in self.born_date_pattern:
            born_date = re.search(p, df_sec)
            if born_date: break
        else:
            return None
        born_year = born_date.group(1)
        age = int(self.year) - int(born_year)
        return age
        
    def _get_defendent_sex(self, df_sec):
        sex = self._search(self.defendent_sex_pattern, df_sec)
        return sex

    def _get_defendent_nation(self, df_sec):
        nation = self._search(self.defendent_nation_pattern, df_sec)
        return nation

    def _get_defendent_education(self, df_sec):
        education = self._search(self.defendent_education_pattern, df_sec)
        return education

    def _get_defendent_job(self, df_sec):
        job = self._search(self.defendent_job_pattern, df_sec)
        return job
    
    def _get_defendent_lawyer(self, df_sec):
        lawyer_list = re.findall(self.defendent_lawyer_pattern, df_sec)
        return lawyer_list
        
    def _get_defendent_law_firm(self, df_sec):    
        law_firm_list = re.findall(self.defendent_law_firm_pattern, df_sec)
        return law_firm_list
    
    def _get_defendent_charge(self, d_name, cv_result):
        for cv in cv_result:
        #    print(cv, d_name)
            if re.search(d_name, cv):
                charge = re.search('(?<=犯).*?(?=罪)', cv)
                break
        if charge:
            print("%s ---------------> %s" % (d_name, charge.group()))
        else:
            print("%s ---------------> NOT FOUND" % d_name)
            print(cv_result)
        return charge.group()
        
        
    def _get_defendent_info(self):
        df_sec = self._get_section('defendent')
        # df_sec should have content like 被告人.....被告人.....起诉书
        if df_sec:
            df_result = re.findall(self.defendent_info_pattern, df_sec)
            # print(df_result)
            # 被告人曾宇，男，1980年12月15日出生（身份证号码：），汉族，大学文化，无业，户籍所在地：成都市成华区。
        if not df_result:
            print("warning -----------------> no defendent result found by %s" % self.defendent_info_pattern)

        cv_sec = self._get_section('convict')
        if cv_sec:
            cv_result = re.findall(self.convict_info_pattern, cv_sec)
        if not cv_result:
            print("warning -----------------> no convict result found by %s" % self.convict_info_pattern)    
            
        defendent_list = [ dict() for x in range(len(df_result)) ]
        for i, d in enumerate(df_result):
            #print('%s, %s' % (i, d))
            #print(defendent_list)    
            defendent_list[i]['name'] = self._get_defendent_name(df_result[i])
            
            defendent_list[i]['age'] = self._get_defendent_age(df_result[i])
            defendent_list[i]['sex'] = self._get_defendent_sex(df_result[i])
            defendent_list[i]['nation'] = self._get_defendent_nation(df_result[i])
            defendent_list[i]['education'] = self._get_defendent_education(df_result[i])
            defendent_list[i]['job'] = self._get_defendent_job(df_result[i])
            defendent_list[i]['lawyer'] = self._get_defendent_lawyer(df_result[i])
            #defendent_list[i]['law_firm'] = self._get_defendent_law_firm(df_result[i])
        print(defendent_list)
        if defendent_list[-1]['name'] == '某某': defendent_list.pop()
        
        for i in range(len(defendent_list)):
            defendent_list[i]['charge'] = self._get_defendent_charge(defendent_list[i]['name'], cv_result)
        return defendent_list

    def analyse_doc(self):
        case_info = {}
        self.read_doc()
        self._remove_space()

        case_info['name'] = self.doc_name
        case_info['verdict'] = self._get_verdict_name()
        case_info['id'] = self._get_case_id()
        case_info['court'] = self._get_court_name(case_info['verdict'])
        case_info['prosecutor'] = self._get_prosecutor()
        case_info['year'] = self._get_year(case_info['id'])
        case_info['defendent'] = self._get_defendent_info()
        
        #print(case_info['defendent'])
        defendent_num = len(case_info['defendent'])
        output = [ dict() for x in range(defendent_num) ]
        for d in range(defendent_num):
            output[d]['file_name'] = case_info['name']
            output[d]['verdict'] = case_info['verdict']
            output[d]['id'] = case_info['id']
            output[d]['court'] = case_info['court']
            output[d]['prosecutor'] = case_info['prosecutor']
            output[d]['year'] = case_info['year']
            output[d]['d_name'] = case_info['defendent'][d]['name']
            output[d]['d_age'] = case_info['defendent'][d]['age']
            output[d]['d_sex'] = case_info['defendent'][d]['sex']
            output[d]['d_nation'] = case_info['defendent'][d]['nation']
            output[d]['d_education'] = case_info['defendent'][d]['education']
            output[d]['d_job'] = case_info['defendent'][d]['job']
            output[d]['d_lawyer'] = case_info['defendent'][d]['lawyer']
            output[d]['d_charge'] = case_info['defendent'][d]['charge']
            
        return output

        