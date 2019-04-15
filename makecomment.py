import xml.etree.ElementTree as ET
from datetime import datetime


class MakeComment:
    def __init__(self, session, list_box):
        self.session = session
        self.list_box = list_box

    def main(self, movie_id):
        flapi_information = self.post_flapi(movie_id)
        thumb_info = self.post_thumbinfo(movie_id)

        movie_information = self.get_movie_information(flapi_information)
        movie_length = self.get_movie_length(thumb_info)

        xml = self.make_xml(movie_information, movie_length)

        comment_data = self.post_xml(xml)
        comment_list = self.sort_xml(comment_data)

        return comment_list

    def post_flapi(self, movie_id):
        flapi_information = self.session.get('http://flapi.nicovideo.jp/api/getflv/' + movie_id)

        return flapi_information

    def post_thumbinfo(self, movie_id):
        thumb_info = self.session.get('http://ext.nicovideo.jp/api/getthumbinfo/' + movie_id)

        return thumb_info

    def get_movie_information(self, flapi_information):
        split_movie_information = flapi_information.text.split('&')  # list型
        # print(split_movie_information)

        thread_id = split_movie_information[0].split('=')
        user_id = split_movie_information[5].split('=')

        if split_movie_information[10] == 'needs_key=1':  # 公式動画か判定
            official_movie = self.session.get('http://flapi.nicovideo.jp/api/getthreadkey?thread=' + thread_id[1])
            # print(official_movie)
            split_official_movie_information = official_movie.text.split('&')
            # print(official_movie_information)
            thread_key = split_official_movie_information[0].split('=')
            force = split_official_movie_information[1].split('=')

            return thread_id, user_id, thread_key, force

        else:
            return thread_id, user_id

    @staticmethod
    def get_movie_length(thumb_info):
        root = ET.fromstring(thumb_info.text)
        movie_length = datetime.strptime(root[0][5].text, '%M:%S')  # ThumbInfoAPIを叩いて取得したXMLから動画時間を抽出。
        if movie_length.second > 0:
            movie_length = movie_length.minute + 1  # 分以下は切り上げらしいのでその処理

        return movie_length

    @staticmethod
    def make_xml(movie_information, movie_length):
        if len(movie_information) > 2:
            post_xml = '<packet>' \
                       '<thread thread="{0}" version="20130701"  />' \
                       '<thread_leaves thread="{0}" user_id="{1}" threadkey="{2}" force_184="{3}">' \
                       '0-{4}:100,1000</thread_leaves>' \
                       '</packet>' \
                .format(movie_information[0][1], movie_information[1][1], movie_information[2][1],
                        movie_information[3][1], 25)
            return post_xml

        else:
            post_xml = '<packet>' \
                       '<thread thread="{0}" version="20130701"/>' \
                       '<thread_leaves thread="{0}">0-{1}:100,1000</thread_leaves>' \
                       '</packet>' \
                .format(movie_information[0][1], movie_length)
            return post_xml

    def post_xml(self, xml):
        comment_data = self.session.post('http://nmsg.nicovideo.jp/api/', xml)
        return comment_data

    def sort_xml(self, comment_data):
        root = ET.fromstring(comment_data.text)

        comment_list = []
        for comment_xml in root.findall('chat'):
            # リスト型の中に辞書型を入れてる
            comment_list.append(
                {"no": comment_xml.get('no'), "vpos": comment_xml.get('vpos'), "chat": comment_xml.text})

        # vpos順で並び替え  https://note.nkmk.me/python-dict-list-sort/
        #                 https://akiyoko.hatenablog.jp/entry/2014/09/26/235300
        comment_list.sort(key=lambda x: int(x['vpos']))
        # print(comment_list)

        # print("XMLソート完了")
        self.list_box.insert('end', 'コメント取得完了')

        return comment_list
