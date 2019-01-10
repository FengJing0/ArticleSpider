import requests
import http.cookiejar as cookielib
import re

agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
header = {
    'HOST': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com',
    'User-Agent': agent
}


def get_xsrf():
    response = requests.get('https://www.zhihu.com',headers=header)
    print(response.text)
    return ''


get_xsrf()


def zhihu_log(account, password):
    if re.match("^1\d{10}", account):
        print('手机登录')
        post_url = 'https://www.zhihu.com/login/phone_num'
        post_data = {
            '_xsrf': '',
            'phone_num': account,
            'password': password
        }
