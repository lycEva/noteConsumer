import unittest
import requests
import time
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re
from businessCommon.createNotes import Create


@class_case_log
class DeleteNoteContent(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    host = envConfig['host']
    userId1 = envConfig['userId1']
    userId2 = envConfig['userId2']
    sid1 = envConfig['sid1']
    sid2 = envConfig['sid2']
    delete_note_url = host + dataConfig['interface']['DeleteNotesContent']['path']
    clear_note_url = host + dataConfig['interface']['ClearNotes']['path']
    get_notes_url = host + f'/v3/notesvr/user/{userId1}/home/startindex/0/rows/999/notes'
    note_delete_base = dataConfig['interface']['DeleteNotesContent']['base']
    note_clear_base = dataConfig['interface']['ClearNotes']['base']

    assertBase = {
      'responseTime': int
    }

    def setUp(self) -> None:
        Clear().clearNotesList(self.userId1, self.sid1)

    def testCase01(self):
        """存在便签数据被删除"""
        step('PRE-STEP: 新增两条便签')
        Create().create_note(self.userId1, self.sid1, 2)

        step('PRE-STEP:获取首页便签列表')
        res1 = self.re.get(url=self.get_notes_url, sid=self.sid1, userId=self.userId1)
        print(res1.text)
        num = len(res1.json()['webNotes'])
        print(num)
        noteIds = []
        for i in range(num):
            noteId = res1.json()['webNotes'][i]['noteId']
            noteIds.append(noteId)

        step('PRE-STEP:删除便签')
        body = self.note_delete_base
        body['noteId'] = noteIds[0]
        self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)

        step('STEP:删除便签的接口请求')
        body2 = self.note_delete_base
        body2['noteId'] = noteIds[0]
        res2 = self.re.post(url=self.delete_note_url, body=body2, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res2.status_code)
        expr = {"errorCode": -7, "errorMsg": ""}
        OutputCheck().assert_output(expr, res2.json())

    def testCase02(self):
        """存在便签数据被清空"""
        step('PRE-STEP: 新增便签内容')
        dic = Create().create_note(self.userId1, self.sid1, 1)

        step('PRE-STEP:删除便签数据')
        body = self.note_delete_base
        body['noteId'] = dic['noteIds'][0]
        res = self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)
        assert res.status_code == 200

        step('PRE-STEP:清空回收站下的便签')
        body1 = self.note_clear_base
        res1 = self.re.post(url=self.clear_note_url, body=body1, userId=self.userId1, sid=self.sid1)
        assert res1.status_code == 200

        step('STEP:删除便签的接口请求')
        body2 = self.note_delete_base
        body2['noteId'] = dic['noteIds'][0]
        res2 = self.re.post(url=self.delete_note_url, body=body2, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res2.status_code)
        expr = {"errorCode": -7, "errorMsg": ""}
        OutputCheck().assert_output(expr, res2.json())

    def testCase03(self):
        """存在日历便签"""
        step('PRE-STEP:新增一条日历便签数据')
        dic = Create().create_mind_note(self.userId1, self.sid1, 1)
        print(dic)

        step('STEP:删除便签的接口请求')
        body = self.note_delete_base
        body['noteId'] = dic['noteIds'][0]
        res = self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    def testCase04(self):
        """存在分组下的便签"""
        step('PRE-STEP:新建一个分组下便签')
        groupIds = Create().create_group(self.userId1, self.sid1, 1)
        dic = Create().create_group_note(self.userId1, self.sid1, groupIds[0], 1)

        step('STEP:删除便签的接口请求')
        body = self.note_delete_base
        body['noteId'] = dic['noteIds'][0]
        res = self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    def testCase05(self):
        """用户A上传 / 更新用户B的便签内容"""
        step('PRE-STEP: 新增两条便签')
        Create().create_note(self.userId1, self.sid1, 2)

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
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid2}',
            'X-user-key': self.userId1
        }
        body = {
            'noteId': noteIds[0]
        }
        res = requests.post(url=self.delete_note_url, headers=headers, json=body)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())
