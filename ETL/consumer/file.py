# encoding: utf-8
"""
文件消费者
@author Yuriseus
@create 2016-8-23 13:50
"""
import os

from consumer.base import BaseConsumer, State
from util.file import FileUtil


class FileConsumer(BaseConsumer):
    def __init__(self, dir_path):
        super().__init__()
        self._dir_path = dir_path
        self._files = []

    def check_process(self):
        """
        主循环每秒检测
        :return:
        """
        if self.state == State.STARTED:
            if not self._files:    # 队列已处理完成，重新读取目录新文件
                self._files = FileUtil.get_files(self._dir_path, ['.COMPLETE'])
            self.process_files()

    def consume(self, line_data):
        print(line_data)

    def process_files(self):
        if self._files:
            for file_path in self._files:
                if self.state == State.STARTED:    # 若处理过程中暂停会停止，正在处理的文件不受影响，继续处理完成
                    with open(file_path) as f:
                        for line in f:
                            self.consume(line)
                    # 处理完成。重命名文件，从列表中移除
                    complete_file_path = file_path + '.COMPLETE'
                    os.rename(file_path, complete_file_path)
                    self._files.remove(file_path)

    def handle_start(self):
        pass

    def handle_pause(self):
        pass

    def handle_stop(self):
        pass


if __name__ == '__main__':
    dir_path = 'G:\\GitHub\\study\\test'
    consumer = FileConsumer(dir_path)
    consumer.start()
