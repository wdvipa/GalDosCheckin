# -*- coding: utf-8 -*-
"""
//更新时间：2023/10/26
//作者：wdvipa
//支持青龙和actions定时执行
//使用方法：创建变量 名字：glados 内容的写法：Cookie  多个账号用回车键隔开
//例如:
koa:sess=xxx;koa:sess.sig=xxx;
koa:sess=xxx;koa:sess.sig=xxx;
//更新内容：支持青龙执行，因pushplus需要实名，所以增加息知推送
//如需推送将需要的推送写入变量glados_fs即可多个用&隔开
如:变量内输入push需再添加glados_push变量 内容是push的token即可
"""
import requests
import os
import time
import re
import json

requests.urllib3.disable_warnings()

# ------------------设置-------------------
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26'

# 初始化环境变量开头
cs = 0
ZData = "5"
ttoken = ""
tuserid = ""
push_token = ""
xizhi_token = ""
SKey = ""
QKey = ""
ktkey = ""
msgs = ""
datas = ""
message = ""
# 检测推送
if cs == 1:
    if "cs_glados" in os.environ:
        datas = os.environ.get("cs_glados")
    else:
        print('您没有输入任何信息')
        exit
elif cs == 2:
    datas = ""
else:
    if "glados_fs" in os.environ:
        fs = os.environ.get('glados_fs')
        fss = fs.split("&")
        if "tel" in fss:
            if "glados_telkey" in os.environ:
                telekey = os.environ.get("glados_telkey")
                telekeys = telekey.split('\n')
                ttoken = telekeys[0]
                tuserid = telekeys[1]
        if "qm" in fss:
            if "glados_qkey" in os.environ:
                QKey = os.environ.get("glados_qkey")
        if "stb" in fss:
            if "glados_skey" in os.environ:
                SKey = os.environ.get("glados_skey")
        if "push" in fss:
            if "glados_push" in os.environ:
                push_token = os.environ.get("glados_push")
        if "xizhi" in fss:
            if "glados_xizhi" in os.environ:
                push_token = os.environ.get("glados_xizhi")
        if "kt" in fss:
            if "glados_ktkey" in os.environ:
                ktkey = os.environ.get("glados_ktkey")
    if "glados" in os.environ:
        datas = os.environ.get("glados")
    else:
        print('您没有输入任何信息')
        exit
groups = datas.split('\n')


# 初始化环境变量结尾

class gladosanelQd(object):
    def __init__(self, cookie):
        # Authorization
        self.ck = ck
        self.checkReturn = ""
        self.signReturn = ""

    def buildHeaders(self, cookie):  # 更改cookie
        session.headers["Cookie"] = cookie

    def status(self):  # 验证
        url = "https://glados.rocks/api/user/status"
        payload = ""
        response = session.request("GET", url, data=payload)
        print(response.text)
        return response

    def sign(self):  # 签到
        url = "https://glados.rocks/api/user/checkin"
        payload = "{\"token\":\"glados.one\"}"
        response = session.request("POST", url, data=payload)
        print(response.text)
        return response

    def main(self):
        global msgs
        # 更新cookie
        self.buildHeaders(self.ck)
        # 每日签到
        self.signReturn = self.sign()
        timeday = ""
        email = ""
        sign_msg = ""
        state = self.status()
        timeday = state.json()['data']['leftDays'].split('.')[0]
        email = state.json()['data']['email']
        if 'message' in self.signReturn.text:
            sign_msg = self.signReturn.json()["message"]
            if sign_msg == "Checkin Repeats! Please Try Tomorrow":
                sign_msg = "重复签到，请明日再试"
        else:
            sign_msg = "签到失败"
        message = '''⏰当前时间：{} 
        GlaDos签到
    ####################
    🧐账号：{}
    💻签到结果：{}
    剩余天数：{}
    ####################
    祝您过上美好的一天！'''.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), email, sign_msg,
                                  timeday)
        print(message)
        msgs = msgs + '\n' + message
        return message


class push:
    # Qmsg私聊推送
    def Qmsg_send(msg):
        if QKey == '':
            return
        qmsg_url = 'https://qmsg.zendee.cn/send/' + str(QKey)
        data = {
            'msg': msg,
        }
        requests.post(qmsg_url, data=data)

    # Server酱推送
    def server_send(self, msg):
        if SKey == '':
            return
        server_url = "https://sctapi.ftqq.com/" + str(SKey) + ".send"
        data = {
            'text': self.name + "glados签到通知",
            'desp': msg
        }
        requests.post(server_url, data=data)

    # 酷推QQ推送
    def kt_send(msg):
        if ktkey == '':
            return
        kt_url = 'https://push.xuthus.cc/send/' + str(ktkey)
        data = ('glados签到完成，点击查看详细信息~\n' + str(msg)).encode("utf-8")
        requests.post(kt_url, data=data)

    # Telegram私聊推送
    def tele_send(self, msg: str, tele_api_url, tele_bot_token, tele_user_id):
        if tele_bot_token == '':
            return
        tele_url = f"{tele_api_url}/bot{tele_bot_token}/sendMessage"
        data = {
            'chat_id': tele_user_id,
            'parse_mode': "Markdown",
            'text': msg
        }
        requests.post(tele_url, data=data)

    # xiZhi推送
    def xiZhi_send(msg):
        if xizhi_token == '':
            return
        title = 'Glados每日通知'
        content = msg
        url = f'https://xizhi.qqoq.net/{xizhi_token}.send'
        data = {
            "title": title,
            "content": content
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        res = requests.post(url, data=body, headers=headers)
        if res.status_code == 200:
            print("息知推送成功")

    # Pushplus推送
    def pushplus_send(msg):
        if push_token == '':
            return
        token = push_token
        title = 'glados签到通知'
        content = msg
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": token,
            "title": title,
            "content": content
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        re = requests.post(url, data=body, headers=headers)
        print(re.status_code)


if __name__ == '__main__':  # 直接运行和青龙入口
    i = 0
    n = 0
    #print("已设置不显示账号密码等信息")
    while i < len(groups):
        n = n + 1
        group = groups[i]
        ck = group
        msgs = msgs + "第" + str(n) + "用户的签到结果"
        print("第" + str(n) + "个用户开始签到")
        session = requests.session()
        # --------------------以下非特殊情况不要动---------------------
        session.headers = {
            'Accept': "application/json, text/plain, */*",
            #'Authorization': "",可选
            'Sec-Fetch-Site': "same-origin",
            'sec-ch-ua': "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Microsoft Edge\";v=\"114\"",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
            'sec-ch-ua-mobile': "?0",
            'Content-Type': "application/json;charset=UTF-8",
            'Sec-Fetch-Dest': "empty",
            'Host': "glados.rocks",
            'Origin': "https://glados.rocks",
            'Sec-Fetch-Mode': "cors",
            'sec-ch-ua-platform': "\"Windows\"",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            'Connection': "keep-alive"
        }
        # --------------------以上非特殊情况不要动---------------------
        run = gladosanelQd(ck)
        run.main()
        time.sleep(5)
        i += 1
    else:
        # gladosanelQd.server_send( msgs )
        push.kt_send(msgs)
        # gladosanelQd.Qmsg_send(gladosanelQd.name+"\n"+gladosanelQd.email+"\n"+ msgs)
        # gladosanelQd.tele_send(gladosanelQd.name+"\n"+gladosanelQd.email+"\n"+ msgs)
        push.pushplus_send(msgs)
        push.xiZhi_send(msgs)
