# -*- coding: UTF-8 -*-
import os
import unittest
import VerdictAnalyser


class TestVerdictAnalyser(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.defendent_list = list()
        self.defendent_info_list = list()
        self.cv_list = list()
        self.cv_result_list = list()

        self.defendent_info_list.append({"name":"李刚李某","sex":"男", "age":32, "nation":"汉族", "education":"高中", "job":"无业", "lawyer":None, "s_lawyer":None})
        self.defendent_info_list.append(
            dict(name="严某", sex=None, age=None, nation=None, education=None, job=None,
                 lawyer=['辩护人易某，北京炜衡（成都）律师事务所律师', '辩护人李某，北京炜衡（成都）律师事务所律师'], s_lawyer=None))
        self.defendent_info_list.append(
            {"name": "程气东", "sex": "男", "age": 42, "nation": "汉族", "education": "初中", "job": "农民", "lawyer": ['辩护人袁成刚，四川明炬律师事务所律师'],
             "s_lawyer": None})
        self.defendent_info_list.append(
            {"name": "龚林强", "sex": "男", "age": 27, "nation": "汉族", "education": "小学", "job": "无业",
             "lawyer": ['辩护人赵敏，四川斗城律师事务所律师'],
             "s_lawyer": None})
        self.cv_list.append({"d_name":"丁祖樊", "content":['被告人丁祖樊犯妨害公务罪，单处罚金人民币一万元。（罚金在本判决生效后三十日内缴纳）']})
        self.cv_result_list.append({"charge":"妨害公务","prison":None, "fine":10000, "probation":None})

    def setUp(self):
        with open(os.path.dirname(__file__) + '\\test_data\\defendent_list.txt', 'r', encoding='utf-8') as t:
            for line in t:
                self.defendent_list.append(line)

    def test_get_len(self):
        v = VerdictAnalyser.VerdictAnalyser()
        length = v._get_len('五年')
        self.assertEqual(length, 60)
        length = v._get_len('三个月')
        self.assertEqual(length, 3)
        length = v._get_len('一年六个月')
        self.assertEqual(length, 18)
        length = v._get_len('拘役3个月15天')
        self.assertEqual(length, 3)


    def test_get_defendent_name(self):
        v = VerdictAnalyser.VerdictAnalyser()
        for i in range(len(self.defendent_list)):
            g = v._get_defendent_name(self.defendent_list[i])
        if self.defendent_info_list[i]['name']:
            self.assertEqual(g, self.defendent_info_list[i]['name'])
        else:
            self.assertFalse(g)

    def test_get_defendent_age(self):
        v = VerdictAnalyser.VerdictAnalyser()
        for i in range(len(self.defendent_list)):
            g = v._get_defendent_age(self.defendent_list[i])
        if self.defendent_info_list[i]['age']:
            self.assertEqual(g, self.defendent_info_list[i]['age'])
        else:
            self.assertFalse(g)

    def test_get_defendent_sex(self):
        v = VerdictAnalyser.VerdictAnalyser()
        for i in range(len(self.defendent_list)):
            g = v._get_defendent_sex(self.defendent_list[i])
        if self.defendent_info_list[i]['sex']:
            self.assertEqual(g, self.defendent_info_list[i]['sex'])
        else:
            self.assertFalse(g)

    def test_get_defendent_nation(self):
        v = VerdictAnalyser.VerdictAnalyser()
        for i in range(len(self.defendent_list)):
            g = v._get_defendent_nation(self.defendent_list[i])
        if self.defendent_info_list[i]['nation']:
            self.assertEqual(g, self.defendent_info_list[i]['nation'])
        else:
            self.assertFalse(g)

    def test_get_defendent_education(self):
        v = VerdictAnalyser.VerdictAnalyser()
        for i in range(len(self.defendent_list)):
            g = v._get_defendent_education(self.defendent_list[i])
        if self.defendent_info_list[i]['education']:
            self.assertEqual(g, self.defendent_info_list[i]['education'])
        else:
            self.assertFalse(g)

    def test_get_defendent_job(self):
        v = VerdictAnalyser.VerdictAnalyser()
        for i in range(len(self.defendent_list)):
            g = v._get_defendent_job(self.defendent_list[i])
        if self.defendent_info_list[i]['job']:
            self.assertEqual(g, self.defendent_info_list[i]['job'])
        else:
            self.assertFalse(g)

    def test_get_defendent_lawyer(self):
        v = VerdictAnalyser.VerdictAnalyser()
        for i in range(len(self.defendent_list)):
            g = v._get_defendent_lawyer(self.defendent_list[i])
        if self.defendent_info_list[i]['lawyer']:
            self.assertEqual(g, self.defendent_info_list[i]['lawyer'])
        else:
            self.assertFalse(g)

    def test_get_defendent_s_lawyer(self):
        v = VerdictAnalyser.VerdictAnalyser()
        for i in range(len(self.defendent_list)):
            g = v._get_defendent_s_lawyer(self.defendent_list[i])
        if self.defendent_info_list[i]['s_lawyer']:
            self.assertEqual(g, self.defendent_info_list[i]['s_lawyer'])
        else:
            self.assertFalse(g)

    def test_get_defendent_prison(self):
        v = VerdictAnalyser.VerdictAnalyser()
        for i in range(len(self.cv_list)):
            g = v._get_defendent_prison(self.cv_list[i]['d_name'], self.cv_list[i]['content'])
        if self.cv_result_list[i]['prison']:
            self.assertEqual(g, self.defendent_info_list[i]['prison'])
        else:
            self.assertFalse(g)

    def test_clean_defendent_charge(self):
        v = VerdictAnalyser.VerdictAnalyser()
        d_name = [{"name":"a"},{"name":"b"},{"name":"c"}]
        c_source1 = ['a', 'a', 'b', 'c', 'abc']
        c_result1 = ['aa', 'b', 'c']
        g = v._clean_defendent_charge(d_name, c_source1)
        self.assertListEqual(g, c_result1)

        c_source2 = ['a', 'b', 'ab', 'b', 'c', 'abc']
        c_result2 = ['a', 'bb', 'c']

        g = v._clean_defendent_charge(d_name, c_source2)
        self.assertListEqual(g, c_result2)

        c_source3 = ['d', 'a', 'bb', 'b', 'abc']
        c_result3 = ['a', 'bbb']

        g = v._clean_defendent_charge(d_name, c_source3)
        self.assertListEqual(g, c_result3)


if __name__ == '__main__':
    unittest.main()
