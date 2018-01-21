# -*- coding: UTF-8 -*-
import re
import logging

import StaticUtils
import FileOperations


class VerdictAnalyser:
    def __init__(self, doc_name=None, year=2016):
        self.file_name = ''
        self.dir_name = ''
        self.content = ''
        self.year = year
        self._init_log()
        self._read(doc_name)
        self._clean()

    def __repr__(self):
        return self.file_name

    def _compile_pattern(self):
        self.case_id_pattern.append(re.compile('[(（]\d\d\d\d[）)].*?号'))

    def _read(self, doc_name):
        if doc_name.endswith('docx'):
            doc = FileOperations.MyDocFile(doc_name)
        elif doc_name.endswith('txt'):
            doc = FileOperations.MyTextFile(doc_name)
        else:
            self.logger.info("Invalid document type: {}.".format(doc_name))
            return False
        self.file_name = doc.get_filename()
        self.dir_name = doc.get_dirname()
        self.content = doc.read()
        self.size = doc.get_size()
        return None

    def _clean(self):
        self._remove_space()
        self._replace_ch_symbol()

    def _replace_ch_symbol(self):
        for key, value in StaticUtils.ch_en_symbol_dict.items():
            self.content = re.sub(key, value, self.content)

    def _remove_space(self):
        self.content = re.sub('\s+', '', self.content)

    def _init_log(self):
        # Create logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        self.ch = logging.StreamHandler()
        #self.ch.setLevel(logging.DEBUG)
        #self.ch.setLevel(logging.INFO)
        self.ch.setLevel(logging.WARNING)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        self.ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(self.ch)

    def _search_by_mul_pattern(self, pattern_list, content):
        # search pattern in content and return match section.
        for p in pattern_list:
            search_results = re.search(p, content)
            if search_results:
                section = search_results.group()
                break
        else:
            self.logger.info("No section found by {} in {}".format(pattern_list, content))
            return None
        self.logger.debug("Found {}".format(section))
        return section

    def _findall_by_mul_pattern(self, pattern_list, content):
        # search pattern in content and return match section.
        for p in pattern_list:
            section_list = re.findall(p, content)
            if section_list: break
        else:
            self.logger.info("No section list found by {} in {}".format(pattern_list, content))
        self.logger.debug("Found {}".format(section_list))
        return section_list

    def divide_2_mul_sections(self):
        self.defendant_section = self._search_by_mul_pattern(StaticUtils.defendant_section_pattern, self.content)
        self.convict_section = self._search_by_mul_pattern(StaticUtils.convict_section_pattern, self.content)
        self.head_section = self._search_by_mul_pattern(StaticUtils.head_section_pattern, self.content)
        return None

    def get_verdict_name(self):
        self.logger.debug("Search verdict name by {} in {}".format(StaticUtils.verdict_pattern, self.head_section))
        return self._search_by_mul_pattern(StaticUtils.verdict_pattern, self.head_section)

    def get_case_id(self):
        self.logger.debug("Search case id by {} in {}".format(StaticUtils.case_id_pattern, self.head_section))
        return self._search_by_mul_pattern(StaticUtils.case_id_pattern, self.head_section)

    def get_court_name(self):
        self.logger.debug("Search court name by {} in {}".format(StaticUtils.court_pattern, self.head_section))
        return self._search_by_mul_pattern(StaticUtils.court_pattern, self.head_section)

    def get_region(self, court_name):
        if not court_name:
            return None
        for region in StaticUtils.court_set:
            for court in StaticUtils.court_set[region]:
                if court in court_name:
                    return StaticUtils.court_trans[region]
        else:
            return None

    def get_court_level(self, court_name):
        if not court_name:
            return None
        if '中级' in court_name:
            return '中级'
        elif '高级' in court_name:
            return '高级'
        else:
            return '基层'

    def get_prosecutor(self):
        self.logger.debug("Search prosecutor id by {} in {}".format(StaticUtils.prosecutor_pattern, self.head_section))
        return self._search_by_mul_pattern(StaticUtils.prosecutor_pattern, self.head_section)

    def get_procedure(self):
        if re.search('简易程序', self.content):
            return '简易程序'
        else:
            return '普通程序'

    def get_defendant_name(self, context):
        self.logger.debug("Get defendant name in {}".format(context))
        for i, p in enumerate(StaticUtils.defendant_pattern):
            defendant = re.search(p, context)
            if defendant:
                # used to solve issue 被告人：王某轩 and 人：王某轩.
                if i == 6:
                    defendant = re.search(StaticUtils.last_name + '\w{0,4}', defendant.group())
                    break
                # used to solve issue 被告人邓运华邓某某.
                if i == 7:
                    d = re.search(StaticUtils.last_name + '\w\w', defendant.group())
                    break
                else:
                    break
        # else:
        #    d = re.search(self.defendant_pattern[0], context)
        if defendant:
            self.logger.debug("Defendant name found {}".format(defendant.group()))
            return defendant.group()
        else:
            return None

    def get_defendant_age(self, context):
        for p in StaticUtils.born_date_pattern:
            self.logger.debug("Search defendent born date by {} in {}".format(StaticUtils.born_date_pattern, context))
            born_date = re.search(p, context)
            if born_date: break
        else:
            self.logger.info("Born year not found in {}.".format(context))
            return None
        born_year = born_date.group(1)
        age = int(self.year) - int(born_year)
        return age

    def get_defendant_nation(self, context):
        self.logger.debug("Search defendant nation by {} in {}".format(StaticUtils.defendant_nation_pattern, context))
        nation = re.search(StaticUtils.defendant_nation_pattern, context)
        return nation.group() if nation else None

    def get_defendant_education(self, context):
        self.logger.debug("Search defendant education by {} in {}".format(StaticUtils.defendant_education_pattern, context))
        education = re.search(StaticUtils.defendant_education_pattern, context)
        if education:
            if education.group() == '不识字':
                return '文盲'
            if education.group() == '专科':
                return '中专'
            return education.group()
        else:
            return None

    def get_defendant_job(self, context):
        self.logger.debug("Search defendant job by {} in {}".format(StaticUtils.defendant_job_pattern, context))
        job = re.search(StaticUtils.defendant_job_pattern, context)
        if job:
            if job.group() in ['务农', '粮农', '农村居民']:
                return '农民'
            elif job.group() in ['修理工', '驾驶员', '工作人员', '教师']:
                return '职工'
            elif job.group() in ['无职业']:
                return '无业'
            elif job.group() in ['务工人员']:
                return '个体'
            return job.group()
        else:
            return None

    def get_defendant_lawyer(self, context):
        self.logger.debug("Search defendant lawyer by {} in {}".format(StaticUtils.defendant_lawyer_pattern, context))
        return self._findall_by_mul_pattern(StaticUtils.defendant_lawyer_pattern, context)

    def get_defendant_s_lawyer(self, context):
        self.logger.debug(
            "Search defendant specified lawyer by {} in {}".format(StaticUtils.defendant_s_lawyer_pattern, context))
        return self._findall_by_mul_pattern(StaticUtils.defendant_s_lawyer_pattern, context)

    def get_defendant_bail(self, context):
        self.logger.debug("Search defendant bail by {} in {}".format(StaticUtils.defendant_bail_pattern, context))
        bail = re.search(StaticUtils.defendant_bail_pattern, context)
        return bail.group() if bail else None

    def get_defendant_sex(self, context):
        self.logger.debug("Search defendant sex by {} in {}".format(StaticUtils.defendant_sex_pattern, context))
        sex = re.search(StaticUtils.defendant_sex_pattern, context)
        return sex.group() if sex else None

    def clean_defendant_info_list(self, defendant_info_list):
        self.logger.debug('Before clean, defenent list is {}'.format(defendant_info_list))
        j = len(defendant_info_list)
        i = 0
        defendant_name_list = list()
        while i < j:
            if defendant_name_list:
                for defendant_name in defendant_name_list:
                    self.logger.debug('search {} in {}'.format(defendant_name, defendant_info_list[i]))
                    search_defendant = re.search(r"被告人?" + defendant_name, defendant_info_list[i])
                    if search_defendant:
                        self.logger.debug("Exist defendant name {} is found in {}".format(defendant_name, defendant_info_list[i]))
                        break
                else:
                    defendant_name = self.get_defendant_name(defendant_info_list[i])
                    if defendant_name:
                        self.logger.debug("Name {} is found in {}".format(defendant_name, defendant_info_list[i]))
                        defendant_name_list.append(defendant_name)
                # 如果i+1段中出现以前出现过的被告人，那么合并i+1到i并删除i+1段
                # 如果i段中没有出现被告人，那么合并i+1到i并删除i+1段
                if search_defendant or not defendant_name:
                    defendant_info_list[i - 1] += defendant_info_list[i]
                    defendant_info_list.pop(i)
                    j -= 1
                    i -= 1
            else:
                defendant_name = self.get_defendant_name(defendant_info_list[i])
                if defendant_name:
                    self.logger.debug("Name {} is found in {}".format(defendant_name, defendant_info_list[i]))
                    defendant_name_list.append(defendant_name)
                else:
                    defendant_info_list[i - 1] += defendant_info_list[i]
                    defendant_info_list.pop(i)
                    j -= 1
                    i -= 1
            i += 1
        return defendant_info_list

    def get_defendant_info_list(self):
        defendant_info_list = None
        if self.defendant_section:
            self.logger.debug(
                "Find defendant info pattern {} in defendant section {}".
                    format(StaticUtils.defendant_info_pattern, self.defendant_section))

            defendant_info_list = self._findall_by_mul_pattern(StaticUtils.defendant_info_pattern,
                                                              self.defendant_section)

            self.logger.debug("Defendant info is {}".format(defendant_info_list))
        if defendant_info_list is None:
            self.logger.info("No defendant result is found by {} in {}".format(StaticUtils.defendant_info_pattern,
                                                                               self.defendant_section))
            return None
        return self.clean_defendant_info_list(defendant_info_list)

    def get_convict_info_list(self):
        if self.convict_section:
            self.logger.debug(
                "Find convict pattern {} in convict section {}".format(StaticUtils.convict_info_pattern, self.convict_section))
            convict_info_list = re.findall(StaticUtils.convict_info_pattern, self.convict_section)
            self.logger.debug("Found {}".format(convict_info_list))
            if not convict_info_list:
                self.logger.info("No convict result found by {}".format(StaticUtils.convict_info_pattern))
            else:
                return convict_info_list

    def clean_defendant_charge(self, defendant_list, convict_info_list):
        defendant_name_list = list()
        for index in range(len(defendant_list)):
            defendant_name_list.append(defendant_list[index]['name'])
        # 如果i段中出现一个以上被告人，删除i，被告人成组出现不处理
        i = 0
        j = len(convict_info_list)
        while i < j:
            sc = 0
            for defendant_name in defendant_name_list:
                if re.search(defendant_name, convict_info_list[i]):
                    sc += 1
            if sc != 1:
                convict_info_list.pop(i)
                j -= 1
            else:
                i += 1

        # 如果i+1段中没有出现被告人或被告人在i段中出现，那么合并i+1到i并删除i+1段
        for defendant_name in defendant_name_list:
            j = len(convict_info_list)
            i = 0
            while i < (j - 1):
                if re.search(defendant_name, convict_info_list[i]) and re.search(defendant_name, convict_info_list[i + 1]):
                    convict_info_list[i] += convict_info_list[i + 1]
                    convict_info_list.pop(i + 1)
                    j -= 1
                else:
                    i += 1
        return convict_info_list

    def get_defendant_charge(self, defendant_name, convict_info_list):
        charge = None
        for convict_info in convict_info_list:
            if re.search(defendant_name, convict_info):
                charge = re.search('(?<=犯).*?(?!犯罪).(?=罪)', convict_info)
                if charge:
                    self.logger.debug("Defendant {} is charged by {}".format(defendant_name, charge.group()))
                    return charge.group()
                else:
                    for g in StaticUtils.zm_group_list:
                        for c in StaticUtils.zm_group[g]:
                            charge = re.search(c, convict_info)
                    if charge:
                        self.logger.debug("Defendant {} 犯.*罪 is not found, {} is found.".format(defendant_name, charge.group()))
                        return charge.group()
        else:
            self.logger.info("Charge is not found in {} for {}".format(convict_info_list, defendant_name))
            return None

    def get_defendant_prison(self, defendant_name, convict_info_list):
        prison = None
        for convict_info in convict_info_list:
            if re.search(defendant_name, convict_info):
                self.logger.debug("Search defendant prison by {} in {}".format(StaticUtils.defendant_prison_pattern, convict_info))
                prison = self._search_by_mul_pattern(StaticUtils.defendant_prison_pattern, convict_info)
            if prison:
                # 如果匹配出罚金则没有匹配到犯罪类型。
                # e.g. 判处罚金
                if "罚金" in prison:
                    return None
                else:
                    return prison
        else:
            self.logger.info("Prison not found for {}".format(defendant_name))
            return None

    def get_charge_class(self, charge):
        for g in StaticUtils.zm_group_list[:-1]:
            if charge in StaticUtils.zm_group[g]:
                return StaticUtils.zm_group_name[g]
        else:
            return StaticUtils.zm_group_name['qt_list']

    def trans_chinese_number(self, number):
        for key, value in StaticUtils.ch_en_number_dict.items():
            if number == key:
                return value
        else:
            return None

    def get_prison_len(self, duration):
        if duration is None:
            return None
        l = 0
        self.logger.debug("Translate {}".format(duration))
        y = re.search('[一二三四五六七八九十]{1,3}(?=年)', duration)
        if y:
            l += int(self.trans_chinese_number(y.group())) * 12
        else:
            y = re.search('[0-9]{1,3}(?=年)', duration)
            if y:
                l += int(y.group())
        m = re.search('[一二三四五六七八九十]{1,3}(?=个月)', duration)
        if m:
            l += int(self.trans_chinese_number(m.group()))
        else:
            m = re.search('[0-9]{1,3}(?=个月)', duration)
            if m:
                l += int(m.group())
        return l

    def get_defendant_probation(self, defendant_name, convict_info_list):
        for convict_info in convict_info_list:
            if re.search(defendant_name, convict_info):
                for p in StaticUtils.defendant_probation_pattern:
                    self.logger.debug(
                        "Search defendant probation by {} in {}".format(p, convict_info))
                    probation = re.search(p, convict_info)
                    if probation:
                        return probation.group()
        else:
            self.logger.debug("Probation is not found for {} by {} in {}".format(defendant_name, StaticUtils.defendant_probation_pattern, convict_info_list))
            return None

    def get_number(self, text):
        number = None
        # Step 1, Remove comma.
        t = text.replace(',', '')

        # Step 2, Retrun number
        n = re.search('[0-9]+', t)
        if not n:
            cn = re.search('([一二三四五六七八九十][千万])+', t)
            if cn:
                c_value = re.search('[千万]', cn.group())
                c_number = re.search('[一二三四五六七八九十]', cn.group())
                if c_value.group() == '千':
                    number = self.trans_chinese_number(c_number.group()) * 1000
                elif c_value.group() == '万':
                    number = self.trans_chinese_number(c_number.group()) * 10000
                else:
                    print(cn)
        else:
            number = n.group()
        return number

    def get_defendant_fine(self, defendant_name, convict_info_list):
        for convict_info in convict_info_list:
            if re.search(defendant_name, convict_info):
                for f in StaticUtils.defendant_fine_pattern:
                    self.logger.debug(
                        "Search defendant fine by {} in {}".format(f, convict_info))
                    fine = re.search(f, convict_info)
                    if fine:
                        return self.get_number(fine.group())
        else:
            self.logger.debug("Fine is not found for {} in {}".format(defendant_name, convict_info_list))
            return None

    def get_defendant_info(self):
        defendant_info_list = self.get_defendant_info_list()
        convict_info_list = self.get_convict_info_list()
        defendant_list = [dict() for x in range(len(defendant_info_list))]
        for index, defendant in enumerate(defendant_info_list):
            self.logger.debug("No.{} defendant info is {}".format(index, defendant))
            defendant_list[index]['name'] = self.get_defendant_name(defendant)
            defendant_list[index]['age'] = self.get_defendant_age(defendant)
            defendant_list[index]['sex'] = self.get_defendant_sex(defendant)
            defendant_list[index]['nation'] = self.get_defendant_nation(defendant)
            defendant_list[index]['education'] = self.get_defendant_education(defendant)
            defendant_list[index]['job'] = self.get_defendant_job(defendant)
            defendant_list[index]['lawyer'] = self.get_defendant_lawyer(defendant)
            defendant_list[index]['s_lawyer'] = self.get_defendant_s_lawyer(defendant)
            defendant_list[index]['bail'] = self.get_defendant_bail(defendant)

            if defendant_list[index]['lawyer']:
                defendant_list[index]['lawyer_n'] = len(defendant_list[index]['lawyer'])
            else:
                defendant_list[index]['lawyer_n'] = None

            if defendant_list[index]['s_lawyer']:
                defendant_list[index]['s_lawyer_n'] = len(defendant_list[index]['s_lawyer'])
            else:
                defendant_list[index]['s_lawyer_n'] = None

            if defendant_list[index]['lawyer_n'] == None and defendant_list[index]['s_lawyer_n'] == None:
                defendant_list[index]['has_lawyer'] = 'no'
            else:
                defendant_list[index]['has_lawyer'] = 'yes'

        if convict_info_list:
            convict_info_list = self.clean_defendant_charge(defendant_list, convict_info_list)

        for i in range(len(defendant_list)):
            defendant_list[i]['charge'] = self.get_defendant_charge(defendant_list[i]['name'], convict_info_list)
            defendant_list[i]['charge_c'] = self.get_charge_class(defendant_list[i]['charge'])
            defendant_list[i]['prison'] = self.get_defendant_prison(defendant_list[i]['name'], convict_info_list)
            defendant_list[i]['prison_l'] = self.get_prison_len(defendant_list[i]['prison'])
            defendant_list[i]['probation'] = self.get_defendant_probation(defendant_list[i]['name'], convict_info_list)
            defendant_list[i]['probation_l'] = self.get_prison_len(defendant_list[i]['probation'])
            defendant_list[i]['fine'] = self.get_defendant_fine(defendant_list[i]['name'], convict_info_list)
        return defendant_list



    def analyse_doc(self):
        if self.size < 100:
            return None
        if "附带民事" in self.content:
            return None

        case_info = dict()
        self.divide_2_mul_sections()
        case_info['name'] = self.dir_name  + '\\' + self.file_name
        case_info['verdict'] = self.get_verdict_name()
        case_info['id'] = self.get_case_id()
        case_info['court'] = self.get_court_name()
        case_info['region'] = self.get_region(case_info['court'])
        case_info['court_level'] = self.get_court_level(case_info['court'])
        case_info['prosecutor'] = self.get_prosecutor()
        case_info['procedure'] = self.get_procedure()
        case_info['year'] = self.year
        case_info['defendant'] = self.get_defendant_info()

        defendant_num = len(case_info['defendant'])
        output = [dict() for x in range(defendant_num)]
        for d in range(defendant_num):
            output[d]['file_name'] = case_info['name']
            output[d]['verdict'] = case_info['verdict']
            output[d]['id'] = case_info['id']
            output[d]['court'] = case_info['court']
            output[d]['region'] = case_info['region']
            output[d]['court_level'] = case_info['court_level']
            output[d]['prosecutor'] = case_info['prosecutor']
            output[d]['procedure'] = case_info['procedure']
            output[d]['year'] = case_info['year']
            output[d]['d_name'] = case_info['defendant'][d]['name']
            output[d]['d_age'] = case_info['defendant'][d]['age']
            output[d]['d_sex'] = case_info['defendant'][d]['sex']
            output[d]['d_nation'] = case_info['defendant'][d]['nation']
            output[d]['d_education'] = case_info['defendant'][d]['education']
            output[d]['d_job'] = case_info['defendant'][d]['job']
            output[d]['d_lawyer'] = case_info['defendant'][d]['lawyer']
            output[d]['d_lawyer_n'] = case_info['defendant'][d]['lawyer_n']
            output[d]['d_s_lawyer'] = case_info['defendant'][d]['s_lawyer']
            output[d]['d_s_lawyer_n'] = case_info['defendant'][d]['s_lawyer_n']
            output[d]['d_has_lawyer'] = case_info['defendant'][d]['has_lawyer']
            output[d]['d_charge'] = case_info['defendant'][d]['charge']
            output[d]['d_charge_c'] = case_info['defendant'][d]['charge_c']
            output[d]['d_prison'] = case_info['defendant'][d]['prison']
            output[d]['d_prison_l'] = case_info['defendant'][d]['prison_l']
            output[d]['d_probation'] = case_info['defendant'][d]['probation']
            output[d]['d_probation_l'] = case_info['defendant'][d]['probation_l']
            output[d]['d_fine'] = case_info['defendant'][d]['fine']
            output[d]['d_bail'] = case_info['defendant'][d]['bail']
        self.logger.debug("Output of case {} is {}".format(self.file_name, output))
        return output
