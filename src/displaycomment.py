import _tkinter
import datetime
import math


class DisplayComment:
    def __init__(self, comment_data, list_box):
        self.comment_data = comment_data
        self.list_box = list_box
        self.i = 0

    def display_comment(self):
        while self.i < len(self.comment_data):
            if self.comment_data[self.i]['chat'] is not None:
                vpos_convert_datetime = datetime.timedelta(milliseconds=int(self.comment_data[self.i]['vpos']) * 10)
                # vposをdatetime型に変換
                convert_minutes = math.floor(vpos_convert_datetime.seconds / 60)
                try:
                    self.list_box.insert('end', '{:0=2.0f}:{:0=2.0f}'
                                         .format(convert_minutes, vpos_convert_datetime.seconds - convert_minutes * 60)
                                         + ' ' + self.comment_data[self.i]['chat'])
                except _tkinter.TclError:
                    pass

            self.i += 1
