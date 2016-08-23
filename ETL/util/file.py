# encoding: utf-8
"""
文件工具类
@author Yuriseus
@create 2016-8-23 14:16
"""
import os


class FileUtil(object):
    @staticmethod
    def get_files(dir_path, exclude_ext=None):
        """
        获取目录下所有文件
        :param dir_path:
        :param exclude_ext: 排除的文件扩展名数组
        :return:
        """
        files = []
        for base, dir_names, file_names in os.walk(dir_path):
            for file_name in file_names:
                shotname, extension = os.path.splitext(file_name)
                if exclude_ext and extension in exclude_ext:
                    continue
                files.append(os.path.join(base, file_name))
        return files


if __name__ == '__main__':
    dir_path = 'G:\\GitHub\\study'
    print(FileUtil.get_files(dir_path))

    # for base, dirs, fs in os.walk(dir_path):
    #   for f in fs:
    #     print(os.path.join(base, f))

