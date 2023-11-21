import unittest
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re
from businessCommon.createNotes import Create


@class_case_log
class GetDeleteNote(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead.data_config()
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    url = host + f'/v3/notesvr/user/{userId1}/invalid/startindex/0/rows/999/notes'
    delete_note_url = host + dataConfig['interface']['DeleteNotesContent']['path']
    delete_note_base = dataConfig['interface']['DeleteNotesContent']['base']
    assertBase = {
        'responseTime': int,
        'webNotes': [
            {
                'noteId': '',
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

    def setUp(self):
        Clear().clearNotesList(self.userId1, self.sid1)

    def testCase_major(self):
        """查看回收站下的便签列表主流程"""
        step('PRE-STEP: 新增一条便签')
        noteIds = Create().create_note(self.userId1, self.sid1, 1)
        print(noteIds)

        step('PRE-STEP:删除便签数据')
        body = self.delete_note_base
        body['noteId'] = noteIds[0]
        res1 = self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)
        assert res1.status_code == 200

        step('STEP: 查看回收站下便签列表接口请求')
        res = self.re.get(url=self.url, sid=self.sid1, userId=self.userId1)
        self.assertEqual(200, res.status_code, msg=f'状态码异常，返回体{res.text}')
        expr = self.assertBase
        expr['webNotes'][0]['noteId'] = noteIds[0]
        OutputCheck().assert_output(expr, res.json())
