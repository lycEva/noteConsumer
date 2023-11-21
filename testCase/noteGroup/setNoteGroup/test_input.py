import unittest
import requests
import time
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re
from parameterized import parameterized


@class_case_log
class SetNoteGroup(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    key = envConfig['key']
    iv = envConfig['iv']
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    dataConfig = YamlRead().data_config()
    url = host + dataConfig['interface']['SetGroupNote']['path']
    base = dataConfig['interface']['SetGroupNote']['base']
    mustKey = dataConfig['interface']['SetGroupNote']['mustKeys']
    optionKey = dataConfig['interface']['SetGroupNote']['optionKey']
    assertBase = {
        'responseTime': int,
        'updateTime': int
    }

    group_id_empty = [[{'groupId': '', 'code': 500}], [{'groupId': None, 'code': 500}]]
    group_id_value = [[{'groupId': '@&#……￥', 'code': 500}], [{'groupId': '你好abc', 'code': 500}]]
    order_empty = [{'order': None, 'code': 200}]
    order_value1 = [[{'order': 1, 'code': 200}], [{'order': 0, 'code': 200}]]
    order_value2 = [[{'order': 'abc', 'code': 500}], [{'order': '1', 'code': 500}]]
    x_user_key_empty = [[{'X-user-key': None, 'code': 412}], [{'X-user-key': '', 'code': 412}]]
    x_user_key_value = [[{'X-user-key': '@%^&*你好asd', 'code': 500}], [{'X-user-key': '-1557488247', 'code': 500}]]

    def setUp(self) -> None:
        Clear().clearNotesList(self.userId1, self.sid1)

    @parameterized.expand(mustKey)
    def testCase01(self, key):
        """必填项字段缺失校验"""
        step('STEP:新增分组的接口请求')
        body = {
            'groupId': str(int(time.time()) * 1000) + '_groupId',
            'groupName': 'groupName',
            'order': 0
        }
        body.pop(key)
        print(body)
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(optionKey)
    def testCase02(self, key):
        """非必填项字段缺失校验"""
        step('STEP:新增分组的接口请求')
        body = {
            'groupId': str(int(time.time()) * 1000) + '_groupId',
            'groupName': 'groupName',
            'order': 0
        }
        body.pop(key)
        print(body)
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(group_id_empty)
    def testCase03(self, dic):
        """新增分组的groupId必填项校验"""
        step('STEP:新增分组的接口请求')
        body = {
            'groupId':  dic['groupId'],
            'groupName': 'groupName',
            'order': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase04(self):
        """新增分组的groupId枚举值校验"""
        step('STEP:新增分组的接口请求')
        body = {
            'groupId': '9999999999999999999999999999999999999999999999999999999999',
            'groupName': 'groupName',
            'order': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        if len(body['groupId']) > 32:
            res.status_code = 500
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(group_id_value)
    def testCase05(self, dic):
        """groupId输入文字字母、特殊字符校验"""
        step('STEP:新增分组的接口请求')
        body = {
            'groupId': dic['group_id'],
            'groupName': 'groupName',
            'order': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase06(self):
        """新增分组的groupId输入' or'1=1"""
        step('STEP:新增分组的接口请求')
        body = {
            'groupId': '' or '1=1',
            'groupName': 'groupName',
            'order': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase07(self):
        """新增分组的groupId输入" or "1=1"""
        step('STEP:新增分组的接口请求')
        body = {
            'groupId': '" or " 1=1',
            'groupName': 'groupName',
            'order': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase08(self):
        """新增分组的groupName输入过长"""
        step('STEP:新增分组的接口请求')
        body = {
            'groupId': str(int(time.time()) * 1000) + '_groupId',
            'groupName': '9999999999999999999999999999999999999999999999999999999999',
            'order': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        if len(body['groupName']) > 32:
            res.status_code = 500
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(order_empty)
    def testCase09(self, dic):
        """新增分组的order必填项校验"""
        step('STEP:新增分组的接口请求')
        body = {
            'groupId': str(int(time.time()) * 1000) + '_groupId',
            'groupName': 'groupName',
            'order': dic['order']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(order_value1)
    def testCase10(self, dic):
        """新增分组的order枚举值校验-0、1"""
        step('STEP:新增分组的接口请求')
        body = {
            'groupId': str(int(time.time()) * 1000) + '_groupId',
            'groupName': 'groupName',
            'order': dic['order']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(order_value2)
    def testCase11(self, dic):
        """新增分组的order枚举值校验-str"""
        step('STEP:新增分组的接口请求')
        body = {
            'groupId': str(int(time.time()) * 1000) + '_groupId',
            'groupName': 'groupName',
            'order': dic['order']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(x_user_key_empty)
    def testCase12(self, dic):
        """X-user-key枚举值-值为空校验"""
        step('STEP:新增便签主体的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': dic['X-user-key']
        }
        body = {
            'groupId': str(int(time.time()) * 1000) + '_groupId',
            'groupName': 'groupName',
            'order': 0
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "X-user-key header Requested!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase13(self):
        """X-user-key枚举值校验:X-user-key不存在"""
        step('STEP:新增便签主体的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': '24194159'
        }
        body = {
            'groupId': str(int(time.time()) * 1000) + '_groupId',
            'groupName': 'groupName',
            'order': 0
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(x_user_key_value)
    def testCase14(self, dic):
        """X-user-key枚举值校验:负数、字母文字特殊字符"""
        step('STEP:新增便签主体的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': dic['X-user-key']
        }
        body = {
            'groupId': str(int(time.time()) * 1000) + '_groupId',
            'groupName': 'groupName',
            'order': 0
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase15(self):
        """身份校验-过期的wps_id"""
        step('STEP:新增便签主体的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid=V02SHoAtXgU_OhHVxg3RazDCWu-WR5Q00a0dd16b005cd56277',
            'X-user-key': '241941591'
        }
        body = {
            'groupId': str(int(time.time()) * 1000) + '_groupId',
            'groupName': 'groupName',
            'order': 0
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(401, res.status_code)
        expr = {"errorCode": -2010, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())

    def testCase16(self):
        """身份校验-非法的wps_id"""
        step('STEP:新增便签主体的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid=7867567eas092q90843=-=-==-=]\]\]\]',
            'X-user-key': '241941591'
        }
        body = {
            'groupId': str(int(time.time()) * 1000) + '_groupId',
            'groupName': 'groupName',
            'order': 0
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(401, res.status_code)
        expr = {"errorCode": -2009, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())

    def testCase17(self):
        """身份校验-wps_id缺失"""
        step('STEP:新增便签主体的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': '241941591'
        }
        body = {
            'groupId': str(int(time.time()) * 1000) + '_groupId',
            'groupName': 'groupName',
            'order': 0
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(401, res.status_code)
        expr = {"errorCode": -2009, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())







