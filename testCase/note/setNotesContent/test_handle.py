import time
import requests
import unittest
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re
from businessCommon.createNotes import Create


@class_case_log
class SetNotesContent(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    key = envConfig['key']
    iv = envConfig['iv']
    host = envConfig['host']
    userId1 = envConfig['userId1']
    userId2 = envConfig['userId2']
    sid1 = envConfig['sid1']
    sid2 = envConfig['sid2']
    dataConfig = YamlRead().data_config()
    url = host + dataConfig['interface']['SetNotesContent']['path']
    note_info_url = host + dataConfig['interface']['SetCommonNote']['path']
    get_notes_url = host + f'/v3/notesvr/user/{userId1}/home/startindex/0/rows/999/notes'
    delete_note_url = host + dataConfig['interface']['DeleteNotesContent']['path']
    clear_note_url = host + dataConfig['interface']['ClearNotes']['path']
    note_info_base = dataConfig['interface']['SetCommonNote']['base']
    note_base = dataConfig['interface']['SetNotesContent']['base']
    note_delete_base = dataConfig['interface']['DeleteNotesContent']['base']
    note_clear_base = dataConfig['interface']['ClearNotes']['base']
    assertBase = {
        'responseTime': int,
        'contentVersion': int,
        'contentUpdateTime': int
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
        info_version = res1.json()['webNotes'][0]['infoVersion']

        step('STEP:删除便签内容')
        body = self.note_delete_base
        body['noteId'] = noteIds[0]
        self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)

        step('STEP:新增便签内容的接口请求')
        body2 = self.note_base
        body2['noteId'] = noteIds[0]
        body2['title'] = 'title'
        body2['summary'] = 'summary'
        body2['body'] = 'body'
        body2['localContentVersion'] = info_version

        res2 = self.re.post(url=self.url, body=body2, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res2.status_code)
        expr = {"errorCode": -7, "errorMsg": ""}
        OutputCheck().assert_output(expr, res2.json())

    def testCase02(self):
        """存在便签数据被清空"""
        step('STEP: 新增便签内容')
        dic = Create().create_note(self.userId1, self.sid1, 1)

        step('STEP:删除便签数据')
        body = self.note_delete_base
        body['noteId'] = dic['noteIds'][0]
        res = self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)
        assert res.status_code == 200

        step('STEP:清空回收站下的便签接口请求')
        body1 = self.note_clear_base
        res1 = self.re.post(url=self.clear_note_url, body=body1, userId=self.userId1, sid=self.sid1)
        assert res1.status_code == 200

        step('STEP:新增便签内容的接口请求')
        body2 = self.note_base
        body2['noteId'] = dic['noteIds'][0]
        body2['title'] = 'title'
        body2['summary'] = 'summary'
        body2['body'] = 'body'
        body2['localContentVersion'] = dic['infoVersion'][0]

        res2 = self.re.post(url=self.url, body=body2, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res2.status_code)
        expr = {"errorCode": -7, "errorMsg": ""}
        OutputCheck().assert_output(expr, res2.json())

    def testCase03(self):
        """存在日历便签"""
        step('PRE-STEP:新增一条日历便签数据')
        dic = Create().create_mind_note(self.userId1, self.sid1, 1)
        print(dic)

        step('STEP:新增便签内容的接口请求')
        body2 = self.note_base
        body2['noteId'] = dic['noteIds'][0]
        body2['title'] = 'title'
        body2['summary'] = 'summary'
        body2['body'] = 'body'
        body2['localContentVersion'] = dic['infoVersion'][0]

        res2 = self.re.post(url=self.url, body=body2, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res2.status_code)
        expr = {"errorCode": -7, "errorMsg": ""}
        OutputCheck().assert_output(expr, res2.json())

    def testCase04(self):
        """存在分组下的便签"""
        step('PRE-STEP:新建一个分组下便签')
        groupIds = Create().create_group(self.userId1, self.sid1, 1)
        dic = Create().create_group_note(self.userId1, self.sid1, groupIds[0], 1)

        step('STEP:新增便签内容的接口请求')
        body2 = self.note_base
        body2['noteId'] = dic['noteIds'][0]
        body2['title'] = 'title'
        body2['summary'] = 'summary'
        body2['body'] = 'body'
        body2['localContentVersion'] = 1

        res2 = self.re.post(url=self.url, body=body2, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res2.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res2.json())

    def testCase05(self):
        """用户A上传 / 更新用户B的便签内容"""
        step('STEP:新增便签内容的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid2}',
            'X-user-key': self.userId1
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

    def testCase06(self):
        """重复数据"""
        step('PRE-STEP:新增便签主体')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': str(self.userId1)
        }
        for i in range(2):
            noteId = str(int(time.time() * 1000)) + '_noteId'
            body = {
                "noteId": noteId
            }

            res = requests.post(url=self.note_info_url, headers=headers, json=body)
            info_version = res.json()["infoVersion"]
            step('STEP:新增便签内容')
            body = {
                'noteId': noteId,
                'title': 'title',
                'summary': 'summary',
                'body': 'body',
                'localContentVersion': info_version,
                'BodyType': 0
            }
            res = requests.post(url=self.url, headers=headers, json=body)
            expr = self.assertBase
            OutputCheck().assert_output(expr, res.json())




