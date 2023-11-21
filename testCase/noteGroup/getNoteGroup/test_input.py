import unittest
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re
from businessCommon.createNotes import Create
from parameterized import parameterized


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
    optionKey = dataConfig['interface']['GetGroup']['optionKey']
    assertBase = {
        'requestTime': int,
        'noteGroups': [
            {
                'userId': str,
                'groupId': str,
                'groupName': str,
                'order': 0,
                'valid': int,
                'updateTime': int
            }
        ]
    }

    exclude_invalid_value = [[{'excludeInvalid': True, 'code': 500}], [{'excludeInvalid': False, 'code': 200}]]

    def setUp(self) -> None:
        Clear().clearNotesList(self.userId1, self.sid1)

    @parameterized.expand(optionKey)
    def testCase01(self, key):
        """非必填项字段缺失校验"""
        step('STEP:新增分组的接口请求')
        body = {
            'excludeInvalid': False
        }
        body.pop(key)
        print(body)
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(exclude_invalid_value)
    def testCase02(self, dic):
        """获取分组列表excludeInvalid枚举值校验"""
        step('STEP:新增分组的接口请求')
        body = {
            'excludeInvalid': dic['excludeInvalid']
        }
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())



