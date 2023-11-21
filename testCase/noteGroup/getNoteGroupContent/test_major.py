import unittest
from businessCommon.createNotes import Create
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re


@class_case_log
class GetNoteGroupPage(unittest.TestCase):
    re = Re()
    envConfig = YamlRead.env_config()
    dataConfig = YamlRead.data_config()
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    url = host + dataConfig['interface']['GetGroupNote']['path']
    base = dataConfig['interface']['GetGroupNote']['base']
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
                'groupId': '',
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
        """查看分组下便签主流程"""
        step('PRE-STEP:新建一个分组下便签')
        groupIds = Create().create_group(self.userId1, self.sid1, 1)
        noteIds = Create().create_group_note(self.userId1, self.sid1, groupIds[0], 1)
        step('STEP: 查看分组下便签的接口请求')
        body = self.base
        body['groupId'] = groupIds[0]
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code, msg=f'状态码异常，返回体{res.text}')
        expr = self.assertBase
        expr['webNotes'][0]['noteId'] = noteIds[0]
        expr['webNotes'][0]['groupId'] = groupIds[0]
        OutputCheck().assert_output(expr, res.json())
