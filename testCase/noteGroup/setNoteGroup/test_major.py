import time
import unittest
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re
from common.AESJIAMI import Aesjiami


@class_case_log
class SetNoteGroup(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    key = envConfig['key']
    iv = envConfig['iv']
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    dataConfig = YamlRead().data_config()
    url = host + dataConfig['interface']['SetGroupNote']['path']
    base = dataConfig['interface']['SetGroupNote']['base']
    assertBase = {
        'responseTime': int,
        'updateTime': int
    }

    def setUp(self) -> None:
        Clear().clearNotesList(self.userId1, self.sid1)

    def testCase_major(self):
        """新增分组主流程"""
        step('STEP:新增分组')
        groupId = str(int(time.time()) * 1000) + '_groupId'
        groupName = Aesjiami().aes_encry('分组1', self.key, self.iv)
        body = self.base
        body['groupId'] = groupId
        body['groupName'] = groupName

        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code, msg=f'状态码异常，返回体{res.text}')
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())
