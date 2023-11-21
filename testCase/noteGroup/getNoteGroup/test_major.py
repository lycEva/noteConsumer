import unittest
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re
from businessCommon.createNotes import Create


@class_case_log
class GetNoteGroup(unittest.TestCase):
    re = Re()
    envConfig = YamlRead.env_config()
    dataConfig = YamlRead.data_config()
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    url = host + dataConfig['interface']['GetGroup']['path']
    base = dataConfig['interface']['GetGroup']['base']
    assertBase = {
        'requestTime': int,
        'noteGroups': [
            {
                'userId': '',
                'groupId': str,
                'groupName': str,
                'order': 0,
                'valid': int,
                'updateTime': int
            }
        ]
    }

    def setUp(self):
        Clear().clearNotesList(self.userId1, self.sid1)

    def testCase_major(self):
        """获取分组列表主流程"""
        step('PRE-STEP:新增分组')
        groupIds = Create().create_group(self.userId1, self.sid1, 1)

        step('STEP:获取分组列表')
        body = self.base
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code, msg=f'状态码异常，返回体{res.text}')

        for i in range(0, 2):
            userId = res.json()['noteGroups'][-i]['userId']
            groupId = res.json()['noteGroups'][-i]['groupId']
            self.assertIn(userId, self.userId1)
            self.assertIn(groupId, groupIds)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())
