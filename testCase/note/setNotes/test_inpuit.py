import unittest
import requests
import time
from businessCommon.createNotes import Create
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re
from parameterized import parameterized


@class_case_log
class SetNotes(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    host = envConfig['host']
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    url = host + dataConfig['interface']['SetCommonNote']['path']
    base = dataConfig['interface']['SetCommonNote']['base']
    mustKey = dataConfig['interface']['SetCommonNote']['mustKey']
    optionKey = dataConfig['interface']['SetCommonNote']['optionKey']
    optionKey1 = dataConfig['interface']['SetGroupNoteInfo']['optionKeys']
    optionKey2 = dataConfig['interface']['SetRemindNote']['optionKeys']
    assertBase = {
        'responseTime': int,
        'infoVersion': int,
        'infoUpdateTime': int
    }

    note_id_empty = [[{'noteId': '', 'code': 500}], [{'noteId': None, 'code': 500}]]
    star_empty = [{'star': None, 'code': 200}]
    star_value = [[{'star': 0, 'code': 200}], [{'star': 1, 'code': 200}]]
    star_value1 = [[{'star': 2, 'code': 500}], [{'star': '1', 'code': 500}]]
    star_value2 = [[{'star': '@&#……￥', 'code': 500}], [{'star': '你好abc', 'code': 500}]]
    remind_time_empty = [{'remindTime': None, 'code': 200}]
    remind_time_value = [[{'remindTime': '1', 'code': 500}], [{'remindTime': -2023101623230000, 'code': 500}]]
    remind_type_empty = [{'remindType': None, 'code': 200}]
    remind_type_value = [[{'remindType': 0, 'code': 200}], [{'remindType': 1, 'code': 200}]], [[{'remindType': 2, 'code': 200}]]
    remind_type_value1 = [[{'remindType': -1, 'code': 500}], [{'remindType': '@&#……￥', 'code': 500}]]
    group_id_empty = [[{'groupId': '', 'code': 500}], [{'groupId': None, 'code': 500}]]
    group_id_value = [[{'groupId': '@&#……￥', 'code': 500}], [{'groupId': '你好abc', 'code': 500}]]
    x_user_key_empty = [[{'X-user-key': None, 'code': 412}], [{'X-user-key': '', 'code': 412}]]
    x_user_key_value = [[{'X-user-key': '@%^&*你好asd', 'code': 500}], [{'X-user-key': '-1557488247', 'code': 500}]]

    def setUp(self) -> None:
        Clear().clearNotesList(self.userId1, self.sid1)

    @parameterized.expand(mustKey)
    def testCase01(self, key):
        """必填项字段缺失校验"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'star': 0
        }
        body.pop(key)
        print(body)
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(optionKey)
    def testCase02(self, key):
        """非必填项字段缺失校验-普通便签"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'star': 0
        }
        body.pop(key)
        print(body)
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(optionKey1)
    def testCase03(self, key):
        """非必填项字段缺失校验-分组便签"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': 'noteId',
            'star': 0,
            'groupId': 'groupId'
        }
        body.pop(key)
        print(body)
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(optionKey2)
    def testCase04(self, key):
        """非必填项字段缺失校验-日历便签"""
        step('STEP:新增便签主体的接口请求')
        body = {
          'noteId': str(int(time.time()) * 1000) + '_noteId',
          'star': 0,
          'remindTime': int(time.time()) * 1000,
          'remindType': 0
        }
        body.pop(key)
        print(body)
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(note_id_empty)
    def testCase05(self, dic):
        """新增便签的noteId必填项校验"""
        step('PRE-STEP: 新增一条便签')
        dic = Create().create_note(self.userId1, self.sid1, 1)
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': dic['noteId'],
            'star': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase06(self):
        """noteId过长校验"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': '9999999999999999999999999999999999999999999999999999999999',
            'star': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        if len(body['noteId']) > 32:
            res.status_code = 500
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase07(self):
        """noteId输入文字字母校验"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': '你好abc',
            'star': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase08(self):
        """noteId输入特殊字符校验"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': '@&#……￥',
            'star': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase09(self):
        """noteId输入‘ or ‘1=1校验"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': "' or '1=1",
            'star': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase10(self):
        """noteId输入" or "1=1校验"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': '" or "1=1',
            'star': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(star_empty)
    def testCase11(self, dic):
        """新增便签的star必填项校验-值为空"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'star': dic['star']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(star_value1)
    def testCase12(self, dic):
        """新增便签的star的枚举值校验"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'star': dic['star']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(star_value2)
    def testCase13(self, dic):
        """新增便签的star的枚举值校验-非法字符"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'star': dic['star']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(remind_time_empty)
    def testCase14(self, dic):
        """新增便签的remindTime必填项校验"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'remindTime': dic['remindTime'],
            'remindType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(remind_time_value)
    def testCase15(self, dic):
        """新增便签的remindTime枚举值校验-值为str、值为负数"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'remindTime': dic['remindTime'],
            'remindType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase16(self):
        """新增便签的remindTime枚举值校验-足够大"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'remindTime': int(time.time() * 1000),
            'remindType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    def testCase17(self):
        """新增便签的remindTime枚举值校验-足够小"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'remindTime': int(time.time()),
            'remindType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(remind_type_empty)
    def testCase18(self, dic):
        """新增便签的remindType必填项校验"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'remindTime': int(time.time() * 1000),
            'remindType': dic['remindType']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(remind_type_value)
    def testCase19(self, dic):
        """新增便签的remindType枚举值校验-0,1,2"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'remindTime': int(time.time() * 1000),
            'remindType': dic['remindType']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(remind_type_value1)
    def testCase20(self, dic):
        """新增便签的remindType枚举值校验-负数、str"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'remindTime': int(time.time() * 1000),
            'remindType': dic['remindType']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(group_id_empty)
    def testCase21(self, dic):
        """新增便签的groupId必填项校验"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'groupId': dic['groupId']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    def testCase22(self):
        """新增便签的groupId枚举值校验"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'groupId': '9999999999999999999999999999999999999999999999999999999999'
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        if len(body['groupId']) > 32:
            res.status_code = 500
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(group_id_value)
    def testCase23(self, dic):
        """groupId输入文字字母、特殊字符校验"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'groupId': dic['group_id']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase24(self):
        """新增便签的groupId输入' or'1=1"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'groupId': '' or '1=1'
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase25(self):
        """新增便签的groupId输入" or "1=1"""
        step('STEP:新增便签主体的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'groupId': '" or " 1=1'
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(x_user_key_empty)
    def testCase26(self, dic):
        """X-user-key枚举值-值为空校验"""
        step('STEP:新增便签主体的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': dic['X-user-key']
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "X-user-key header Requested!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase27(self):
        """X-user-key枚举值校验:X-user-key不存在"""
        step('STEP:新增便签主体的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': '24194159'
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(x_user_key_value)
    def testCase28(self, dic):
        """X-user-key枚举值校验:负数、字母文字特殊字符"""
        step('STEP:新增便签主体的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': dic['X-user-key']
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase29(self):
        """身份校验-过期的wps_id"""
        step('STEP:新增便签主体的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid=V02SHoAtXgU_OhHVxg3RazDCWu-WR5Q00a0dd16b005cd56277',
            'X-user-key': '241941591'
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(401, res.status_code)
        expr = {"errorCode": -2010, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())

    def testCase30(self):
        """身份校验-非法的wps_id"""
        step('STEP:新增便签主体的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid=7867567eas092q90843=-=-==-=]\]\]\]',
            'X-user-key': '241941591'
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(401, res.status_code)
        expr = {"errorCode": -2009, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())

    def testCase31(self):
        """身份校验-wps_id缺失"""
        step('STEP:新增便签主体的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': '241941591'
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(401, res.status_code)
        expr = {"errorCode": -2009, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())






























