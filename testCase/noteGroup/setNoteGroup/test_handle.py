import unittest
import requests
import time
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re
from parameterized import parameterized
from businessCommon.createNotes import Create


@class_case_log
class SetNoteGroup(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    key = envConfig['key']
    iv = envConfig['iv']
    userId1 = envConfig['userId1']
    userId2 = envConfig['userId2']
    sid1 = envConfig['sid1']
    sid2 = envConfig['sid2']
    host = envConfig['host']
    dataConfig = YamlRead().data_config()
    url = host + dataConfig['interface']['SetGroupNote']['path']
    delete_group_url = host + dataConfig['interface']['DeleteGroup']['path']
    delete_note_url = host + dataConfig['interface']['DeleteNotesContent']['path']
    clear_note_url = host + dataConfig['interface']['ClearNotes']['path']
    base = dataConfig['interface']['SetGroupNote']['base']
    delete_group_base = dataConfig['interface']['DeleteGroup']['base']
    note_delete_base = dataConfig['interface']['DeleteNotesContent']['base']
    note_clear_base = dataConfig['interface']['ClearNotes']['base']
    assertBase = {
        'responseTime': int,
        'updateTime': int
    }

    def setUp(self) -> None:
        Clear().clearNotesList(self.userId1, self.sid1)

    def testCase01(self):
        """存在分组被删除"""
        step('PRE-STEP: 新增1个分组')
        group_list = Create().create_group(self.userId1, self.sid1, 1)

        step('STEP:删除分组')
        body = self.delete_group_base
        body['groupId'] = group_list[0]
        self.re.post(url=self.delete_group_url, body=body, userId=self.userId1, sid=self.sid1)

        step('STEP:新增分组的接口请求')
        body1 = self.base
        body1['groupId'] = group_list[0]
        body1['groupName'] = 'groupName'

        res1 = self.re.post(url=self.url, body=body1, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res1.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res1.json())

    def testCase02(self):
        """存在分组便签被清空"""
        step('PRE-STEP: 新增1个分组便签')
        groupId = str(int(time.time()) * 1000) + '_groupId'
        dic = Create().create_group_note(self.userId1, self.sid1, groupId, 1)

        step('STEP:删除分组下便签数据')
        body = self.note_delete_base
        body['noteId'] = dic['noteIds'][0]
        res = self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)
        assert res.status_code == 200

        step('STEP:删除分组')
        body = self.delete_group_base
        body['groupId'] = dic['groupIds'][0]
        self.re.post(url=self.delete_group_url, body=body, userId=self.userId1, sid=self.sid1)

        step('STEP:清空回收站下的便签接口请求')
        body1 = self.note_clear_base
        res1 = self.re.post(url=self.clear_note_url, body=body1, userId=self.userId1, sid=self.sid1)
        assert res1.status_code == 200

        step('STEP:新增分组的接口请求')
        body1 = self.base
        body1['groupId'] = dic['groupIds'][0]
        body1['groupName'] = 'groupName'

        res1 = self.re.post(url=self.url, body=body1, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res1.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res1.json())

    def testCase03(self):
        """存在日历便签"""
        step('PRE-STEP:新增一条日历便签数据')
        Create().create_mind_note(self.userId1, self.sid1, 1)

        step('STEP:新增分组的接口请求')
        body1 = self.base
        body1['groupId'] = str(int(time.time()) * 1000) + '_groupId'
        body1['groupName'] = 'groupName'

        res1 = self.re.post(url=self.url, body=body1, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res1.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res1.json())

    def testCase04(self):
        """存在分组"""
        step('PRE-STEP: 新增1个分组')
        group_list = Create().create_group(self.userId1, self.sid1, 1)

        step('STEP:新增分组的接口请求')
        body = self.base
        body['groupId'] = group_list[0]
        body['groupName'] = 'groupName'

        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(400, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "分组已存在!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase05(self):
        """用户A新增用户B的分组"""
        step('STEP:新增分组的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid2}',
            'X-user-key': self.userId1
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

    def testCase06(self):
        """重复数据"""
        step('STEP:新增分组的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': str(self.userId1)
        }
        for i in range(2):
            groupId = str(int(time.time() * 1000)) + '_groupId'
            body = {
                'groupId': str(int(time.time()) * 1000) + '_groupId',
                'groupName': 'groupName',
                'order': 0
            }
            res = requests.post(url=self.url, headers=headers, json=body)
            expr = self.assertBase
            OutputCheck().assert_output(expr, res.json())

