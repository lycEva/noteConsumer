import requests
import time
from common.AESJIAMI import Aesjiami
from common.yamlRead import YamlRead


class Create:
    envConfig = YamlRead().env_config()
    host = envConfig['host']
    key = envConfig['key']
    iv = envConfig['iv']

    def create_group(self, userid, sid, num):
        """
        批量新增分组的方法
        :param userid: 用户id
        :param sid: 用户的sid
        :param num: 批量新增分组的数量
        :return: group_list 分组id列表
        """
        url = self.host + '/v3/notesvr/set/notegroup'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(userid)
        }
        group_list = []
        for i in range(num):
            groupId = str(int(time.time() * 1000)) + '_groupId'
            body = {
                'groupId': groupId,
                'groupName': 'Test'
            }
            res = requests.post(url=url, headers=headers, json=body)
            assert res.status_code == 200
            group_list.append(groupId)
        return group_list

    def create_group_note(self, userid, sid, groupId, num):
        """
        批量新增分组下便签的方法
        :param userid: 用户id
        :param sid: 用户的sid
        :param groupId: 分组id
        :param num: 新增分组下便签数量
        :return: noteIds 便签id列表
        """
        note_info_url = self.host + '/v3/notesvr/set/noteinfo'
        note_content_url = self.host + '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(userid)
        }
        dic = {'noteIds': [], 'groupIds': [], 'infoVersion': []}
        for i in range(num):
            # 新增便签主体
            noteId = str(int(time.time() * 1000)) + '_noteId'
            body = {
                "noteId": noteId,
                "groupId": groupId
            }

            res = requests.post(url=note_info_url, headers=headers, json=body)
            info_version = res.json()["infoVersion"]
            dic['groupIds'].append(groupId)

            # 新增分组下便签内容
            body = {
                'noteId': noteId,
                'title': Aesjiami().aes_encry('便签1', self.key, self.iv),
                'summary': Aesjiami().aes_encry('便签1摘要', self.key, self.iv),
                'body': Aesjiami().aes_encry('便签1内容', self.key, self.iv),
                'localContentVersion': info_version,
                'BodyType': 0
            }
            res = requests.post(url=note_content_url, headers=headers, json=body)
            assert res.status_code == 200
            dic['noteIds'].append(noteId)
            dic['infoVersion'].append(info_version)

        return dic

    def create_note(self, userid, sid, num):
        """
        批量新增便签的方法
        :param userid: 用户id
        :param sid: 用户的sid
        :param num: 新增便签数量
        :return: note_ids 便签id列表
        """
        note_info_url = self.host + '/v3/notesvr/set/noteinfo'
        note_content_url = self.host + '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(userid)
        }
        dic = {'noteIds': [], 'infoVersion': []}
        for i in range(num):
            # 新增便签主体
            noteId = str(int(time.time() * 1000)) + '_noteId'
            body = {
                "noteId": noteId
            }

            res = requests.post(url=note_info_url, headers=headers, json=body)
            info_version = res.json()['infoVersion']
            # 新增普通便签内容
            body = {
                'noteId': noteId,
                'title': Aesjiami().aes_encry('便签1', self.key, self.iv),
                'summary': Aesjiami().aes_encry('便签1摘要', self.key, self.iv),
                'body': Aesjiami().aes_encry('便签1内容', self.key, self.iv),
                'localContentVersion': info_version,
                'BodyType': 0
            }
            res = requests.post(url=note_content_url, headers=headers, json=body)
            assert res.status_code == 200
            dic['noteIds'].append(noteId)
            dic['infoVersion'].append(info_version)

        return dic

    def create_mind_note(self, userid, sid, num):
        """
        批量新增日历便签的方法
        :param userid: 用户id
        :param sid: 用户的sid
        :param num: 新增日历便签数量
        :return: note_ids 便签id列表
        """
        note_info_url = self.host + '/v3/notesvr/set/noteinfo'
        note_content_url = self.host + '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(userid)
        }
        dic = {'noteIds': [], 'contentUpdateTime': [], 'infoVersion': []}
        for i in range(num):
            # 新增便签主体
            noteId = str(int(time.time() * 1000)) + '_noteId'
            body = {
                "noteId": noteId,
                "remindTime": str(int(time.time()) * 1000),
                "remindType": 0
            }

            res = requests.post(url=note_info_url, headers=headers, json=body)
            info_version = res.json()["infoVersion"]
            # 新增日历便签内容
            body = {
                'noteId': noteId,
                'title': Aesjiami().aes_encry('便签1', self.key, self.iv),
                'summary': Aesjiami().aes_encry('便签1摘要', self.key, self.iv),
                'body': Aesjiami().aes_encry('便签1内容', self.key, self.iv),
                'localContentVersion': info_version,
                'BodyType': 0
            }
            res = requests.post(url=note_content_url, headers=headers, json=body)
            contentUpdateTime = res.json()['contentUpdateTime']
            assert res.status_code == 200
            dic['noteIds'].append(noteId)
            dic['contentUpdateTime'].append(contentUpdateTime)
            dic['infoVersion'].append(info_version)

        return dic


if __name__ == '__main__':
    userId1 = '241941591'
    sid1 = 'V02SF9fkXCUADsJPrr7dCOVwdT-JjkQ00abedd08000e6bbc57'
    Create().create_note(userid=userId1, sid=sid1, num=1)
    group_id = Create().create_group(userid=userId1, sid=sid1, num=1)
    Create().create_group_note(userid=userId1, sid=sid1, groupId=group_id[0], num=1)
