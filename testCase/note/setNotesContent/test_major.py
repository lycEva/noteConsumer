import unittest
import time
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.AESJIAMI import Aesjiami
from common.caseLog import step, class_case_log
from businessCommon.res import Re


@class_case_log
class SetNotesContent(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    key = envConfig['key']
    iv = envConfig['iv']
    host = envConfig['host']
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    dataConfig = YamlRead().data_config()
    url = host + dataConfig['interface']['SetNotesContent']['path']
    note_info_url = host + dataConfig['interface']['SetCommonNote']['path']
    note_base = dataConfig['interface']['SetNotesContent']['base']
    note_info_base = dataConfig['interface']['SetCommonNote']['base']
    assertBase = {
        'responseTime': int,
        'contentVersion': int,
        'contentUpdateTime': int
    }

    def setUp(self):
        Clear().clearNotesList(self.userId1, self.sid1)

    def testCase_major(self):
        """新增普便签内容主流程"""
        step('PRE-STEP:新建普通便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body1 = self.note_info_base
        body1['noteId'] = noteId

        res1 = self.re.post(url=self.note_info_url, body=body1, userId=self.userId1, sid=self.sid1)
        info_version = res1.json()["infoVersion"]

        step('STEP: 新增便签内容')
        title = Aesjiami().aes_encry('便签1', self.key, self.iv)
        summary = Aesjiami().aes_encry('便签1摘要', self.key, self.iv)
        body = Aesjiami().aes_encry('便签1内容', self.key, self.iv)
        body2 = self.note_base
        body2['noteId'] = noteId
        body2['title'] = title
        body2['summary'] = summary
        body2['body'] = body
        body2['localContentVersion'] = info_version

        res2 = self.re.post(url=self.url, body=body2, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res2.status_code, msg=f'状态码异常，返回体{res2.text}')
        expr = self.assertBase
        OutputCheck().assert_output(expr, res2.json())
