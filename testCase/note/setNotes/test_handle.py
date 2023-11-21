import time
import requests
import unittest
from common.yamlRead import YamlRead
from common.outputCheck import OutputCheck
from businessCommon.clearNotes import Clear
from common.caseLog import step, class_case_log
from businessCommon.res import Re
from businessCommon.createNotes import Create
from parameterized import parameterized


@class_case_log
class SetNotes(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    host = envConfig['host']
    userId1 = envConfig['userId1']
    userId2 = envConfig['userId2']
    sid1 = envConfig['sid1']
    sid2 = envConfig['sid2']
    url = host + dataConfig['interface']['SetCommonNote']['path']
    get_notes_url = host + f'/v3/notesvr/user/{userId1}/home/startindex/0/rows/999/notes'
    delete_note_url = host + dataConfig['interface']['DeleteNotesContent']['path']
    clear_note_url = host + dataConfig['interface']['ClearNotes']['path']
    base = dataConfig['interface']['SetCommonNote']['base']
    note_delete_base = dataConfig['interface']['DeleteNotesContent']['base']
    note_clear_base = dataConfig['interface']['ClearNotes']['base']
    mustKey = dataConfig['interface']['SetCommonNote']['mustKey']
    assertBase = {
        'responseTime': int,
        'infoVersion': int,
        'infoUpdateTime': int
    }
    star_value = [[{'star': 1, 'code': 200}], [{'star': 0, 'code': 200}], [{'star': None, 'code': 200}]]
    remind_type_value = [[{'remindType': 0, 'code': 200}], [{'remindType': 1, 'code': 200}], [{'remindType': 2, 'code': 200}]]

    def setUp(self) -> None:
        Clear().clearNotesList(self.userId1, self.sid1)

    def testCase01(self):
        """存在便签数据被删除"""
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

        step('STEP:删除便签')
        body = self.note_delete_base
        body['noteId'] = noteIds[0]
        self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)

        step('STEP:新增便签主体的接口请求')
        body = self.base
        body['noteId'] = noteIds[0]
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())

    def testCase02(self):
        """存在便签数据被清空"""
        step('STEP: 新增便签内容')
        dic = Create().create_note(self.userId1, self.sid1, 1)

        step('STEP:删除便签数据')
        body = self.note_delete_base
        body['noteId'] = dic['noteIds'][0]
        res = self.re.post(url=self.delete_note_url, body=body, userId=self.userId1, sid=self.sid1)
        assert res.status_code == 200

        step('STEP:清空回收站下的便签接口请求')
        body1 = self.note_clear_base
        res1 = self.re.post(url=self.clear_note_url, body=body1, userId=self.userId1, sid=self.sid1)
        assert res1.status_code == 200

        step('STEP:新增便签主体的接口请求')
        body = self.base
        body['noteId'] = dic['noteIds'][0]

        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())

    def testCase03(self):
        """存在日历便签"""
        step('PRE-STEP:新增一条日历便签数据')
        dic = Create().create_mind_note(self.userId1, self.sid1, 1)
        print(dic)

        step('STEP:新增便签主体的接口请求')
        body = self.base
        body['noteId'] = dic['noteIds'][0]

        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": ""}
        OutputCheck().assert_output(expr, res.json())

    def testCase04(self):
        """存在分组下的便签"""
        step('PRE-STEP:新建一个分组下便签')
        groupIds = Create().create_group(self.userId1, self.sid1, 1)
        dic = Create().create_group_note(self.userId1, self.sid1, groupIds[0], 1)

        step('STEP:新增便签主体的接口请求')
        body = self.base
        body['noteId'] = dic['noteIds'][0]
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    def testCase05(self):
        """用户A上传 / 更新用户B的便签主体"""
        step('STEP:新增便签内容的接口请求')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid2}',
            'X-user-key': self.userId1
        }
        body = {
            'noteId': str(int(time.time()) * 1000) + '_noteId'
        }
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase06(self):
        """重复数据"""
        step('PRE-STEP:新增便签主体')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid1}',
            'X-user-key': str(self.userId1)
        }
        for i in range(2):
            noteId = str(int(time.time() * 1000)) + '_noteId'
            body = {
                "noteId": noteId
            }
            res = requests.post(url=self.url, headers=headers, json=body)
            expr = self.assertBase
            OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(star_value)
    def testCase07(self, dic):
        """存在1条标星便签主体枚举值遍历"""
        step('PRE-STEP:新增一条标星便签主体')
        body = self.base
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body['noteId'] = noteId
        body['star'] = 1
        self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)

        step('STEP:更新便签主体的接口请求')
        body1 = self.base
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body1['noteId'] = noteId
        body1['star'] = dic['star']
        res1 = self.re.post(url=self.url, body=body1, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res1.status_code, msg=f'状态码异常，返回体{res1.text}')
        expr = self.assertBase
        OutputCheck().assert_output(expr, res1.json())

    @parameterized.expand(star_value)
    def testCase08(self, dic):
        """存在0条标星便签主体枚举值遍历"""
        step('PRE-STEP:新增一条标星便签主体')
        body = self.base
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body['noteId'] = noteId
        self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)

        step('STEP:更新便签主体的接口请求')
        body1 = self.base
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body1['noteId'] = noteId
        body1['star'] = dic['star']
        res1 = self.re.post(url=self.url, body=body1, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res1.status_code, msg=f'状态码异常，返回体{res1.text}')
        expr = self.assertBase
        OutputCheck().assert_output(expr, res1.json())

    @parameterized.expand(remind_type_value)
    def testCase09(self, dic):
        """存在提醒1次的便签主体"""
        step('PRE-STEP:新增一条提醒1次的便签主体')
        body = self.base
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body['noteId'] = noteId
        body['remindTime'] = str(int(time.time() * 1000))
        body['remindType'] = 1
        self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)

        step('STEP:更新便签主体的接口请求')
        body1 = self.base
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body1['noteId'] = noteId
        body1['remindTime'] = str(int(time.time() * 1000))
        body1['remindType'] = dic['remindType']
        res1 = self.re.post(url=self.url, body=body1, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res1.status_code, msg=f'状态码异常，返回体{res1.text}')
        expr = self.assertBase
        OutputCheck().assert_output(expr, res1.json())

    @parameterized.expand(remind_type_value)
    def testCase10(self, dic):
        """存在已经提醒的便签主体"""
        step('PRE-STEP:新增一条已经提醒的便签主体')
        body = self.base
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body['noteId'] = noteId
        body['remindTime'] = str(int(time.time() * 1000))
        body['remindType'] = 2
        self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)

        step('STEP:更新便签主体的接口请求')
        body1 = self.base
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body1['noteId'] = noteId
        body1['remindTime'] = str(int(time.time() * 1000))
        body1['remindType'] = dic['remindType']
        res1 = self.re.post(url=self.url, body=body1, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res1.status_code, msg=f'状态码异常，返回体{res1.text}')
        expr = self.assertBase
        OutputCheck().assert_output(expr, res1.json())

    @parameterized.expand(remind_type_value)
    def testCase11(self, dic):
        """存在不提醒的便签主体"""
        step('PRE-STEP:新增一条已经提醒的便签主体')
        body = self.base
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body['noteId'] = noteId
        body['remindTime'] = str(int(time.time() * 1000))
        self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)

        step('STEP:更新便签主体的接口请求')
        body1 = self.base
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body1['noteId'] = noteId
        body1['remindTime'] = str(int(time.time() * 1000))
        body1['remindType'] = dic['remindType']
        res1 = self.re.post(url=self.url, body=body1, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res1.status_code, msg=f'状态码异常，返回体{res1.text}')
        expr = self.assertBase
        OutputCheck().assert_output(expr, res1.json())

    @parameterized.expand(remind_type_value)
    def testCase12(self, dic):
        """不存在便签主体"""
        step('STEP:新增便签主体的接口请求')
        body = self.base
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body['noteId'] = noteId
        body['remindTime'] = str(int(time.time() * 1000))
        body['remindType'] = dic['remindType']
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(dic['code'], res.status_code, msg=f'状态码异常，返回体{res.text}')
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())








