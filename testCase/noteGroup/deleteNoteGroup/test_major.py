import unittest
from businessCommon.createNotes import Create
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re


@class_case_log
class DeleteNoteGroup(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead.data_config()
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    url = host + dataConfig['interface']['DeleteGroup']['path']
    base = dataConfig['interface']['DeleteGroup']['base']
    assertBase = {
        'responseTime': int
    }

    def setUp(self):
        Clear().clearNotesList(self.userId1, self.sid1)

    def testCase_major(self):
        """删除分组主流程"""
        step('PRE-STEP:新增分组')
        groupIds = Create().create_group(self.userId1, self.sid1, 1)

        step('STEP:删除分组')
        body = self.base
        body['groupId'] = groupIds[0]
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code, msg=f'状态码异常，返回体{res.text}')
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())
