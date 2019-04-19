import configparser
import time

from src.displaycomment import DisplayComment
from src.login import Login
from src.makecomment import MakeComment


class Command:

    def __init__(self, list_box, master):
        self.session = None
        self.list_box = list_box
        self.master = master

    def login(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        MAIL_ADDRESS = config.get('GENERAL', 'MailAddress')
        PASSWORD = config.get('GENERAL', 'PassWord')

        if not MAIL_ADDRESS or not PASSWORD:
            self.list_box.insert('end', 'config.iniが正しく設定されていません')

        login = Login(MAIL_ADDRESS, PASSWORD, self.list_box)
        self.session = login.do_login()

    def get_comment(self, list_box, movie_id):
        global comment_list
        make_comment = MakeComment(self.session, list_box)
        comment_list = make_comment.main(movie_id.get())
        play_comment = DisplayComment(comment_list, list_box)
        play_comment.display_comment()

    def preparation_do_comment(self, list_box):
        play_time = time.perf_counter()
        i = 0
        j = 0
        self.do_comment(play_time, i, j, list_box)

    def do_comment(self, play_time, i, j, list_box):
        global comment_list
        elapsed_time = time.perf_counter()  # 経過した時間
        now_time = int((elapsed_time - play_time) * 100)  # 再生時間を計測してvposと比較可能なミリ秒に変換
        while now_time > int(comment_list[i]['vpos']):
            # 未加工のcomment_listで比較しているので、display_comment段階でNoneが消された表示されたコメントと長さに差がある
            # 比較がないとlist_boxにNoneがないため早く進んでしまう
            # それを埋めるために同じようにis not Noneで比較して、jという独自変数(list_box上のコメントの位置)でlist_boxを進める
            if comment_list[i]['chat'] is not None:
                list_box.see(j)
                j += 1
            else:
                pass
            i += 1

        # ()で実行するとよくわからん挙動するのでlambda式で()をない状態に
        self.master.after(100, lambda: self.do_comment(play_time, i, j, list_box))

    def delete_comment(self):
        self.list_box.delete(0, 'end')
