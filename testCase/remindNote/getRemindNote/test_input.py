import time
import datetime
import requests
import unittest
from businessCommon.createNotes import Create
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re
from parameterized import parameterized


@class_case_log
class GetRemindNote(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    url = host + dataConfig['interface']['GetRemindNote']['path']
    base = dataConfig['interface']['GetRemindNote']['base']
    mustKey = dataConfig['interface']['GetRemindNote']['mustKeys']
    assertBase = {
        'responseTime': int,
        'webNotes': [
            {
                'noteId': str,
                'createTime': int,
                'star': 0,
                'remindTime': int,
                'remindType': int,
                'infoVersion': int,
                'infoUpdateTime': int,
                'groupId': None,
                'title': str,
                'summary': str,
                'thumbnail': None,
                'contentVersion': int,
                'contentUpdateTime': int
            }
        ]
    }

    remind_start_time_empty = [{'remindStartTime': None, 'code': 500}]
    remind_end_time_empty = [{'remindEndTime': None, 'code': 500}]
    start_index_empty = [{'startIndex': None, 'code': 500}]
    start_index_value = [[{'startIndex': 0, 'code': 200}], [{'startIndex': 1, 'code': 200}], [{'startIndex': -1, 'code': 200}]]
    start_index_value1 = [[{'startIndex': '1', 'code': 500}], [{'startIndex': 'abc', 'code': 500}], [{'startIndex': 1.5, 'code': 500}]]
    rows_empty = [{'rows': None, 'code': 500}]
    rows_value1 = [[{'rows': '你好abc@&#……￥', 'code': 500}], [{'rows': '1', 'code': 500}]]
    rows_value2 = [[{'rows': -1, 'code': 500}], [{'rows': 1.5, 'code': 500}]]
    x_user_key_empty = [[{'X-user-key': None, 'code': 412}], [{'X-user-key': '', 'code': 412}]]
    x_user_key_value = [[{'X-user-key': '@%^&*你好asd', 'code': 500}], [{'X-user-key': '-1557488247', 'code': 500}]]

    def setUp(self) -> None:
        Clear().clearRemindNotes(self.userId1, self.sid1)

    @parameterized.expand(mustKey)
    def testCase01(self, key):
        """必填项字段缺失校验"""
        step('PRE-STEP:新增一条日历便签数据')
        dic = Create().create_mind_note(self.userId1, self.sid1, 2)

        step('STEP:获取日历便签接口请求')
        body = {
            'remindStartTime': dic['contentUpdateTime'][0],
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 999
        }
        body.pop(key)
        print(body)
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "remindTime Requested!"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(remind_start_time_empty)
    def testCase02(self, dic):
        """查看日历便签的remindStartTime枚举值校验-空"""
        step('STEP:获取日历便签接口请求')
        body = {
            'remindStartTime': dic['remindStartTime'],
            'remindEndTime': int(time.time()) * 1000,
            'startIndex': 0,
            'rows': 999
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase03(self):
        """查看日历便签的remindStartTime枚举值校验-值为负数：-2023101623230000"""
        step('STEP:获取日历便签接口请求')
        body = {
            'remindStartTime': -2023101623230000,
            'remindEndTime': int(time.time()) * 1000,
            'startIndex': 0,
            'rows': 999
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase04(self):
        """查看日历便签的remindStartTime枚举值校验-值足够大"""
        step('STEP:获取日历便签接口请求')
        body = {
            'remindStartTime': int(time.time()),
            'remindEndTime': int(time.time()) * 1000,
            'startIndex': 0,
            'rows': 999
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    def testCase05(self):
        """查看日历便签的remindStartTime枚举值校验-值足够小"""
        step('STEP:获取日历便签接口请求')
        body = {
            'remindStartTime': int(time.time()) * 1000,
            'remindEndTime': int(time.time()) * 1000,
            'startIndex': 0,
            'rows': 999
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(remind_end_time_empty)
    def testCase06(self, dic):
        """查看日历便签的remindEndTime枚举值校验-空"""
        step('STEP:获取日历便签接口请求')
        body = {
            'remindStartTime': int(time.time()) * 1000,
            'remindEndTime': dic['remindEndTime'],
            'startIndex': 0,
            'rows': 999
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "remindTime Requested!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase07(self):
        """查看日历便签的remindEndTime枚举值校验-值为负数：-2023101623230000"""
        step('STEP:获取日历便签接口请求')
        body = {
            'remindStartTime': int(time.time()) * 1000,
            'remindEndTime': -2023101623230000,
            'startIndex': 0,
            'rows': 999
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase08(self):
        """查看日历便签的remindEndTime枚举值校验-值足够大"""
        step('STEP:获取日历便签接口请求')
        body = {
            'remindStartTime': int(time.time()) * 1000,
            'remindEndTime': int(time.time()),
            'startIndex': 0,
            'rows': 999
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    def testCase09(self):
        """查看日历便签的remindEndTime枚举值校验-值足够小"""
        step('STEP:获取日历便签接口请求')
        body = {
            'remindStartTime': int(time.time()) * 1000,
            'remindEndTime': int(time.time()) * 1000,
            'startIndex': 0,
            'rows': 999
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(start_index_empty)
    def testCase10(self, dic):
        """查看日历便签的startindex枚举值校验-空"""
        step('PRE-STEP:新增一条日历便签数据')
        dic1 = Create().create_mind_note(self.userId1, self.sid1, 2)

        step('STEP:获取日历便签接口请求')
        body = {
            'remindStartTime': dic1['contentUpdateTime'][0],
            'remindEndTime': dic1['contentUpdateTime'][1],
            'startIndex': dic['startIndex'],
            'rows': 999
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "remindTime Requested!"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(start_index_value)
    def testCase11(self, dic):
        """查看日历便签的startindex枚举值校验-0,1,-1"""
        step('PRE-STEP:新增一条日历便签数据')
        dic1 = Create().create_mind_note(self.userId1, self.sid1, 2)

        step('STEP:获取日历便签接口请求')
        body = {
            'remindStartTime': dic1['contentUpdateTime'][0],
            'remindEndTime': dic1['contentUpdateTime'][1],
            'startIndex': dic['startIndex'],
            'rows': 999
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(start_index_value1)
    def testCase12(self, dic):
        """查看日历便签的startindex枚举值校验-非法"""
        step('PRE-STEP:新增一条日历便签数据')
        dic1 = Create().create_mind_note(self.userId1, self.sid1, 2)

        step('STEP:获取日历便签接口请求')
        body = {
            'remindStartTime': dic1['contentUpdateTime'][0],
            'remindEndTime': dic1['contentUpdateTime'][1],
            'startIndex': dic['startIndex'],
            'rows': 999
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "remindTime Requested!"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(rows_empty)
    def testCase13(self, dic):
        """查看日历便签的rows枚举值校验-空"""
        step('PRE-STEP:新增一条日历便签数据')
        dic1 = Create().create_mind_note(self.userId1, self.sid1, 2)

        step('STEP:获取日历便签接口请求')
        body = {
            'remindStartTime': dic1['contentUpdateTime'][0],
            'remindEndTime': dic1['contentUpdateTime'][1],
            'startIndex': 0,
            'rows': dic['rows']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "remindTime Requested!"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(rows_value1)
    def testCase14(self, dic):
        """查看日历便签的startindex枚举值校验-值为str"""
        step('PRE-STEP:新增一条日历便签数据')
        dic1 = Create().create_mind_note(self.userId1, self.sid1, 2)

        step('STEP:获取日历便签接口请求')
        body = {
            'remindStartTime': dic1['contentUpdateTime'][0],
            'remindEndTime': dic1['contentUpdateTime'][1],
            'startIndex': 0,
            'rows': dic['rows']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(rows_value2)
    def testCase15(self, dic):
        """查看日历便签的startindex枚举值校验-值非法"""
        step('PRE-STEP:新增2条日历便签数据')
        dic1 = Create().create_mind_note(self.userId1, self.sid1, 2)

        step('STEP:获取日历便签接口请求')
        body = {
            'remindStartTime': dic1['contentUpdateTime'][0],
            'remindEndTime': int(time.time()) * 1000,
            'startIndex': 0,
            'rows': dic['rows']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "remindTime Requested!"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(x_user_key_empty)
    def testCase16(self, dic):
        """X-user-key枚举值-值为空校验"""
        step('PRE-STEP:新增2条日历便签数据')
        dic1 = Create().create_mind_note(self.userId1, self.sid1, 2)
        step('STEP:获取日历便签接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': dic['X-user-key']
        }
        body = {
            'remindStartTime': dic1['contentUpdateTime'][0],
            'remindEndTime': int(time.time()) * 1000,
            'startIndex': 0,
            'rows': 999
        }

        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "X-user-key header Requested!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase17(self):
        """X-user-key枚举值校验:X-user-key不存在"""
        step('STEP:新增便签内容的接口请求')
        dic1 = Create().create_mind_note(self.userId1, self.sid1, 2)
        step('PRE-STEP:新增一条日历便签数据')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': '24194159'
        }
        body = {
            'remindStartTime': dic1['remindStartTime'],
            'remindEndTime': int(time.time()) * 1000,
            'startIndex': 0,
            'rows': 999
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(x_user_key_value)
    def testCase18(self, dic):
        """X-user-key枚举值校验:负数、字母文字特殊字符"""
        step('STEP:新增便签内容的接口请求')
        dic1 = Create().create_mind_note(self.userId1, self.sid1, 2)
        step('PRE-STEP:新增一条日历便签数据')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': dic['X-user-key']
        }
        body = {
            'remindStartTime': dic1['remindStartTime'],
            'remindEndTime': int(time.time()) * 1000,
            'startIndex': 0,
            'rows': 999
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase19(self):
        """身份校验-过期的wps_id"""
        step('STEP:新增便签内容的接口请求')
        dic1 = Create().create_mind_note(self.userId1, self.sid1, 2)
        step('PRE-STEP:新增一条日历便签数据')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid=V02SHoAtXgU_OhHVxg3RazDCWu-WR5Q00a0dd16b005cd56277',
            'X-user-key': '241941591'
        }
        body = {
            'remindStartTime': dic1['remindStartTime'],
            'remindEndTime': int(time.time()) * 1000,
            'startIndex': 0,
            'rows': 999
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(401, res.status_code)
        expr = {"errorCode": -2010, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())

    def testCase20(self):
        """身份校验-非法的wps_id"""
        step('STEP:新增便签内容的接口请求')
        dic1 = Create().create_mind_note(self.userId1, self.sid1, 2)
        step('PRE-STEP:新增一条日历便签数据')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid=7867567eas092q90843=-=-==-=]\]\]\]',
            'X-user-key': '241941591'
        }
        body = {
            'remindStartTime': dic1['remindStartTime'],
            'remindEndTime': int(time.time()) * 1000,
            'startIndex': 0,
            'rows': 999
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(401, res.status_code)
        expr = {"errorCode": -2009, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())

    def testCase21(self):
        """身份校验-wps_id缺失"""
        step('STEP:新增便签内容的接口请求')
        dic1 = Create().create_mind_note(self.userId1, self.sid1, 2)
        step('PRE-STEP:新增一条日历便签数据')
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': '241941591'
        }
        body = {
            'remindStartTime': dic1['remindStartTime'],
            'remindEndTime': int(time.time()) * 1000,
            'startIndex': 0,
            'rows': 999
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(401, res.status_code)
        expr = {"errorCode": -2009, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())






