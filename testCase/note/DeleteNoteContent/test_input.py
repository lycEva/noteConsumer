import unittest
import requests
import time
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re
from businessCommon.createNotes import Create
from parameterized import parameterized


@class_case_log
class DeleteNoteContent(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    host = envConfig['host']
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    delete_note_url = host + dataConfig['interface']['DeleteNotesContent']['path']
    get_notes_url = host + f'/v3/notesvr/user/{userId1}/home/startindex/0/rows/999/notes'
    mustKey = dataConfig['interface']['DeleteNotesContent']['mustKey']
    base = dataConfig['interface']['DeleteNotesContent']['base']
    assertBase = {
      'responseTime': int
    }

    note_id_empty = [[{'noteId': '', 'code': 500}], [{'noteId': None, 'code': 500}]]
    x_user_key_empty = [[{'X-user-key': None, 'code': 412}], [{'X-user-key': '', 'code': 412}]]
    x_user_key_value = [[{'X-user-key': 'asd', 'code': 500}], [{'X-user-key': '-1557488247', 'code': 412}]]

    def setUp(self) -> None:
        Clear().clearNotesList(self.userId1, self.sid1)

    @parameterized.expand(mustKey)
    def testCase01(self, key):
        """必填项字段缺失校验"""
        step('PRE-STEP: 新增一条便签')
        Create().create_note(self.userId1, self.sid1, 1)

        step('PRE-STEP:获取首页便签列表')
        res1 = self.re.get(url=self.get_notes_url, sid=self.sid1, userId=self.userId1)
        print(res1.text)
        num = len(res1.json()['webNotes'])
        print(num)
        noteIds = []
        for i in range(num):
            noteId = res1.json()['webNotes'][i]['noteId']
            noteIds.append(noteId)

        step('STEP:删除便签的接口请求')
        body = {
            'noteId': noteIds[0]
        }
        body.pop(key)
        print(body)
        res = self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(note_id_empty)
    def testCase02(self, dic):
        """必填项字段缺失校验"""
        step('STEP:删除便签的接口请求')
        body = {
            'noteId': dic['noteId']
        }
        res = self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase03(self):
        """noteId过长校验"""
        step('STEP:删除便签的接口请求')
        body = {
            'noteId': '9999999999999999999999999999999999999999999999999999999999',
        }
        res = self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)
        if len(body['noteId']) > 32:
            res.status_code = 500
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase04(self):
        """noteId输入文字字母校验"""
        step('STEP:删除便签的接口请求')
        body = {
            'noteId': '你好abc'
        }
        res = self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase05(self):
        """noteId输入特殊字符校验"""
        step('STEP:删除便签的接口请求')
        body = {
            'noteId': '@&#……￥'
        }
        res = self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase06(self):
        """noteId输入‘ or ‘1=1校验"""
        step('STEP:删除便签的接口请求')
        body = {
            'noteId': "' or '1=1"
        }
        res = self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase07(self):
        """noteId输入" or "1=1校验"""
        step('STEP:删除便签的接口请求')
        body = {
            'noteId': '" or "1=1'
        }
        res = self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(x_user_key_empty)
    def testCase08(self, dic):
        """X-user-key枚举值-值为空校验"""
        step('STEP:删除便签的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': dic['X-user-key']
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
        }
        res = requests.post(url=self.delete_note_url, headers=headers, json=body)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -7, "errorMsg": "X-user-key header Requested!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase23(self):
        """X-user-key枚举值校验:X-user-key不存在"""
        step('STEP:删除便签的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': '24194159'
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
        }
        res = requests.post(url=self.delete_note_url, headers=headers, json=body)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(x_user_key_value)
    def testCase24(self, dic):
        """X-user-key枚举值校验:负数、字母文字特殊字符"""
        step('STEP:删除便签的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': dic['X-user-key']
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
        }
        res = requests.post(url=self.delete_note_url, headers=headers, json=body)
        self.assertEqual(dic['code'], res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase25(self):
        """身份校验-过期的wps_id"""
        step('STEP:删除便签的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid=V02SHoAtXgU_OhHVxg3RazDCWu-WR5Q00a0dd16b005cd56277',
            'X-user-key': '241941591'
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
        }
        res = requests.post(url=self.delete_note_url, headers=headers, json=body)
        self.assertEqual(401, res.status_code)
        expr = {"errorCode": -2010, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())

    def testCase26(self):
        """身份校验-非法的wps_id"""
        step('STEP:删除便签的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid=7867567eas092q90843=-=-==-=]\]\]\]',
            'X-user-key': '241941591'
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
        }
        res = requests.post(url=self.delete_note_url, headers=headers, json=body)
        self.assertEqual(401, res.status_code)
        expr = {"errorCode": -2009, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())

    def testCase27(self):
        """身份校验-wps_id缺失"""
        step('STEP:删除便签的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': '241941591'
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId',
        }
        res = requests.post(url=self.delete_note_url, headers=headers, json=body)
        self.assertEqual(401, res.status_code)
        expr = {"errorCode": -2009, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())


