import requests


class Login:
    def __init__(self, mail_address, password, list_box):
        self.MAIL_ADDRESS = mail_address
        self.PASSWORD = password
        self.session = requests.Session()  # セッションの開始
        self.list_box = list_box

    def do_login(self):
        login_url = 'https://secure.nicovideo.jp/secure/login?site=niconico'
        login_date = {
            'mail': self.MAIL_ADDRESS,
            'password': self.PASSWORD
        }

        request_result = self.session.post(login_url, login_date)

        if request_result.status_code == requests.codes.ok and request_result.url == 'https://www.nicovideo.jp/':
            self.list_box.insert('end', 'ログイン成功')
        else:
            self.list_box.insert('end', 'ログイン失敗')

        return self.session
