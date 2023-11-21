import json
import unittest
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.createNotes import Create
from businessCommon.clearNotes import Clear
from businessCommon.res import Re
from common.caseLog import step, class_case_log


@class_case_log
class GetNotePage(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    host = envConfig['host']
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    dataConfig = YamlRead().data_config()
    url = host + f'/v3/notesvr/user/{userId1}/home/startindex/0/rows/999/notes'
    assertBase = {
        'responseTime': int,
        'webNotes': [
            {
                'noteId': str,
                'createTime': int,
                'star': 0,
                'remindTime': 0,
                'remindType': 0,
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

    def setUp(self) -> None:
        Clear().clearNotesList(self.userId1, self.sid1)

    def testCase_major(self):
        """获取首页便签列表主流程"""
        step('PRE-STEP: 新增2条便签')
        dic = Create().create_note(self.userId1, self.sid1, 2)
        noteIds = dic['noteIds']
        step('STEP: 查看列表下便签的接口请求')
        res = self.re.get(url=self.url, sid=self.sid1, userId=self.userId1)
        self.assertEqual(200, res.status_code, msg=f'状态码异常，返回体{res.text}')
        for i in range(2):
            noteId = res.json()['webNotes'][i]['noteId']
            self.assertIn(noteId, noteIds)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())
