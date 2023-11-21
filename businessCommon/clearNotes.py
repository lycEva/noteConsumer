import requests
from common.yamlRead import YamlRead
import datetime
import time


class Clear:
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    host = envConfig['host']
    delete_note_url = host + dataConfig['interface']['DeleteNotesContent']['path']
    clear_note_url = host + dataConfig['interface']['ClearNotes']['path']
    get_remind_note_url = host + dataConfig['interface']['GetRemindNote']['path']



    def clearNotesList(self, userid, sid):
        """
        清空用户下所有便签功能
        :param userid: 用户id
        :param sid: 用户的sid
        :return: None
        """
        get_note_url = self.host + f'/v3/notesvr/user/{userid}/home/startindex/0/rows/999/notes'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(userid)
        }

        # 获取用户首页便签列表
        res = requests.get(url=get_note_url, headers=headers)
        note_ids = []
        for item in res.json()['webNotes']:
            note_ids.append(item['noteId'])

        # 删除便签
        for noteId in note_ids:
            body = {
                'noteId': noteId
            }
            res = requests.post(url=self.delete_note_url, headers=headers, json=body)
            assert res.status_code == 200

        # 清空回收站下的便签

        clear_body = {
            "noteIds": ['-1']
        }
        res = requests.post(url=self.clear_note_url, headers=headers, json=clear_body)
        assert res.status_code == 200

    def clearRemindNotes(self, userid, sid):
        """
        清空用户下所有日历便签功能
        :param userid: 用户id
        :param sid: 用户的sid
        :return: None
        """
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(userid)
        }

        # 获取日历便签
        body = self.dataConfig['interface']['GetRemindNote']['base']
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        body['remindStartTime'] = int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))
        body['remindEndTime'] = int(time.time())
        res = requests.post(url=self.get_remind_note_url, headers=headers, json=body)
        print(res.text)
        note_ids = []
        for item in res.json()['webNotes']:
            note_ids.append(item['noteId'])

        # 删除便签
        for noteId in note_ids:
            body = {
                'noteId': noteId
            }
            res = requests.post(url=self.delete_note_url, headers=headers, json=body)
            assert res.status_code == 200

        # 清空回收站下的便签

        clear_body = {
            "noteIds": ['-1']
        }
        res = requests.post(url=self.clear_note_url, headers=headers, json=clear_body)
        assert res.status_code == 200

    def clearGroupNote(self, userid, sid):
        """
        清空用户下所有分组便签功能
        :param userid: 用户id
        :param sid: 用户的sid
        :return: None
        """
        get_group_url = self.host + f'/v3/notesvr/user/{userid}/home/startindex/0/rows/999/notes'
        get_group_content_url = self.host + self.dataConfig['interface']['GetGroupNote']['path']
        delete_group_url = self.host + self.dataConfig['interface']['DeleteGroup']['path']
        get_group_content_base = self.dataConfig['interface']['GetGroupNote']['base']
        get_group_base = self.dataConfig['interface']['GetGroup']['base']
        delete_group_base = self.dataConfig['interface']['DeleteGroup']['base']

        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(userid)
        }

        # 获取分组列表
        body1 = get_group_base
        res1 = requests.post(url=get_group_url, headers=headers, json=body1)
        assert res1.status_code == 200

        group_ids = []
        for item in res1.json()['noteGroups']:
            group_ids.append(item['groupId'])

        # 查看分组下便签
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(userid)
        }
        noteIds = []
        for i in range(len(group_ids)):
            body2 = get_group_content_base
            body2['groupId'] = group_ids[i]
            res2 = requests.post(url=get_group_content_url, headers=headers, json=body2)
            assert res2.status_code == 200
            for a in range(len(res2.json()['webNotes'])):
                noteId = res2.json()['webNotes'][a]['noteId']
                noteIds.append(noteId)

        # 删除便签
        for b in noteIds:
            body3 = {
                'noteId': b
            }
            res3 = requests.post(url=self.delete_note_url, headers=headers, json=body3)
            assert res3.status_code == 200

        # 删除分组
        for c in range(len(group_ids)):
            body4 = delete_group_base
            body4['groupId'] = group_ids[c]
            res4 = requests.post(url=delete_group_url, headers=headers, json=body4)
            assert res4.status_code == 200

        # 清空回收站下的便签
        clear_body = {
            "noteIds": ['-1']
        }
        res5 = requests.post(url=self.clear_note_url, headers=headers, json=clear_body)
        assert res5.status_code == 200


if __name__ == '__main__':
    userId1 = '241941591'
    sid1 = 'V02SF9fkXCUADsJPrr7dCOVwdT-JjkQ00abedd08000e6bbc57'
    Clear().clearGroupNote(userId1, sid1)
