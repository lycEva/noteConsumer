import unittest
import requests
import time
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re
from parameterized import parameterized
from businessCommon.createNotes import Create


@class_case_log
class GetNotePage(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    host = envConfig['host']
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    dataConfig = YamlRead().data_config()

    mustKey = dataConfig['interface']['GetNotes']['mustKey']
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

    def setUp(self) -> None:
        Clear().clearNotesList(self.userId1, self.sid1)

    @parameterized.expand(mustKey)
    def testCase01(self, key):
        """必填项字段缺失校验"""
        dic = {
            'userid': self.userId1,
            'startindex': 0,
            'rows': 999
        }
        url = self.host + f'/v3/notesvr/user/{userid}/home/startindex/{startindex}/rows/{rows}/notes'
        step('PRE-STEP: 新增2条便签')
        Create().create_note(self.userId1, self.sid1, 2)
        step('STEP:获取首页便签的接口请求')
        dic.pop(key)
        print(dic)
        res = self.re.get(url=url, sid=self.sid1, userId=self.userId1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())
