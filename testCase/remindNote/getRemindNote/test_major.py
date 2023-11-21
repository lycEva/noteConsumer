import time
import unittest
from businessCommon.createNotes import Create
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re


@class_case_log
class GetRemindNote(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    url = host + dataConfig['interface']['GetRemindNote']['path']
    base = dataConfig['interface']['GetRemindNote']['base']

    assertBase = {
        'responseTime': int,
        'webNotes': [
            {
                'noteId': str,
                'createTime': int,
                'star': 0,
                'remindTime': int,
                'remindType': int,
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
        Clear().clearRemindNotes(self.userId1, self.sid1)

    def testCase_major(self):
        """查看日历下便签主流程"""

        step('PRE-STEP:新增2条日历便签数据')
        dic = Create().create_mind_note(self.userId1, self.sid1, 1)
        print(dic)

        step('STEP:获取日历便签接口请求')
        body = self.base
        noteIds = dic['noteIds']
        body['remindStartTime'] = dic['contentUpdateTime'][0]
        body['remindEndTime'] = int(time.time() * 1000)
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code, msg=f'状态码异常，返回体{res.text}')
        for i in range(2):
            noteId = res.json()['webNotes'][i]['noteId']
            self.assertIn(noteId, noteIds)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())
