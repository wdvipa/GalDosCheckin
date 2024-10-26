# GalDosCheckin
GalDos每日签到脚本，支持青龙和action，支持多账号批量签到
## 各位既然用了那就随手点个Satr行不行
## 使用方式
`ql repo https://ghproxy.com/https://github.com/wdvipa/GlaDosCheckin/raw/main/glados.py`
如需直接运行或不用环境变量吧文件开头的cs变量改为2即可
### 青龙订阅
青龙最新版本订阅请填写下面内容（没写的别乱填）
|数据|内容|
|----|----|
|名称|GalDos签到|
|链接|`https://kkgithub.com/wdvipa/GlaDosCheckin.git`|
|定时类型|crontab|
|定时规则|	2 2 28 * *|
|白名单|glados.py|
## 更新内容
支持青龙执行，因pushplus需要实名，所以增加息知推送
## 青龙变量
| 参数 | 说明                     |  格式  |
| ---- | -----------------------  |  -------  |
| glados  | 机场的名字，网址，账号密码 |  `机场名字\|机场的网址(https:www.xxxx...)\|第一个账号,密码;第二个账号,密码;... 多机场用回车隔开 例:名字\|https://yyy.com\|jjjj@qq.com,password;jjjj@gmail,password`  |
| glados_fs  | 推送的平台 |  多个平台使用&隔开 支持push,kt,stb,qm,tel  |
| glados_push  | Pushplus的推送token |  token  |
| glados_xizhi  | 息知的推送token 公众号发送密钥后回复的中间XZ开头不包含.send的字符串|  token  |
| glados_ktkey  | 酷推的key |  key  |
| 暂不支持  | 暂不支持 |  暂不支持  |
## 使用教程
### 青龙
视频：https://www.bilibili.com/video/BV1bv411F7HL/
[![](https://bb-embed.zjffun.com/embed?v=BV1jS4y1w7SW)](https://www.bilibili.com/video/BV1bv411F7HL/)

参考仓库:https://github.com/GeorgeLxw/sspauto

