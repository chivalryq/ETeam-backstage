import json
import requests
import datetime
APPID="wxb285604f36464d54"
SECRET="509ea2cb21d08d34b4ad47156e56c8d3"

def getuserinfo(code):
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (
    APPID, SECRET, code)
    response = requests.get(url)


    if response.status_code == 200:
        info = response.text
        return json.loads(info)

    else:
        #info = response.text
        file = open('log', 'a+')
        file.write(str(datetime.datetime.now())+'response.status_code=>'+response.status_code+'\n')
        file.close()
