import time
import requests
import unittest
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re
from parameterized import parameterized


@class_case_log
class SetNotesContent(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    key = envConfig['key']
    iv = envConfig['iv']
    host = envConfig['host']
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    dataConfig = YamlRead().data_config()
    url = host + dataConfig['interface']['SetNotesContent']['path']
    note_info_url = host + dataConfig['interface']['SetCommonNote']['path']
    note_info_base = dataConfig['interface']['SetCommonNote']['base']
    assertBase = {
        'responseTime': int,
        'contentVersion': int,
        'contentUpdateTime': int
    }

    mustKey = dataConfig['interface']['SetNotesContent']['mustKey']
    note_id_empty = [[{'noteId': '', 'code': 500}], [{'noteId': None, 'code': 500}]]
    title_empty = [[{'title': '', 'code': 500}], [{'title': None, 'code': 500}]]
    summary_empty = [[{'summary': '', 'code': 500}], [{'summary': None, 'code': 500}]]
    body_empty = [[{'body': '', 'code': 412}], [{'body': None, 'code': 412}]]
    local_content_version_empty = [[{'localContentVersion': '', 'code': 500}], [{'localContentVersion': None, 'code': 500}]]
    body_type_value = [[{'BodyType': 2, 'code': 500}], [{'BodyType': None, 'code': 500}]]
    x_user_key_empty = [[{'X-user-key': None, 'code': 412}], [{'X-user-key': '', 'code': 412}]]
    x_user_key_value = [[{'X-user-key': '@%^&*你好asd', 'code': 500}], [{'X-user-key': '-1557488247', 'code': 500}]]

    def setUp(self) -> None:
        Clear().clearNotesList(self.userId1, self.sid1)

    @parameterized.expand(mustKey)
    def testCase01(self, key):
        """必填项字段缺失校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        body.pop(key)
        print(body)
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(note_id_empty)
    def testCase02(self, dic):
        """新增便签的noteId枚举值校验-空"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': dic['noteId'],
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase03(self):
        """noteId过长校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': '9999999999999999999999999999999999999999999999999999999999',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        if len(body['noteId']) > 32:
            res.status_code = 500
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase04(self):
        """noteId输入文字字母校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': '你好abc',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase05(self):
        """noteId输入特殊字符校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': '@&#……￥',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase06(self):
        """noteId输入‘ or ‘1=1校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': "' or '1=1",
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    def testCase07(self):
        """noteId输入" or "1=1校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': '" or "1=1',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(title_empty)
    def testCase08(self, dic):
        """新增便签的title枚举值校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': dic['title'],
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase09(self):
        """title过长校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': '9999999999999999999999999999999999',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        if len(body['title']) > 32:
            res.status_code = 500
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase10(self):
        """title输入‘ or ‘1=1校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': "' or '1=1",
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase11(self):
        """title输入" or "1=1校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': '" or "1=1',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(summary_empty)
    def testCase12(self, dic):
        """新增便签summary枚举值校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': dic['summary'],
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase13(self):
        """summary过长校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': '9999999999999999999999999999999999',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        if len(body['summary']) > 32:
            res.status_code = 500
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase14(self):
        """summary输入‘ or ‘1=1校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': "' or '1=1",
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase15(self):
        """summary输入" or "1=1校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': '" or "1=1',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(body_empty)
    def testCase16(self, dic):
        """新增便签body枚举值校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': dic['body'],
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -1012, "errorMsg": "Note body Requested!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase17(self):
        """body过长校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': '99999999999999999999999999999999999999999999999999',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        if len(body['body']) > 32:
            res.status_code = 500
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase18(self):
        """body输入‘ or ‘1=1校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': '' or '1=1',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase19(self):
        """body输入" or "1=1校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': '" or "1=1',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(local_content_version_empty)
    def testCase20(self, dic):
        """新增便签localContentVersion枚举值校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': dic['localContentVersion'],
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase21(self):
        """新增便签localContentVersion与便签主体接口返回的infoVersion一致"""
        step('PRE-STEP:新建便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body1 = self.note_info_base
        body1['noteId'] = noteId

        res1 = self.re.post(url=self.note_info_url, body=body1, userId=self.userId1, sid=self.sid1)
        info_version = res1.json()["infoVersion"]
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(body['localContentVersion'], info_version)
        expr = {"responseTime": int, "contentVersion": int, "contentUpdateTime": int}
        OutputCheck().assert_output(expr, res.json())

    def testCase22(self):
        """新增便签localContentVersion与便签主体接口返回的infoVersion不一致"""
        step('PRE-STEP:新建便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body1 = self.note_info_base
        body1['noteId'] = noteId

        res1 = self.re.post(url=self.note_info_url, body=body1, userId=self.userId1, sid=self.sid1)
        info_version = res1.json()["infoVersion"]
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 89,
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expr = {"responseTime": int, "contentVersion": int, "contentUpdateTime": int}
        OutputCheck().assert_output(expr, res.json())
        self.assertEqual(body['localContentVersion'], info_version)

    def testCase23(self):
        """新增便签localContentVersion值为str"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': '2@%^&*你好asd',
            'bodyType': 0
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(body_type_value)
    def testCase24(self, dic):
        """新增便签BodyType枚举值校验"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': dic['BodyType']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase25(self):
        """新增便签bodyType值为str"""
        step('STEP:新增便签内容的接口请求')
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': '2@%^&*你好asd',
            'bodyType': '@&#……￥你好abc'
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(x_user_key_empty)
    def testCase26(self, dic):
        """X-user-key枚举值-值为空校验"""
        step('STEP:新增便签内容的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': dic['X-user-key']
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "X-user-key header Requested!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase27(self):
        """X-user-key枚举值校验:X-user-key不存在"""
        step('STEP:新增便签内容的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': '24194159'
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(x_user_key_value)
    def testCase28(self, dic):
        """X-user-key枚举值校验:负数、字母文字特殊字符"""
        step('STEP:新增便签内容的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': dic['X-user-key']
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase29(self):
        """身份校验-过期的wps_id"""
        step('STEP:新增便签内容的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid=V02SHoAtXgU_OhHVxg3RazDCWu-WR5Q00a0dd16b005cd56277',
            'X-user-key': '241941591'
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(401, res.status_code)
        expr = {"errorCode": -2010, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())

    def testCase30(self):
        """身份校验-非法的wps_id"""
        step('STEP:新增便签内容的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid=7867567eas092q90843=-=-==-=]\]\]\]',
            'X-user-key': '241941591'
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(401, res.status_code)
        expr = {"errorCode": -2009, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())

    def testCase31(self):
        """身份校验-wps_id缺失"""
        step('STEP:新增便签内容的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': '241941591'
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
            'title': 'title',
            'summary': 'summary',
            'body': 'body',
            'localContentVersion': 1,
            'bodyType': 0
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(401, res.status_code)
        expr = {"errorCode": -2009, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())
