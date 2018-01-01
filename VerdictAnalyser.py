# -*- coding: UTF-8 -*-
import csv
import re
import sys
import logging
import os
# import time
# import codecs
# from datetime import date, datetime

# from shutil import copyfile
from docx import Document
from docx.opc.exceptions import PackageNotFoundError
import CourtList


class VerdictAnalyser:
    def __init__(self, doc_name=None, year=2016):
        self.accuse_section = ''
        self.content = ''
        self.year = year
        self.df_sec = ''
        self.cv_sec = ''
        self.last_sec = ''
        self.first_sec = ''
        self.second_sec = ''
        self.doc_name = doc_name
        self.case_id_pattern = []
        self.case_id_pattern.append(re.compile('[(（]\d\d\d\d[）)].*?号'))
        self.case_id_pattern.append(re.compile('[(（]\d\d\d\d[）)][\w\d]+[初]([字第]+)?[\d]+'))
        self.case_id_pattern.append(re.compile('\d{4}[\w\d]+[初]([字第]+)?[\d]+号'))
        self.defendent_bail_pattern = re.compile('取保候审')
        self.verdict_pattern = list()
        self.verdict_pattern.append(re.compile(".*?判决书"))
        self.prosecutor_pattern = list()
        self.prosecutor_pattern.append(re.compile('(?<=公诉机关).*?人民检察院'))
        self.court_pattern = list()
        self.court_pattern.append(re.compile('\w+人民法院'))
        self.year_pattern = re.compile('[12][09]\d{2}')
        self.defendent_charge_pattern = re.compile('(?<=犯).*?(?!犯罪).罪')
        self.defendent_section_pattern = []
        self.defendent_section_pattern.append(re.compile('被告人?.*?(?:起诉书|指控)'))
        self.defendent_section_pattern.append(re.compile('被告人?.*?人民检察院指控'))
        self.defendent_section_pattern.append(re.compile('被告人?.*?自诉'))
        self.defendent_info_pattern = list()
        self.defendent_info_pattern.append(re.compile('被告人?.*?(?=被告人|起诉书|自诉|人民检察院指控|指控)'))
        self.convict_section_pattern = []
        self.convict_section_pattern.append(re.compile('(?<=判决如下).*如不服本判决'))
        self.convict_section_pattern.append(re.compile('(?<=判决如下).*提出上诉'))
        self.convict_section_pattern.append(re.compile('(?<=判处如下).*提出上诉'))
        self.convict_section_pattern.append(re.compile('(?<=判决结果).*如不服本判决'))
        self.convict_section_pattern.append(re.compile('(?<=判处结果).*如不服本判决'))
        self.convict_section_pattern.append(re.compile('(?<=判决如下).*审'))  # 审　判　长
        self.convict_section_pattern.append(re.compile('(?<=之规定).*如不服本判决'))
        self.convict_info_pattern = re.compile('被告人.*?(?=被告人|如不服本判决|提出上诉|审)')
        self.first_section_pattern = []
        self.first_section_pattern.append(re.compile('.*?(?=被告人)'))
        self.second_section_pattern = []
        self.second_section_pattern.append(re.compile('人民检察院.*?以.*?审理终结'))
        self.second_section_pattern.append(re.compile('公诉机关以.*?审理终结'))
        self.second_section_pattern.append(re.compile('人民检察院指控.*?公诉机关认为'))
        self.second_section_pattern.append(re.compile('公诉机关以.*?终结审理'))
        self.defendent_sex_pattern = re.compile('(?<=[，,])[男女](?=[，。])')
        self.defendent_nation_pattern = re.compile('(?<=[，,])' + CourtList.nation_list + '族(?=[，。])')
        self.defendent_education_pattern = re.compile(CourtList.education_list)
        self.defendent_job_pattern = re.compile(CourtList.job_list)


        # self.defendent_prison_pattern = []
        # self.defendent_prison_pattern.append(re.compile('(?<=判处).*?(?=[。，,；(（])'))
        # self.defendent_prison_pattern.append(re.compile('免予刑事处罚'))
        # self.defendent_prison_pattern.append(re.compile('免于刑事处罚'))
        # self.defendent_prison_pattern.append(re.compile('(?<=判)(!决).*?(?=[。，,；(（])'))
        # self.defendent_prison_pattern.append(re.compile('无罪'))

        self.defendent_prison_pattern = []
        #self.defendent_prison_pattern.append(re.compile('有期徒刑.*?(?=[。，,；(（])'))
        #self.defendent_prison_pattern.append(re.compile('拘役.*?(?=[。，,；(（;])'))
        self.defendent_prison_pattern.append(re.compile('有期徒刑.{1,6}月'))
        self.defendent_prison_pattern.append(re.compile('有期徒刑.{1,3}年'))
        self.defendent_prison_pattern.append(re.compile('拘役.{1,5}月'))
        self.defendent_prison_pattern.append(re.compile('拘役.年'))
        #self.defendent_prison_pattern.append(re.compile('管制.*?(?=[。，,；(（;])'))
        self.defendent_prison_pattern.append(re.compile('管制.{1,5}月'))
        self.defendent_prison_pattern.append(re.compile('管制.年'))
        self.defendent_prison_pattern.append(re.compile('免[予于]刑事处罚'))
        self.defendent_prison_pattern.append(re.compile('无期徒刑.*?(?=[。，,；(（])'))
        self.defendent_prison_pattern.append(re.compile('死刑.*?(?=[。，,；(（])'))
        self.defendent_prison_pattern.append(re.compile('无罪'))
        self.defendent_prison_pattern.append(re.compile('(?<=判)(!决).*?(?=[。，,；(（])'))


        self.defendent_fine_pattern = []
        self.defendent_fine_pattern.append(re.compile('(?<=罚金).*?(?=元)'))
        self.defendent_probation_pattern = []
        #self.defendent_probation_pattern.append(re.compile('缓刑.*?(?=[。，,；])'))
        self.defendent_probation_pattern.append(re.compile('缓刑.{1,5}月'))
        self.defendent_probation_pattern.append(re.compile('缓刑.年'))
        self.defendent_probation_pattern.append(re.compile('缓期.*?执行'))
        self.defendent_lawyer_pattern = []
        self.defendent_lawyer_pattern.append(re.compile('(?<!指定|指派)辩护人.*?(?:事务所|法律援助中心|分所)(?:律师|实习律师)'))
        self.defendent_lawyer_pattern.append(re.compile('(?<!指定|指派)辩护人\w{3}'))
        self.defendent_s_lawyer_pattern = []
        self.defendent_s_lawyer_pattern.append(re.compile('(?<=指定|指派)辩护人.*?(?:事务所|法律援助中心|分所)律师'))
        self.defendent_s_lawyer_pattern.append(re.compile('(?<=指定|指派)辩护人\w{3}'))
        self.defendent_law_firm_pattern = re.compile('(?<=辩护人).*?事务所律师')
        self.defendent_pattern = []
        self.defendent_pattern.append(re.compile('(?<=被告人).+?[，,（(。]'))
        # self.defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.last_name + '\w{1,3}(?=[。，,（(]|201|犯)'))
        self.defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.last_name + '\w{1,3}(?=[。，,（(]|201)'))
        self.defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.ss_name))
        self.defendent_pattern.append(re.compile('(?<=被告人..情况姓名)' + CourtList.last_name + '\w{0,4}[，（|出生日期|性别]'))
        self.defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.last_name + '\w{0,4}(?=成都市)'))
        self.defendent_pattern.append(re.compile('(?<=被告人姓名)' + CourtList.last_name + '\w{0,4}出生日期'))
        self.defendent_pattern.append(re.compile('(?<=被告)人?[：:]?' + CourtList.last_name + '\w{0,4}(?=[。，,（(]|201)'))
        self.defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.last_name + '\w\w' + CourtList.last_name + '某某'))
        self.defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.last_name + '\w{1,2}'))
        self.defendent_pattern.append(re.compile(CourtList.invalid_name))
        self.born_date_pattern = []
        self.born_date_pattern.append(re.compile('(\d\d\d\d)年(\d{1,2})月(\d{1,2})日出?生'))
        self.born_date_pattern.append(re.compile('生于(\d\d\d\d)年(\d{1,2})月(\d{1,2})日'))
        self.fieldnames = ['file_name', 'verdict', 'id', 'court', 'region', 'court_level', 'prosecutor',
                           'procedure', 'year', 'd_name', 'd_age', 'd_sex', 'd_nation', 'd_education',
                           'd_job', 'd_lawyer', 'd_lawyer_n', 'd_s_lawyer', 'd_s_lawyer_n', 'd_has_lawyer',
                           'd_charge', 'd_charge_c', 'd_prison', 'd_prison_l', 'd_probation', 'd_probation_l',
                           'd_fine', 'd_bail']
        self._init_log()

    def __del__(self):
        self.logger.removeHandler(self.ch)

    def _init_log(self):
        # Create logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        self.ch = logging.StreamHandler()
        #self.ch.setLevel(logging.DEBUG)
        # self.ch.setLevel(logging.INFO)
        self.ch.setLevel(logging.WARNING)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        self.ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(self.ch)

    def _remove_space(self):
        self.content = self.content.replace(' ', '')


    def dump2csv(self, results, folder_name):
        file = folder_name + 'report.csv'
        self.logger.info("dump to csv".format(file))
        with open(file, 'w', newline='', encoding='utf-8_sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            for r in results:
                writer.writerow(r)


    def _read_doc(self):
        if 'txt' in self.doc_name:
            try:
                with open(self.doc_name, 'r') as txt_file:
                    self.content = txt_file.read()
            except Exception as e:
                self.logger.info("Failed load file {} with error {}".format(self.doc_name, e))
        else:
            try:
                document = Document(self.doc_name) if self.doc_name else sys.exit(0)
                l = [paragraph.text for paragraph in document.paragraphs]
                self.content = ''.join(str(e) for e in l)
            except PackageNotFoundError:
                print("Document %s is invalid" % self.doc_name)


    def _findall_by_mul_pattern(self, pattern_list, content):
        # search pattern in content and return match section.
        for p in pattern_list:
            section_list = re.findall(p, content)
            if section_list: break
        else:
            self.logger.info("No section list found by {} in {}".format(pattern_list, content))
        self.logger.debug("Found {}".format(section_list))
        return section_list


    def _search_by_mul_pattern(self, pattern_list, content):
        # search pattern in content and return match section.
        for p in pattern_list:
            section = self._search(p, content)
            if section: break
        else:
            self.logger.info("No section found by {} in {}".format(pattern_list, content))
        self.logger.debug("Found {}".format(section))
        return section


    def _search(self, pattern, text=None):
        if text is None:
            text = self.content
        result = re.search(pattern, text)
        return result.group() if result is not None else None


    def _get_case_id(self):
        self.logger.debug("Search case id by {} in {}".format(self.case_id_pattern, self.first_sec))
        return self._search_by_mul_pattern(self.case_id_pattern, self.first_sec)


    def _get_verdict_name(self):
        self.logger.debug("Search verdict name by {} in {}".format(self.verdict_pattern, self.first_sec))
        return self._search_by_mul_pattern(self.verdict_pattern, self.first_sec)

    def _get_court_name(self):
        self.logger.debug("Search court name by {} in {}".format(self.court_pattern, self.first_sec))
        return self._search_by_mul_pattern(self.court_pattern, self.first_sec)

    def _get_region(self, court_name):
        if not court_name:
            return None
        for k in CourtList.court_list:
            for court in CourtList.court_list[k]:
                if court in court_name:
                    return CourtList.court_trans[k]
        else:
            return None

    def _get_court_level(self, court_name):
        if not court_name:
            return None
        if '中级' in court_name:
            return '中级'
        elif '高级' in court_name:
            return '高级'
        else:
            return '基层'

    def _get_prosecutor(self):
        self.logger.debug("Search prosecutor id by {} in {}".format(self.prosecutor_pattern, self.first_sec))
        return self._search_by_mul_pattern(self.prosecutor_pattern, self.first_sec)

    def _get_procedure(self):
        if self._search('简易程序'):
            return '简易程序'
        else:
            return '普通程序'


    def _get_charge_class(self, charge):
        for g in CourtList.zm_group_list[:-1]:
            if charge in CourtList.zm_group[g]:
                return CourtList.zm_group_name[g]
        else:
            return CourtList.zm_group_name['qt_list']

    def _get_year(self, id):
        # TODO:   Receive year from command line, update to get it from doc later.
        return self.year


    def _get_all_section(self):
        self.df_sec = self._search_by_mul_pattern(self.defendent_section_pattern, self.content)
        self.cv_sec = self._search_by_mul_pattern(self.convict_section_pattern, self.content)
        self.first_sec = self._search_by_mul_pattern(self.first_section_pattern, self.content)
        # self.second_sec = self._search_by_mul_pattern(self.second_section_pattern, self.content)

    def _get_defendent_name(self, context):
        self.logger.debug("Get defendent name in {}".format(context))
        for i, p in enumerate(self.defendent_pattern[1:]):
            d = re.search(p, context)
            if d:
                # used to solve issue 被告人：王某轩 and 人：王某轩.
                if i == 5:
                    d = re.search(CourtList.last_name + '\w{0,4}', d.group())
                    break
                # used to solve issue 被告人邓运华邓某某.    
                if i == 6:
                    d = re.search(CourtList.last_name + '\w\w', d.group())
                    break
                else:
                    break
        # else:
        #    d = re.search(self.defendent_pattern[0], context)
        if d:
            self.logger.debug("Defendent name found {}".format(d.group()))
            return d.group()
        else:
            return None

    def _get_defendent_age(self, df_sec):
        for p in self.born_date_pattern:
            self.logger.debug("Search defendent born date by {} in {}".format(self.born_date_pattern, df_sec))
            born_date = re.search(p, df_sec)
            if born_date: break
        else:
            self.logger.info("Born year not found.")
            return None
        born_year = born_date.group(1)
        age = int(self.year) - int(born_year)
        return age

    def _get_defendent_sex(self, df_sec):
        self.logger.debug("Search defendent sex by {} in {}".format(self.defendent_sex_pattern, df_sec))
        return self._search(self.defendent_sex_pattern, df_sec)


    def _get_defendent_nation(self, df_sec):
        self.logger.debug("Search defendent nation by {} in {}".format(self.defendent_nation_pattern, df_sec))
        return self._search(self.defendent_nation_pattern, df_sec)


    def _get_defendent_education(self, df_sec):
        self.logger.debug("Search defendent education by {} in {}".format(self.defendent_education_pattern, df_sec))
        education = self._search(self.defendent_education_pattern, df_sec)
        if education == '不识字':
            return '文盲'
        if education == '专科':
            return '中专'
        return education

    def _get_defendent_job(self, df_sec):
        self.logger.debug("Search defendent job by {} in {}".format(self.defendent_job_pattern, df_sec))
        job = self._search(self.defendent_job_pattern, df_sec)
        if job == '务农' or job == '粮农' or job == '农村居民':
            return '农民'
        elif job == '修理工' or job == '驾驶员' or job == '工作人员' or job == '教师':
            return '职工'
        elif job == '无职业':
            return '无业'
        elif job == '务工人员':
            return '个体'
        return job

    def _get_defendent_lawyer(self, df_sec):
        self.logger.debug("Search defendent lawyer by {} in {}".format(self.defendent_lawyer_pattern, df_sec))
        return self._findall_by_mul_pattern(self.defendent_lawyer_pattern, df_sec)


    def _get_defendent_s_lawyer(self, df_sec):
        self.logger.debug("Search defendent specified lawyer by {} in {}".format(self.defendent_s_lawyer_pattern, df_sec))
        return self._findall_by_mul_pattern(self.defendent_s_lawyer_pattern, df_sec)

    def _get_defendent_bail(self, df_sec):
        self.logger.debug("Search defendent bail by {} in {}".format(self.defendent_bail_pattern, df_sec))
        return self._search(self.defendent_bail_pattern, df_sec)

    def _clean_defendent_charge(self, d_list, cv_list):
        d_name = list()
        for idx in range(len(d_list)):
            d_name.append(d_list[idx]['name'])
        # 如果i段中出现一个以上被告人，删除i，被告人成组出现不处理
        i = 0
        j = len(cv_list)
        while i < j:
            sc = 0
            for d in d_name:
              if re.search(d, cv_list[i]):
                  sc += 1
            if sc != 1:
                cv_list.pop(i)
                j -= 1
            else:
                i += 1

        # 如果i+1段中没有出现被告人或被告人在i段中出现，那么合并i+1到i并删除i+1段
        for d in d_name:
            j = len(cv_list)
            i = 0
            while i < (j - 1):
                if re.search(d, cv_list[i]) and re.search(d, cv_list[i + 1]):
                    cv_list[i] += cv_list[i + 1]
                    cv_list.pop(i + 1)
                    j -= 1
                else:
                    i += 1
        return cv_list


    def _get_defendent_charge(self, d_name, cv_result):
        charge = None
        for cv in cv_result:
            if re.search(d_name, cv):
                charge = re.search('(?<=犯).*?(?!犯罪).(?=罪)', cv)
                if charge:
                    self.logger.debug("Defendent {} is charged by {}".format(d_name, charge.group()))
                    return charge.group()
                else:
                    for g in CourtList.zm_group_list:
                        for c in CourtList.zm_group[g]:
                            charge = re.search(c, cv)
                    if charge:
                        self.logger.debug("Defendent {} 犯.*罪 is not found, {} is found.".format(d_name, charge))
                        return charge
        else:
            self.logger.info("Charge is not found in {} for {}".format(cv_result, d_name))
            return None

    def _get_defendent_prison(self, d_name, cv_result):
        prison = None
        for cv in cv_result:
            if re.search(d_name, cv):
                self.logger.debug("Search defendent prison by {} in {}".format(self.defendent_prison_pattern, cv))
                prison = self._search_by_mul_pattern(self.defendent_prison_pattern, cv)
            if prison:
                # 如果匹配出罚金则没有匹配到犯罪类型。
                # e.g. 判处罚金
                if "罚金" in prison:
                    return None
                else:
                    return prison
        else:
            self.logger.info("Prison not found for {}".format(d_name))
            return None

    def _get_number(self, text):
        number = None
        # Step 1, Remove comma.        
        t = text.replace(',', '')
        t = t.replace('，', '')
        # print(t)

        # Step 2, Retrun number
        n = re.search('[0-9]+', t)
        if not n:
            cn = re.search('([一二三四五六七八九十][千万])+', t)
            if cn:
                c_value = re.search('[千万]', cn.group())
                c_number = re.search('[一二三四五六七八九十]', cn.group())
                if c_value.group() == '千':
                    number = self._trans_chinese_number(c_number.group()) * 1000
                elif c_value.group() == '万':
                    number = self._trans_chinese_number(c_number.group()) * 10000
                else:
                    print(cn)
        # print(n.group())
        else:
            number = n.group()
        return number

    def _get_defendent_fine(self, d_name, cv_result):
        for cv in cv_result:
            if re.search(d_name, cv):
                for f in self.defendent_fine_pattern:
                    self.logger.debug(
                        "Search defendent fine by {} in {}".format(f, cv))
                    fine = re.search(f, cv)
                    if fine:
                        return self._get_number(fine.group())
        else:
            self.logger.debug("Fine is not found for {} in {}".format(d_name, cv_result))
            return None

    def _get_defendent_probation(self, d_name, cv_result):
        for cv in cv_result:
            if re.search(d_name, cv):
                for p in self.defendent_probation_pattern:
                    self.logger.debug(
                        "Search defendent probation by {} in {}".format(p, cv))
                    probation = re.search(p, cv)
                    if probation:
                        return probation.group()
        else:
            self.logger.debug("Probation is not found for {} by {} in {}".format(d_name, self.defendent_probation_pattern, cv_result))
            return None

    def _trans_chinese_number(self, number):
        if number == '一': return 1
        if number == '二': return 2
        if number == '三': return 3
        if number == '四': return 4
        if number == '五': return 5
        if number == '六': return 6
        if number == '七': return 7
        if number == '八': return 8
        if number == '九': return 9
        if number == '十': return 10
        if number == '十一': return 11
        if number == '十二': return 12
        if number == '十三': return 13
        if number == '十四': return 14
        if number == '十五': return 15
        if number == '十六': return 16
        if number == '一六': return 16
        if number == '十七': return 17
        if number == '十八': return 18
        if number == '十九': return 19
        if number == '二十': return 20
        if number == '二十一': return 21
        if number == '二十二': return 22
        if number == '二十三': return 23
        if number == '二十四': return 24
        if number == '二十五': return 25
        if number == '二十六': return 26
        if number == '二十七': return 27
        if number == '二十八': return 28
        if number == '二十九': return 29
        if number == '三十': return 30
        return None

    def _get_len(self, duration):
        if duration is None: return None
        l = 0
        self.logger.debug("Translate {}".format(duration))
        y = re.search('[一二三四五六七八九十]{1,3}(?=年)', duration)
        if y:
            l += int(self._trans_chinese_number(y.group())) * 12
        else:
            y = re.search('[0-9]{1,3}(?=年)', duration)
            if y:
                l += int(y.group())
        m = re.search('[一二三四五六七八九十]{1,3}(?=个月)', duration)
        if m:
            l += int(self._trans_chinese_number(m.group()))
        else:
            m = re.search('[0-9]{1,3}(?=个月)', duration)
            if m:
                l += int(m.group())
        return l

    def _clean_defendent_result(self, df_result):
        # 如果i+1段中出现以前出现过的被告人，那么合并i+1到i并删除i+1段
        # 如果i段中没有出现被告人，那么合并i+1到i并删除i+1段

        self.logger.debug('Before clean, defenent list is {}'.format(df_result))
        j = len(df_result)
        i = 0
        df_name_list = []
        while i < j:
            if df_name_list:
                for dn in df_name_list:
                    self.logger.debug('search {} in {}'.format(dn, df_result[i]))
                    df_search = re.search('被告人' + dn, df_result[i])
                    if df_search:
                        self.logger.debug("Exist Name {} is found in {}".format(dn, df_result[i]))
                        break
                else:
                    df_name = self._get_defendent_name(df_result[i])
                    if df_name:
                        self.logger.debug("Name {} is found in {}".format(df_name, df_result[i]))
                        df_name_list.append(df_name)
                if df_search or not df_name:
                    df_result[i - 1] += df_result[i]
                    df_result.pop(i)
                    j -= 1
                    i -= 1
            else:
                df_name = self._get_defendent_name(df_result[i])
                if df_name:
                    self.logger.debug("Name {} is found in {}".format(df_name, df_result[i]))
                    df_name_list.append(df_name)
                else:
                    df_result[i - 1] += df_result[i]
                    df_result.pop(i)
                    j -= 1
                    i -= 1
            i += 1
        return df_result

    def _get_defendent_info(self):
        df_result = None
        if self.df_sec:
            self.logger.debug(
                "Find defendent info pattern {} in defendent section {}".
                format(self.defendent_info_pattern, self.df_sec))
            df_result = self._findall_by_mul_pattern(self.defendent_info_pattern, self.df_sec)
            self.logger.debug("Defendent info is {}".format(df_result))
        if df_result is None:
            self.logger.info("No defendent result found by %s" % self.defendent_info_pattern)
            return None
        df_result = self._clean_defendent_result(df_result)

        if self.cv_sec:
            self.logger.debug(
                "Find convict pattern {} in convict section {}".format(self.convict_info_pattern, self.cv_sec))
            cv_result = re.findall(self.convict_info_pattern, self.cv_sec)
            self.logger.debug("Found {}".format(cv_result))
            if not cv_result:
                self.logger.info("No convict result found by {}".format(self.convict_info_pattern))



        defendent_list = [dict() for x in range(len(df_result))]
        for i, d in enumerate(df_result):
            self.logger.debug("No.{} defendent info is {}".format(i, d))
            defendent_list[i]['name'] = self._get_defendent_name(d)
            defendent_list[i]['age'] = self._get_defendent_age(d)
            defendent_list[i]['sex'] = self._get_defendent_sex(d)
            defendent_list[i]['nation'] = self._get_defendent_nation(d)
            defendent_list[i]['education'] = self._get_defendent_education(d)
            defendent_list[i]['job'] = self._get_defendent_job(d)
            defendent_list[i]['lawyer'] = self._get_defendent_lawyer(d)
            defendent_list[i]['s_lawyer'] = self._get_defendent_s_lawyer(d)
            defendent_list[i]['bail'] = self._get_defendent_bail(d)

            if defendent_list[i]['lawyer']:
                defendent_list[i]['lawyer_n'] = len(defendent_list[i]['lawyer'])
            else:
                defendent_list[i]['lawyer_n'] = None
            if defendent_list[i]['s_lawyer']:
                defendent_list[i]['s_lawyer_n'] = len(defendent_list[i]['s_lawyer'])
            else:
                defendent_list[i]['s_lawyer_n'] = None

            if defendent_list[i]['lawyer_n'] == None and defendent_list[i]['s_lawyer_n'] == None:
                defendent_list[i]['has_lawyer'] = 'no'
            else:
                defendent_list[i]['has_lawyer'] = 'yes'

        if cv_result:
            cv_result = self._clean_defendent_charge(defendent_list, cv_result)

        for i in range(len(defendent_list)):
            defendent_list[i]['charge'] = self._get_defendent_charge(defendent_list[i]['name'], cv_result)
            defendent_list[i]['charge_c'] = self._get_charge_class(defendent_list[i]['charge'])
            defendent_list[i]['prison'] = self._get_defendent_prison(defendent_list[i]['name'], cv_result)
            defendent_list[i]['prison_l'] = self._get_len(defendent_list[i]['prison'])
            defendent_list[i]['probation'] = self._get_defendent_probation(defendent_list[i]['name'], cv_result)
            defendent_list[i]['probation_l'] = self._get_len(defendent_list[i]['probation'])
            defendent_list[i]['fine'] = self._get_defendent_fine(defendent_list[i]['name'], cv_result)

        return defendent_list

    def analyse_doc(self):
        case_info = dict()
        self._read_doc()
        self._remove_space()
        self._get_all_section()

        case_info['name'] = self.doc_name
        case_info['verdict'] = self._get_verdict_name()
        case_info['id'] = self._get_case_id()
        case_info['court'] = self._get_court_name()
        case_info['region'] = self._get_region(case_info['court'])
        case_info['court_level'] = self._get_court_level(case_info['court'])
        case_info['prosecutor'] = self._get_prosecutor()
        case_info['procedure'] = self._get_procedure()
        case_info['year'] = self._get_year(case_info['id'])
        case_info['defendent'] = self._get_defendent_info()

        # print(case_info['defendent'])
        defendent_num = len(case_info['defendent'])
        output = [dict() for x in range(defendent_num)]
        for d in range(defendent_num):
            output[d]['file_name'] = case_info['name']
            output[d]['verdict'] = case_info['verdict']
            output[d]['id'] = case_info['id']
            output[d]['court'] = case_info['court']
            output[d]['region'] = case_info['region']
            output[d]['court_level'] = case_info['court_level']
            output[d]['prosecutor'] = case_info['prosecutor']
            output[d]['procedure'] = case_info['procedure']
            output[d]['year'] = case_info['year']
            output[d]['d_name'] = case_info['defendent'][d]['name']
            output[d]['d_age'] = case_info['defendent'][d]['age']
            output[d]['d_sex'] = case_info['defendent'][d]['sex']
            output[d]['d_nation'] = case_info['defendent'][d]['nation']
            output[d]['d_education'] = case_info['defendent'][d]['education']
            output[d]['d_job'] = case_info['defendent'][d]['job']
            output[d]['d_lawyer'] = case_info['defendent'][d]['lawyer']
            output[d]['d_lawyer_n'] = case_info['defendent'][d]['lawyer_n']
            output[d]['d_s_lawyer'] = case_info['defendent'][d]['s_lawyer']
            output[d]['d_s_lawyer_n'] = case_info['defendent'][d]['s_lawyer_n']
            output[d]['d_has_lawyer'] = case_info['defendent'][d]['has_lawyer']
            output[d]['d_charge'] = case_info['defendent'][d]['charge']
            output[d]['d_charge_c'] = case_info['defendent'][d]['charge_c']
            output[d]['d_prison'] = case_info['defendent'][d]['prison']
            output[d]['d_prison_l'] = case_info['defendent'][d]['prison_l']
            output[d]['d_probation'] = case_info['defendent'][d]['probation']
            output[d]['d_probation_l'] = case_info['defendent'][d]['probation_l']
            output[d]['d_fine'] = case_info['defendent'][d]['fine']
            output[d]['d_bail'] = case_info['defendent'][d]['bail']
        self.logger.debug("Output of case {} is {}".format(self.doc_name, output))
        return output


class VerdictAnalyser2(VerdictAnalyser):
    def __init__(self, doc_name, year):
        super().__init__(doc_name, year)

        self.prosecutor_pattern = list()
        self.prosecutor_pattern.append(re.compile('(?<=公诉机关).*?人民检察院'))

        # 上诉人（原审被告人）
        self.defendent_section_pattern = list()
        self.defendent_section_pattern.append(re.compile('上诉人.*?(?:人民法院审理)'))
        self.defendent_section_pattern.append(re.compile('上诉人.*?(?:人民法院)'))

        self.defendent_pattern = list()
        self.defendent_pattern.append(re.compile('(?<=被告人).+?[，,（(。]'))
        self.defendent_pattern.append(re.compile('(?<=上诉人（原审被告人）)' + CourtList.last_name + '\w{1,3}(?=[。，,（(]|201)'))
        self.defendent_pattern.append(re.compile('(?<=上诉人\(原审被告人\))' + CourtList.last_name + '\w{1,3}(?=[。，,（(]|201)'))

        self.convict_info_pattern = list()
        self.convict_info_pattern.append(re.compile('(?<=上诉人（原审被告人）).*?(?=上诉人)'))
        self.convict_info_pattern.append(re.compile('(?<=上诉人\(原审被告人\)).*?(?=上诉人)'))

        self.defendent_info_pattern = list()
        self.defendent_info_pattern.append(re.compile('上诉人[（\(]原审被告人[）\)].*?(?=原审被告人|人民法院审理|上诉人)'))
        self.defendent_info_pattern.append(re.compile('上诉人[（\(]原审被告人[）\)].*?(?=原审被告人|人民法院|上诉人)'))

        self.convict_section_pattern = list()
        self.convict_section_pattern.append(re.compile('(?<=判决如下).*审(.+)?判(.+)?长'))

        self.fieldnames = ['file_name', 'verdict', 'id', 'court', 'region', 'court_level', 'prosecutor', 'procedure',
                           'year', 'd_name', 'd_age', 'd_sex', 'd_nation', 'd_education', 'd_job', 'd_lawyer',
                           'd_lawyer_n', 'd_s_lawyer', 'd_s_lawyer_n', 'd_has_lawyer', 'd_charge', 'd_charge_c',
                           'd_prison', 'd_prison_l', 'd_probation', 'd_probation_l', 'd_fine', 'd_withdraw']

    def _get_all_section(self):
        self.df_sec = self._search_by_mul_pattern(self.defendent_section_pattern, self.content)
        self.first_sec = self._search_by_mul_pattern(self.first_section_pattern, self.content)
        c = re.split('判决如下', self.content)
        cv_section = re.search('.*审(.+)?判(.+)?长', c[-1])
        self.cv_sec = cv_section.group()

    def _get_defendent_info(self):
        if self.df_sec:
            self.logger.debug(
                "Find defendent info pattern {} in defendent section {}".format(self.defendent_info_pattern,
                                                                                self.df_sec))
            df_result = self._findall_by_mul_pattern(self.defendent_info_pattern, self.df_sec)
            self.logger.debug("Defendent info is {}".format(df_result))
        if not df_result:
            self.logger.info("No defendent result found by %s" % self.defendent_info_pattern)

        if self.cv_sec:
            cv_result = re.split('上诉人', self.cv_sec)
            if not cv_result:
                print("warning -----------------> no convict result found by %s" % self.convict_info_pattern)
        print(
            '--------------------------------------------------------------------------------------------------------')
        print(cv_result)
        df_result = self._clean_defendent_result(df_result)

        defendent_list = [dict() for x in range(len(df_result))]
        for i, d in enumerate(df_result):
            # print('%s, %s' % (i, d))
            # print(defendent_list)
            defendent_list[i]['name'] = self._get_defendent_name(df_result[i])
            defendent_list[i]['age'] = self._get_defendent_age(df_result[i])
            defendent_list[i]['sex'] = self._get_defendent_sex(df_result[i])
            defendent_list[i]['nation'] = self._get_defendent_nation(df_result[i])
            defendent_list[i]['education'] = self._get_defendent_education(df_result[i])
            defendent_list[i]['job'] = self._get_defendent_job(df_result[i])
            defendent_list[i]['lawyer'] = self._get_defendent_lawyer(df_result[i])
            defendent_list[i]['s_lawyer'] = self._get_defendent_s_lawyer(df_result[i])

            if defendent_list[i]['lawyer']:
                defendent_list[i]['lawyer_n'] = len(defendent_list[i]['lawyer'])
            else:
                defendent_list[i]['lawyer_n'] = None
            if defendent_list[i]['s_lawyer']:
                defendent_list[i]['s_lawyer_n'] = len(defendent_list[i]['s_lawyer'])
            else:
                defendent_list[i]['s_lawyer_n'] = None

            if defendent_list[i]['lawyer_n'] == None and defendent_list[i]['s_lawyer_n'] == None:
                defendent_list[i]['has_lawyer'] = 'no'
            else:
                defendent_list[i]['has_lawyer'] = 'yes'
        for i in range(len(defendent_list)):
            defendent_list[i]['charge'] = self._get_defendent_charge(defendent_list[i]['name'], cv_result)
            defendent_list[i]['charge_c'] = self._get_charge_class(defendent_list[i]['charge'])
            defendent_list[i]['prison'] = self._get_defendent_prison(defendent_list[i]['name'], cv_result)
            defendent_list[i]['prison_l'] = self._get_len(defendent_list[i]['prison'])
            defendent_list[i]['probation'] = self._get_defendent_probation(defendent_list[i]['name'], cv_result)
            defendent_list[i]['probation_l'] = self._get_len(defendent_list[i]['probation'])
            defendent_list[i]['fine'] = self._get_defendent_fine(defendent_list[i]['name'], cv_result)
            defendent_list[i]['withdraw'] = self._get_defendent_withdraw(defendent_list[i]['name'], cv_result)
        return defendent_list

    def _check_protest(self):
        protest = re.search('抗诉机关', self.content)
        if protest:
            print("It's a protest case------<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            return True
        else:
            return False

    def _get_defendent_charge(self, d_name, cv_result):
        charge = None
        for cv in cv_result:
            # print("Search %s in %s" % (d_name, cv))
            if re.search('(撤销|维持)', cv):
                continue
            if re.search(d_name, cv):

                charge = re.search('(?<=犯).*(?=罪)', cv)
                if charge: break
            else:
                for g in CourtList.zm_group_list:
                    for c in CourtList.zm_group[g]:
                        charge = re.search(c, cv)
                    if charge: break

        if charge:
            # print("%s ---------------> %s" % (d_name, charge.group()))
            return charge.group()
        else:
            print(
                "%s ------------------------------------------------------------------------------------------> charge NOT FOUND" % d_name)
            print(cv_result)
            return charge

    def _get_defendent_prison(self, d_name, cv_result):
        prison = None
        for cv in cv_result:
            self.logger.debug("Search %s in %s" % (d_name, cv))
            if re.search('(撤销|维持)', cv):
                continue
            if re.search(d_name, cv):
                for p in self.defendent_prison_pattern:
                    prison = re.search(p, cv)
                    if prison: break
            if prison: break
        if prison:
            # print("%s ---------------> %s" % (d_name, prison.group()))
            if "罚金" in prison.group():
                return None
            return prison.group()
        else:
            print(self.doc_name)
            print(
                "%s -----------------------------------------------------------------------------------------------> prison NOT FOUND" % d_name)
            print(cv_result)
            print('')
            print('')
            return prison

    def _get_defendent_fine(self, d_name, cv_result):
        fine = None
        for cv in cv_result:
            # print("Search %s in %s" % (d_name, cv))
            if re.search('(撤销|维持)', cv):
                continue
            if re.search(d_name, cv):
                for f in self.defendent_fine_pattern:
                    fine = re.search(f, cv)
                    if fine: break
            if fine: break
        if fine:
            # print("%s ---------------> %s" % (d_name, fine.group()))
            return self._get_number(fine.group())
        else:
            print(self.doc_name)
            print(
                "%s -----------------------------------------------------------------------------------------------> prison NOT FOUND" % d_name)
            print(cv_result)
            print('')
            print('')
            return fine

    def _get_defendent_probation(self, d_name, cv_result):
        probation = None
        for cv in cv_result:
            # print("Search %s in %s" % (d_name, cv))
            if re.search('(撤销|维持)', cv):
                continue
            if re.search(d_name, cv):
                for p in self.defendent_probation_pattern:
                    probation = re.search(p, cv)
                    if probation: break
            if probation: break
        if probation:
            # print("%s ---------------> %s" % (d_name, probation.group()))
            return probation.group()
        else:
            # print(self.doc_name)
            # print("%s -----------------------------------------------------------------------------------------------> probation NOT FOUND" % d_name)
            # print(cv_result)
            # print('')
            # print('')
            return probation

    def _get_defendent_withdraw(self, d_name, cv_result):
        withdraw = None
        for cv in cv_result:
            if re.search('撤销', cv):
                if re.search(d_name, cv):
                    return 'yes'
        else:
            return withdraw

    def analyse_doc(self):
        case_info = dict()
        self._read_doc()
        self._remove_space()
        if self._check_protest():
            return None
        self._get_all_section()

        case_info['name'] = self.doc_name
        case_info['verdict'] = self._get_verdict_name()
        case_info['id'] = self._get_case_id()
        case_info['court'] = self._get_court_name()
        case_info['region'] = self._get_region(case_info['court'])
        case_info['court_level'] = self._get_court_level(case_info['court'])
        case_info['prosecutor'] = self._get_prosecutor()
        case_info['procedure'] = self._get_procedure()
        case_info['year'] = self._get_year(case_info['id'])
        case_info['defendent'] = self._get_defendent_info()

        defendent_num = len(case_info['defendent'])
        output = [dict() for x in range(defendent_num)]
        for d in range(defendent_num):
            output[d]['file_name'] = case_info['name']
            output[d]['verdict'] = case_info['verdict']
            output[d]['id'] = case_info['id']
            output[d]['court'] = case_info['court']
            output[d]['region'] = case_info['region']
            output[d]['court_level'] = case_info['court_level']
            output[d]['prosecutor'] = case_info['prosecutor']
            output[d]['procedure'] = case_info['procedure']
            output[d]['year'] = case_info['year']
            output[d]['d_name'] = case_info['defendent'][d]['name']
            output[d]['d_age'] = case_info['defendent'][d]['age']
            output[d]['d_sex'] = case_info['defendent'][d]['sex']
            output[d]['d_nation'] = case_info['defendent'][d]['nation']
            output[d]['d_education'] = case_info['defendent'][d]['education']
            output[d]['d_job'] = case_info['defendent'][d]['job']
            output[d]['d_lawyer'] = case_info['defendent'][d]['lawyer']
            output[d]['d_lawyer_n'] = case_info['defendent'][d]['lawyer_n']
            output[d]['d_s_lawyer'] = case_info['defendent'][d]['s_lawyer']
            output[d]['d_s_lawyer_n'] = case_info['defendent'][d]['s_lawyer_n']
            output[d]['d_has_lawyer'] = case_info['defendent'][d]['has_lawyer']
            output[d]['d_charge'] = case_info['defendent'][d]['charge']
            output[d]['d_charge_c'] = case_info['defendent'][d]['charge_c']
            output[d]['d_prison'] = case_info['defendent'][d]['prison']
            output[d]['d_prison_l'] = case_info['defendent'][d]['prison_l']
            output[d]['d_probation'] = case_info['defendent'][d]['probation']
            output[d]['d_probation_l'] = case_info['defendent'][d]['probation_l']
            output[d]['d_fine'] = case_info['defendent'][d]['fine']
            output[d]['d_withdraw'] = case_info['defendent'][d]['withdraw']
        self.logger.debug("Output of case {} is {}".format(self.doc_name, output))
        return output
