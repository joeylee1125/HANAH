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
    def __init__(self, doc_name, year):
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
        
        
        
        self.verdict_pattern = re.compile(".*?判决书")
        self.prosecutor_pattern = re.compile('(?<=公诉机关).*?人民检察院')
        self.court_pattern = re.compile('\w+人民法院')
        self.year_pattern = re.compile('[12][09]\d{2}')
        self.judgement_pattern = re.compile('(?:判决|判处|决定)(?:结果|如下).*')
        self.charge_pattern = re.compile('(?<=犯).+?罪')
        self.accuse_pattern = re.compile('指控.*?审理终结')
        
        self.defendent_section_pattern = []
        self.defendent_section_pattern.append(re.compile('被告人?.*?(?:起诉书|指控)'))
        self.defendent_section_pattern.append(re.compile('被告人?.*?人民检察院指控'))
        self.defendent_section_pattern.append(re.compile('被告人?.*?自诉'))
        
        self.defendent_info_pattern = re.compile('被告人?.*?(?=被告人|起诉书|自诉|人民检察院指控|指控)')
        #self.defendent_c_info_pattern = re.compile('(被告人|附带民事诉讼被告人).*?(?=附带民事诉讼被告人|被告人|起诉书|自诉|人民检察院指控|指控)')
        
        
        self.convict_section_pattern = []
        self.convict_section_pattern.append(re.compile('(?<=判决如下).*如不服本判决'))
        self.convict_section_pattern.append(re.compile('(?<=判决如下).*提出上诉'))
        self.convict_section_pattern.append(re.compile('(?<=判处如下).*提出上诉'))
        self.convict_section_pattern.append(re.compile('(?<=判决结果).*如不服本判决'))
        self.convict_section_pattern.append(re.compile('(?<=判处结果).*如不服本判决'))
        self.convict_section_pattern.append(re.compile('(?<=判决如下).*审'))#审　判　长
        self.convict_section_pattern.append(re.compile('(?<=之规定).*如不服本判决'))
        self.convict_info_pattern = re.compile('被告人.*?(?=被告人|如不服本判决|提出上诉|审)')
        
        self.first_section_pattern = []
        self.first_section_pattern.append(re.compile('.*?(?=被告人)'))
        
        self.second_section_pattern = []
        self.second_section_pattern.append(re.compile('人民检察院.*?以.*?审理终结'))
        self.second_section_pattern.append(re.compile('公诉机关以.*?审理终结'))
        self.second_section_pattern.append(re.compile('人民检察院指控.*?公诉机关认为'))
        self.second_section_pattern.append(re.compile('公诉机关以.*?终结审理'))
        
        
        
        #self.last_section_pattern = []
        #self.last_section_pattern.append(re.compile('审(.+)?判(.+)?长.*书(.+)?记(.+)?员(.+)?\w{2,3}'))
        
        
        
        self.defendent_sex_pattern = re.compile('(?<=，|,)[男女](?=，|。)')
        self.defendent_nation_pattern = re.compile('(?<=，|,)' + CourtList.nation_list + '族(?=，|。)')
        self.defendent_education_pattern = re.compile(CourtList.education_list)
        self.defendent_job_pattern = re.compile(CourtList.job_list)

        self.defendent_prison_pattern = []
        self.defendent_prison_pattern.append(re.compile('(?<=判处).*?(?=[。，,；（])'))
        self.defendent_prison_pattern.append(re.compile('免予刑事处罚'))
        self.defendent_prison_pattern.append(re.compile('免于刑事处罚'))
        self.defendent_prison_pattern.append(re.compile('(?<=判).*?(?=[。，,；（])'))
        self.defendent_prison_pattern.append(re.compile('无罪'))
        
        self.defendent_fine_pattern = []
        self.defendent_fine_pattern.append(re.compile('(?<=罚金).*?(?=元)'))
        
        self.defendent_probation_pattern = []
        self.defendent_probation_pattern.append(re.compile('缓刑.*?(?=[。，,；])'))
        self.defendent_probation_pattern.append(re.compile('缓期.*?执行'))
        
        
        self.defendent_lawyer_pattern = []
        self.defendent_lawyer_pattern.append(re.compile('(?<!指定|指派)辩护人.*?(?:事务所|法律援助中心|分所)律师'))
        self.defendent_lawyer_pattern.append(re.compile('(?<!指定|指派)辩护人\w{3}'))
        
        self.defendent_s_lawyer_pattern = []
        self.defendent_s_lawyer_pattern.append(re.compile('(?<=指定|指派)辩护人.*?(?:事务所|法律援助中心|分所)律师'))
        self.defendent_s_lawyer_pattern.append(re.compile('(?<=指定|指派)辩护人\w{3}'))
        
        
        self.defendent_law_firm_pattern = re.compile('(?<=辩护人).*?事务所律师')
        
        self.defendent_pattern = []
        self.defendent_pattern.append(re.compile('(?<=被告人).+?[，,（(。]'))
        #self.defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.last_name + '\w{1,3}(?=[。，,（(]|201|犯)'))
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

        
    def _remove_space(self):
        self.content = self.content.replace(' ', '')
        #print(self.content)

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
        #print(self.first_sec)
        for p in self.case_id_pattern:
            case_id = self._search(p, self.first_sec)
            if case_id: 
                return case_id
        else:
            return None
        
    def _get_verdict_name(self):
        return self._search(self.verdict_pattern, self.first_sec)

    def _get_court_name(self):
        return self._search(self.court_pattern, self.first_sec)
        
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
        else:
            return '基层'    
        
    def _get_prosecutor(self):
        return self._search(self.prosecutor_pattern, self.first_sec)
    
    def _get_procedure(self):
        p = self._search('普通程序')
        if not p:
            p = self._search('简易程序')
        
        if not p:
            return '普通程序'
        else:
            return p
    
    def _get_judgement(self):
        return self._search(self.judgement_pattern)

    def _get_accuse_section(self):
        return self._search(self.accuse_pattern)

    def _get_charge(self, defendent):
        # print(judgement_section)
        # return self._search(self.charge_pattern, judgement_section)
        return self._search('(?<=被告人' + defendent + '犯).+?罪', self.judgement_section)
        
    def _get_charge_class(self, charge):
        for g in CourtList.zm_group_list[:-1]:
            if charge in CourtList.zm_group[g]:
                return CourtList.zm_group_name[g]
        else:
            return CourtList.zm_group_name['qt_list']

        
    def _get_year(self, id):
        #print(self.last_sec)
        #self.year = self._search(self.year_pattern, id)
        #TODO:   This is hard code to receive command line parameter
        return self.year

    def _get_section(self):
        for p in self.defendent_section_pattern:
            defendent_section = self._search(p, self.content)
            if defendent_section: break
        else:
            print("warning -----------------> no defendent section found by %s" % self.defendent_section_pattern)
            print(self.doc_name)
            print(self.content)
        #print(defendent_section)
        self.df_sec = defendent_section
    
        for p in self.convict_section_pattern:
            convict_section = self._search(p, self.content)
            if convict_section: break
        else:
            print("warning -----------------> no convict section found by %s" % self.convict_section_pattern)
            print(self.doc_name)
            print(self.content)
        #print(convict_section)
        
        self.cv_sec = convict_section
        
        for p in self.first_section_pattern:
            first_section = self._search(p, self.content)
            if first_section: break
        #print(first_section)
        self.first_sec = first_section
        
        for p in self.second_section_pattern:
            second_section = self._search(p, self.content)
            if second_section: break
        else:
            print(self.doc_name)
            print('<--------------------2 Section NOT FOUND------------------------>')
            print('')
            print('')
        #print(second_section)
        self.second_sec = second_section
        
        
        #for p in self.last_section_pattern:
        #    last_section = self._search(p, self.content)
        #    if last_section: break
        #print(last_section)
        #self.last_sec = last_section
            
    def _get_defendent_name(self, context):
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
        #else:
        #    d = re.search(self.defendent_pattern[0], context)
        if d: 
            return d.group()
        else:
            return None
        
    def _get_defendent_age(self, df_sec):
        if not self.year:
            return None
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
        if education == '不识字': 
            return '文盲'
        return education

    def _get_defendent_job(self, df_sec):
        job = self._search(self.defendent_job_pattern, df_sec)
        if job == '务农' or job == '粮农' or job == '农村居民':
            return '农民'
        elif job == '修理工' or job == '驾驶员' or job == '工作人员':
            return '职工'
        elif job == '无职业':
            return '无业'
        elif job == '务工人员':
            return '个体'
        return job
    
    def _get_defendent_lawyer(self, df_sec):
        #print(df_sec)
        for p in self.defendent_lawyer_pattern:
            lawyer_list = re.findall(p, df_sec)
            if lawyer_list: break
        else:
            return None
        return lawyer_list
    
    def _get_defendent_s_lawyer(self, df_sec):
        #print(df_sec)
        for p in self.defendent_s_lawyer_pattern:
            s_lawyer_list = re.findall(p, df_sec)
            if s_lawyer_list: break
        else:
            return None
        return s_lawyer_list
        
    def _get_defendent_law_firm(self, df_sec):    
        law_firm_list = re.findall(self.defendent_law_firm_pattern, df_sec)
        return law_firm_list
    
    def _get_defendent_charge(self, d_name, cv_result):
        charge = None
        for cv in cv_result:
            #print("Search %s in %s" % (d_name, cv))
            if re.search(d_name, cv):
                charge = re.search('(?<=犯).*?(?=罪)', cv)
                if charge: break
            else:
                for g in CourtList.zm_group_list:
                    for c in CourtList.zm_group[g]:
                        charge = re.search(c, cv)
                    if charge: break                
        
        if charge:
            #print("%s ---------------> %s" % (d_name, charge.group()))
            return charge.group()
        else:
            print(self.doc_name)
            print("%s ------------------------------------------------------------------------------------------> charge NOT FOUND" % d_name)
            print(cv_result)
            print('')
            print('')
            return charge

    def _get_defendent_prison(self, d_name, cv_result):
        prison = None
        for cv in cv_result:
            # print("Search %s in %s" % (d_name, cv))
            if re.search(d_name, cv):
                for p in self.defendent_prison_pattern:
                    prison = re.search(p, cv)
                    if prison: break
            if prison: break            
        if prison:
            #print("%s ---------------> %s" % (d_name, prison.group()))
            if "罚金" in prison.group():
                return None
            return prison.group()
        else:
            print(self.doc_name)
            print("%s -----------------------------------------------------------------------------------------------> prison NOT FOUND" % d_name)
            print(cv_result)
            print('')
            print('')
            return prison
    
    def _get_number(self, text):
        number = None
        # Step 1, Remove comma.        
        t = text.replace(',', '')
        t = t.replace('，', '')
        #print(t)
        
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
        #print(n.group())
        else:
            number = n.group()
        return number
    
    def _get_defendent_fine(self, d_name, cv_result):
        fine = None
        for cv in cv_result:
            #print("Search %s in %s" % (d_name, cv))
            if re.search(d_name, cv):
                for f in self.defendent_fine_pattern:
                    fine = re.search(f, cv)
                    if fine: break
            if fine: break            
        if fine:
            #print("%s ---------------> %s" % (d_name, fine.group()))
            return self._get_number(fine.group())
        else:
            print(self.doc_name)
            print("%s -----------------------------------------------------------------------------------------------> prison NOT FOUND" % d_name)
            print(cv_result)
            print('')
            print('')
            return fine                    
            
    def _get_defendent_probation(self, d_name, cv_result):
        probation = None
        for cv in cv_result:
            #print("Search %s in %s" % (d_name, cv))
            if re.search(d_name, cv):
                for p in self.defendent_probation_pattern:
                    probation = re.search(p, cv)
                    if probation: break
            if probation: break            
        if probation:
            #print("%s ---------------> %s" % (d_name, probation.group()))
            return probation.group()
        else:
            #print(self.doc_name)
            #print("%s -----------------------------------------------------------------------------------------------> probation NOT FOUND" % d_name)
            #print(cv_result)
            #print('')
            #print('')
            return probation            
    
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
        if not duration: return None
        l = 0
        #print(duration)
        y = re.search('[一二三四五六七八九十]{1,3}(?=年)', duration)
        if y: 
            #print(y.group())
            l += int(self._trans_chinese_number(y.group())) * 12
        m = re.search('[一二三四五六七八九十]{1,3}(?=个月)', duration)
        if m: 
            #print(m.group())
            l += int(self._trans_chinese_number(m.group()))
        return l
    
    def _clean_defendent_result(self, df_result):
        # 如果i+1段中出现以前出现过的被告人，那么合并i+1到i并删除i+1段
        # 如果i段中没有出现被告人，那么合并i+1到i并删除i+1段
        
        #print('Before clean ----------------------------> %s'%df_result)
        j = len(df_result)
        #print(j)
        i = 0
        df_name_list = []
        while i < j:
            #print(i, j)
            #print(df_result[i])
            #print(df_name_list)
            if df_name_list:
                for dn in df_name_list:
                    #print('search %s -----------------> in %s' % (dn, df_result[i]))
                    df_search = re.search('被告人' + dn, df_result[i])
                    if df_search: break
                if not df_search:
                    df_name = self._get_defendent_name(df_result[i])
                    #print(df_name)
                    if df_name:
                        df_name_list.append(df_name)
                if df_search or not df_name:
                    #print(df_search.group())
                    df_result[i-1] += df_result[i]
                    #print(df_result[i-1])
                    df_result.pop(i)
                    j -= 1
                    i -= 1
            else:
                df_name = self._get_defendent_name(df_result[i])
                #print(df_name)
                if df_name: 
                    df_name_list.append(df_name)
                else:
                    df_result[i-1] += df_result[i]
                    df_result.pop(i)
                    j -= 1
                    i -= 1
            #print(df_name)
            #print('')
            i += 1
        #print(df_result)
        #print('')
        #for i in df_result:
        #    print(i)
        
        # Remove 附带民事 section
        #c = len(df_result)
        #print(c)
        #while c > 1:
        #    print(c)
        #    c_search = re.search('附带民事', df_result[c-2])
        #    if c_search:
        #        print('pop ---> %s' % c)
        #        df_result.pop(c-1)
        #    c -= 1
        #print('')
        #print(df_result)
        #print('After clean ----------------------------')
        #print('')
        #for i in df_result:
        #    print(i)
        return df_result
        
    
    def _get_defendent_info(self):
        if self.df_sec:
            #print(self.df_sec)
            df_result = re.findall(self.defendent_info_pattern, self.df_sec)
            #print(df_result)
            # 被告人曾宇，男，1980年12月15日出生（身份证号码：），汉族，大学文化，无业，户籍所在地：成都市成华区。
        if not df_result:
            print("warning -----------------> no defendent result found by %s" % self.defendent_info_pattern)

        if self.cv_sec:
            cv_result = re.findall(self.convict_info_pattern, self.cv_sec)
            #print(self.cv_sec)
            #print(cv_result)
            if not cv_result:
                print("warning -----------------> no convict result found by %s" % self.convict_info_pattern)  
                #print(self.cv_sec)
        
        df_result = self._clean_defendent_result(df_result)
        #print(df_result)
        
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
                defendent_list[i]['has_lawyer'] = 'no'
                
        #j = len(defendent_list)
        #i = 0
        #while i < j: 
        #    #print(i,j)
        #    if defendent_list[i]['name'] == '某某' or defendent_list[i]['name'] == None:
        #        defendent_list.pop(i)
        #        j -= 1
        #        i -= 1
        #    i += 1
        #print(defendent_list)
        
        
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
        case_info = {}
        self.read_doc()
        self._remove_space()
        self._get_section()
        

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
                    

        #print(case_info['defendent'])
        defendent_num = len(case_info['defendent'])
        output = [ dict() for x in range(defendent_num) ]
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
        return output