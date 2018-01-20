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

    def divide_2_mul_sections(self):
        self.defendent_section = self._search_by_mul_pattern(StaticUtils.defendent_section_pattern, self.content)
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
        #case_info['prosecutor'] = self._get_prosecutor()
        #case_info['procedure'] = self._get_procedure()
        #case_info['private_prosecution'] = self._get_private_prosecution()
        #case_info['year'] = self._get_year(case_info['id'])
        return case_info

        #case_info['defendent'] = self._get_defendent_info()