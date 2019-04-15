import tkinter

from command import Command


class Application(tkinter.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('NicoNico Comment Viewer')
        self.master.geometry("400x650")
        self.pack()
        self.create_widget()

    def create_widget(self):
        upper_based_frame = tkinter.Frame(self)
        upper_based_frame.pack()

        row_01_frame = tkinter.Frame(upper_based_frame)
        row_01_frame.pack()
        label_movie_id = tkinter.Label(row_01_frame, text='動画ID')
        label_movie_id.pack(fill='x', side='left', padx=10, pady=10)
        movie_id = tkinter.StringVar()
        movie_id_entry = tkinter.Entry(row_01_frame, textvariable=movie_id, width=50)
        movie_id_entry.pack(fill='x', side='left')

        row_02_frame = tkinter.Frame(upper_based_frame)
        row_02_frame.pack(fill='x')
        login_button = tkinter.Button(row_02_frame, text='ログイン', width='12')
        login_button.pack(fill='x', side='left')
        get_comment_button = tkinter.Button(row_02_frame, text='コメント取得', width='11')
        get_comment_button.pack(fill='x', side='left')
        play_comment_button = tkinter.Button(row_02_frame, text='コメント再生', width='12')
        play_comment_button.pack(fill='x', side='left')
        delete_comment_button = tkinter.Button(row_02_frame, text='コメント消去', width='12')
        delete_comment_button.pack(fill='x', side='left')

        under_based_frame = tkinter.Frame(self)
        under_based_frame.pack()

        label_log = tkinter.Label(under_based_frame, text='ログとか')
        label_log.pack()
        list_box = tkinter.Listbox(under_based_frame, height=34, width=60)
        list_box.pack(fill='both', padx=10, side='left')
        scrollbar = tkinter.Scrollbar(under_based_frame, command=list_box.yview)
        scrollbar.pack(side='left', fill='y')
        list_box.configure(yscrollcommand=scrollbar.set)

        command = Command(list_box, self.master)

        # 引数いる関数を直でやるとなぜかボタンを押す前に実行されちゃうのでlambdaを用いる
        login_button['command'] = command.login()
        get_comment_button['command'] = lambda: command.get_comment(list_box, movie_id)
        play_comment_button['command'] = lambda: command.preparation_do_comment(list_box)
        delete_comment_button['command'] = command.delete_comment
