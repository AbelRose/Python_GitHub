import requests
from lxml import etree
import re

class GithubLogin(object):
    def __init__(self):
        # 登录页get请求URL
        self.base_url = 'https://github.com/login'
        # 登录post提交URL
        self.login_url = 'https://github.com/session'
        # github个人主页
        self.profile_url = 'https://github.com/settings/profile'
        # 登录页headers
        self.headers = {
            'Referer': 'https://github.com/',
            'Host': 'github.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        }

        self.session = requests.Session()

    # # =============获取登录页的 authenticity_token 值=============
    # def token(self):
    #     res = self.session.get(url=self.base_url, headers=self.headers)
    #     if res.status_code == requests.codes.ok:
    #         res_obj = etree.HTML(res.text)
    #         print(res_obj)
    #         token_value = res_obj.xpath('//div[@id="login"]/form/input[@name="authenticity_token"]/@value')[0]
    #         return token_value

    # 获取 authenticity_token
    def get_authenticity_token(self):
        login_url = "https://github.com/login"
        r = self.session.get(login_url, headers=self.headers)
        # print(r.text)
        authenticity_token = re.findall('<input type="hidden" name="authenticity_token" value="(.+?)" />', r.text)
        print("authenticity_token：{}".format(authenticity_token))
        return authenticity_token[0]


    def login(self, email, passwd):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'login': email,
            'password': passwd,
            'authenticity_token': self.get_authenticity_token()
        }

        # 登录 post 提交表单
        res_index = self.session.post(url=self.login_url, headers=self.headers, data=post_data)
        print(res_index)
        if res_index.status_code == requests.codes.ok:
            self.repository(res_index.text)

        # 请求个人中心页面
        res_profile = self.session.get(url=self.profile_url, headers=self.headers)
        if res_profile.status_code == requests.codes.ok:
            # self.getProfile(res_profile.text)
            self.repository(res_profile.text)

    def repository(self, text):
        res_obj = etree.HTML(text)
        print(res_obj)
        # repo_list = res_obj.xpath('//div[@class="Box-body"]/ul/li//a/@href')
        repo_list = res_obj.xpath('//div[@class="js-collaborated-repos"]')  # TODO 从js-collaborated-repos中获取库的信息
        print(repo_list)
        for repo in repo_list:
            print(repo)

    # def getProfile(self, text):
    #     res_obj = etree.HTML(text)
    #     username = res_obj.xpath(
    #         '//div[@class="column two-thirds"]/dl[contains(@class,"form-group")]/dd/input[@id="user_profile_name"]/@value')[0]
    #     print("用户名：", username)
    #     email = res_obj.xpath('//div[@class="column two-thirds"]/dl[2]/dd/select/option[2]/text()')[0]
    #     print("邮箱：", email)


if __name__ == '__main__':
    alice_login = GithubLogin()
    alice_login.login('15941999082@163.com', 'Sherlockholmes0528')
