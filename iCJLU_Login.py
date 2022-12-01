import requests
import time
import re
from datetime import datetime
from urllib import parse
from configparser import ConfigParser
from ping3 import ping, verbose_ping
from os.path import dirname, abspath, join
from win10toast import ToastNotifier
from encryption.srun_md5 import *
from encryption.srun_sha1 import *
from encryption.srun_base64 import *
from encryption.srun_xencode import *

header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666 Edg/107.0.0.0'
}
init_url = "http://10.253.0.100/"
get_challenge_api = "http://10.253.0.100//cgi-bin/get_challenge"
srun_portal_api = "http://10.253.0.100//cgi-bin/srun_portal"
n = '200'
type = '1'
enc = "srun_bx1"
py_loc = dirname(abspath(__file__))
ico_loc = py_loc + r'\ico'
success_icon = join(ico_loc, "Check.ico")
false_icon = join(ico_loc, "Cross.ico")
unknown_icon = join(ico_loc, "Unknown.ico")
logout_icon = join(ico_loc, "Warn.ico")
day_time = datetime.now().strftime('%Y-%m-%d %H:%M')

def get_chksum():
    chkstr = token + username
    chkstr += token + hmd5
    chkstr += token + ac_id
    chkstr += token + ip
    chkstr += token + n
    chkstr += token + type
    chkstr += token + i
    return chkstr


def get_info():
    info_temp = {
        "username": username,
        "password": password,
        "ip": ip,
        "acid": ac_id,
        "enc_ver": enc
    }
    i = re.sub("'", '"', str(info_temp))
    i = re.sub(" ", '', i)
    return i


def init_getip():
    global ip
    init_res = requests.get(init_url, headers=header)
    print("初始化获取ip...")
    ip = re.search('id="user_ip" value="(.*?)"', init_res.text).group(1)
    print("获取成功,ip:" + ip)


def get_token():
    print("正在获取token...")
    global token
    get_challenge_params = {
        "callback": "jQuery112406728703022454459_" + str(int(time.time() * 1000)),
        "username": username,
        "ip": ip,
        "_": int(time.time() * 1000),
    }
    get_challenge_res = requests.get(get_challenge_api, params=get_challenge_params, headers=header)
    token = re.search('"challenge":"(.*?)"', get_challenge_res.text).group(1)


# print(get_challenge_res.text)
# print("token为:"+token)


def do_complex_work():
    global i, hmd5, chksum
    i = get_info()
    i = "{SRBX1}" + get_base64(get_xencode(i, token))
    hmd5 = get_md5(password, token)
    chksum = get_sha1(get_chksum())
    print("所有加密工作已完成!")


def login():
    srun_portal_params = {
        'callback': 'jQuery112406728703022454459_' + str(int(time.time() * 1000)),
        'action': 'login',
        'username': username,
        'password': '{MD5}' + hmd5,
        'ac_id': ac_id,
        'ip': ip,
        'chksum': chksum,
        'info': i,
        'n': n,
        'type': type,
        'os': 'Windows 10',
        'name': 'Windows',
        'double_stack': '0',
        '_': int(time.time() * 1000)
    }
    # print(srun_portal_params)
    print('正在发送数据...')
    srun_portal_res = requests.get(srun_portal_api, params=srun_portal_params, headers=header)
    res = srun_portal_res.text
    # print(res)
    if '"ecode":0' in res:
        print('登陆成功!')
        ToastNotifier().show_toast(title="该设备已登录", msg=f"iCJLU_Login\n{day_time}", icon_path=success_icon, duration=5,
                                   threaded=False)
    elif '"ecode":"E2531"' in res:
        print('用户不存在!')
        ToastNotifier().show_toast(title="用户不存在!", msg=f"iCJLU_Login\n{day_time}", icon_path=false_icon, duration=5,
                                   threaded=False)

    elif '"ecode":"E2901"' in res:
        print('账号或密码错误!')
        ToastNotifier().show_toast(title="账号或密码错误!", msg=f"iCJLU_Login\n{day_time}", icon_path=false_icon, duration=5,
                                   threaded=False)
    else:
        print('未知错误!')
        ToastNotifier().show_toast(title="未知错误!", msg=f"iCJLU_Login\n{day_time}", icon_path=unknown_icon, duration=5,
                                   threaded=False)


def logout():
    srun_portal_params = {
        'callback': 'jQuery112406728703022454459_' + str(int(time.time() * 1000)),
        'action': 'logout',
        'username': username,
        'ac_id': ac_id,
        'ip': ip,
        '_': int(time.time() * 1000)
    }
    requests.get(srun_portal_api, params=srun_portal_params, headers=header)
    print('注销成功!')
    ToastNotifier().show_toast(title="未知错误!", msg=f"iCJLU_Login\n{day_time}", icon_path=logout_icon, duration=5,
                               threaded=False)


def test_net():
    print('测试网络连接...')
    # print('ping @ {}'.format(datetime.now()))
    host = 'www.baidu.com'
    src_addr = None
    result = ping(host, src_addr=src_addr)
    if result is None:
        print('连接失败！')
    else:
        print('已连接！')


def params_get(url):
    res = requests.get(url, headers=header)
    url = parse.urlparse(res.url)
    params = dict([(k, v[0]) for k, v in parse.parse_qs(url.query).items()])
    return params


if __name__ == '__main__':
    global username, password, ac_id
    ac_id = f'{params_get(init_url).get("ac_id")}'
    conf = ConfigParser()
    conf.read("config.ini")
    time.sleep(0.5)
    username = conf['user']['username']
    print(username)
    password = conf['user']['password']
    init_getip()
    get_token()
    do_complex_work()
    login()
    # logout()
    test_net()
