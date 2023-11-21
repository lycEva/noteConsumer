import unittest
import time
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re


@class_case_log
class SetNotes(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    host = envConfig['host']
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    url = host + dataConfig['interface']['SetCommonNote']['path']
    base = dataConfig['interface']['SetCommonNote']['base']
    assertBase = {
        'responseTime': int,
        'infoVersion': int,
        'infoUpdateTime': int
    }

    def setUp(self):
        Clear().clearNotesList(self.userId1, self.sid1)

    def testCase_major(self):
        """新增便签主体主流程"""
        step('PRE-STEP:新建普通便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = self.base
        body['noteId'] = noteId

        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code, msg=f'状态码异常，返回体{res.text}')
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())
