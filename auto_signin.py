# auto_signin.py
'''自动签到：
【你】——> 伪装浏览器（设置URL + headers）——> 带着身份证（Cookie）访问微博签到接口 ——> 微博验证 ——> 返回签到成功/失败
'''
import requests
import pickle
import time
import random
from datetime import datetime
import sys

# Cookie（身份）证明你是谁（登录状态），如果没有 Cookie，微博就不认你
def load_cookies(cookie_path="weibo_cookies.pkl"):
    with open(cookie_path, "rb") as f:
        cookies = pickle.load(f)
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    return session

def weibo_signin():
    session = load_cookies()

    # 设置请求的URL和参数
    # 告诉微博：“我要在哪个页面干什么事情”
    url = "https://weibo.com/p/aj/general/button"
    topic_id = "100808c98f988ea22d7b40caed47951f8eb507"  # 目标超话 ID
    # 请求的参数
    # 告诉微博：“这是超话 ID，我的状态是未签到，我想签到”
    params = {
        "ajwvr": "6",
        "api": "http://i.huati.weibo.com/aj/super/checkin",
        "texta": "签到",  # 按钮文字
        "textb": "已签到",  # 成功后显示文字
        "status": "0",  # 表示“我还没签”
        "id": topic_id,  # 替换为你目标超话 ID
        "location": "page_100808_super_index",
        "timezone": "GMT+0800",
        "lang": "zh-cn",
        "plat": "Win32",
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
        "screen": "1920*1080",
        "__rnd": str(int(time.time() * 1000))  # 防止缓存，微博接口需要
    }

    headers = {
        "User-Agent": params["ua"],  # 你模拟的是哪个浏览器
        "Referer": f"https://weibo.com/p/{topic_id}/super_index",  # 你是从哪个页面跳过来的
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Sec-CH-UA": '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-CH-UA-Mobile": "?0"
    }

    try:
        response = session.get(url, headers=headers, params=params)
        res_json = response.json()
        print(f"[{datetime.now()}] 签到请求结果：{res_json}")
        if "code" in res_json and res_json["code"] == "100000":
            print(f"[{datetime.now()}] 签到成功！")
        elif "msg" in res_json:
            print(f"[{datetime.now()}] 签到失败：{res_json['msg']}")
        else:
            print(f"[{datetime.now()}] 签到结果未知：{res_json}")
    except Exception as e:
        print(f"签到异常：{e}")

if __name__ == "__main__":
    print("开始签到任务...")
    try:
        sys.stdout = open("signin_log.txt", "a", encoding="utf-8")
        sys.stderr = sys.stdout
        print("=" * 20)
        print(f"【{datetime.now()}】启动签到任务")
        weibo_signin()

    except Exception as e:
        print(f"程序异常：{e}")
