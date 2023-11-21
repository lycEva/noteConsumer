import unittest
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
    sid1 = envConfig['sid1']
    delete_note_url = host + dataConfig['interface']['DeleteNotesContent']['path']
    get_notes_url = host + f'/v3/notesvr/user/{userId1}/home/startindex/0/rows/999/notes'
    base = dataConfig['interface']['DeleteNotesContent']['base']
    assertBase = {
      'responseTime': int
    }

    def setUp(self) -> None:
        Clear().clearNotesList(self.userId1, self.sid1)

    def testCase_major(self):
        """删除便签主流程"""
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
        body = self.base
        body['noteId'] = noteIds[0]
        res = self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code, msg=f'状态码异常，返回体{res.text}')
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())
