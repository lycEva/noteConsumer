import requests
import json
from common.yamlRead import YamlRead
envConfig = YamlRead().env_config()
userid = envConfig['userid']
host = envConfig['host']
content_type = envConfig['Content-Type'],
x_user_key = envConfig['X-user-key'],
cookie = envConfig['Cookie']
startindex = 0
rows = 9999
path = f'/v3/notesvr/user/{userid}/invalid/startindex/{startindex}/rows/{rows}/notes'
url = host + path
headers = {
    'Cookie': cookie
}
res = requests.get(url=url, headers=headers)
print(res.status_code)
text1 = json.loads(res.text)
print(text1)
print(type(text1))
noteIds = []
for i in range(len(text1)):
    noteId = text1["webNotes"][i]['noteId']
    print(noteId)
    noteIds = noteIds.append(noteId)
print(noteIds)