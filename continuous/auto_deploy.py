# encoding: utf-8
"""
自动部署。先内网代码复制提交到外网svn下，再修改配置，最后执行ssh执行远程命令
@author Yuriseus
@create 2016-6-20 13:56
"""

import logging
import os
import time
import subprocess
import filecmp
import shutil
import os
import re
import sys
from fabric.api import local, run, env, cd, execute, roles, open_shell


class AutoDeploy(object):
    def __init__(self):
        self.filecopy = FileCopy()
        self.shell = RemoteShell()
        self.src_dir = '/workspace/continuous/kshow_weixin_intranet/'
        self.dst_dir = '/workspace/continuous/kshow_weixin_internet_dev/'

    def deploy(self):
        self.init_config()
        print(self.update_code())
        self.copy_code()
        self.modify_file()
        print(self.commit_code())
        self.__restart_server()

    def init_config(self):
        raise Exception(u"此方法必须被实现初始化部署相关信息，来源源码目录self.src_dir，目标源码目录self.dst_dir")

    def update_code(self):
        cmds = [
            'cd %s' % self.src_dir,
            'svn update',
            'cd %s' % self.dst_dir,
            'svn update'
        ]
        return self.shell.run_in_local(cmds)

    def copy_code(self):
        self.filecopy.clear()
        self.filecopy.copy(self.src_dir, self.dst_dir)

    def modify_file(self):
        raise Exception(u"此方法必须被实现修改不同项目的特有文件")

    def commit_code(self):
        cmds = [
            'cd %s' % self.dst_dir,
            'svn update',
            'svn add * --force',
            'svn ci . -m "auto commit"'
        ]
        return self.shell.run_in_local(cmds)

    def __restart_server(self):
        self.shell.execute(self.restart_server)

    def restart_server(self):
        raise Exception(u"此方法必须被实现重启远程服务器")

    # def commit_code_to_internet(self):
    #     self.filecopy.clear()
    #     self.filecopy.copy(self.src_dir, self.dst_dir)
    #     js_path = os.path.join(self.dst_dir, 'web_frontend/static/js/kshow_1.0.js')
    #     setting_path = os.path.join(self.dst_dir, 'kshow_server/settings/setting.py')
    #     # 修改kshow.js的apiUrl
    #     self.replace_in_file(js_path, ['http://172.16.2.102/kshow/api/'], ['http://dev.corp.weixin.meda.cc/api/'])
    #     # 修改setting.py的CONF
    #     self.replace_in_file(setting_path, ['DEBUG = True', 'settings/config_intranet.conf'],
    #                          ['DEBUG = False', 'settings/config_kshow.conf'])
    #     # 提交svn
    #     self.shell.run_in_local(['cd %s' % self.dst_dir, 'svn update', 'svn add * --force', 'svn ci . -m "auto commit"'])

    def replace_in_file(self, filepath, olds, news):
        with open(filepath, mode='r') as rf:
            content = rf.read()
            new_content = content
            for old, new in zip(olds, news):
                new_content = new_content.replace(old, new)
        with open(filepath, mode='w') as wf:
            wf.write(new_content)


class FileCopy(object):
    """将文件夹下所有文件复制到另外一个文件夹下"""
    def __init__(self, src=None, dst=None):
        self.src = src
        self.dst = dst
        self.new_files = []
        self.del_files = []

    def compare(self, src, dst):
        ignore = ['.svn', '.pyc', 'test', 'test_frontend', 'logs', '.idea']
        dircmp = filecmp.dircmp(src, dst, ignore)
        src_only = dircmp.left_only
        dst_only = dircmp.right_only
        diff_files = dircmp.diff_files    # 源文件已发生改变
        for f in src_only:
            self.new_files.append(os.path.abspath(os.path.join(src, f)))
        for f in dst_only:
            self.del_files.append(os.path.abspath(os.path.join(dst, f)))
        for df in diff_files:
            self.new_files.append(os.path.abspath(os.path.join(src, df)))
        for cf in dircmp.common_dirs:
            self.compare(os.path.abspath(os.path.join(src, cf)), os.path.abspath(os.path.join(dst, cf)))
        return self.new_files, self.del_files

    def copy(self, src, dst):
        new_files, del_files = self.compare(src, dst)
        for _, nf in enumerate(new_files):
            nf = nf.replace('\\', '/')
            new_dst_file = re.sub(src, dst, nf)
            if os.path.isfile(nf):
                shutil.copy(nf, new_dst_file)
            else:
                shutil.copytree(nf, new_dst_file)

    def clear(self):
        self.new_files = []
        self.del_files = []


class RemoteShell(object):
    """远程登陆执行shelL"""
    def __init__(self):
        self.ssh_hosts = ['119.146.204.122:63220']
        env.roledefs = {
            'dev': ['root@119.146.204.122:63220']
        }
        env.password = '7=gNQqbkz3hv'

    @roles('dev')
    def run_after_cd_path(self, cd_path, cmds):
        output = ''
        with cd(cd_path):
            for _, cmd in enumerate(cmds):
                output += run(cmd) + '\n'
            return output

    def execute(self, task, hosts=None):
        # 解决不通过如：fab -f fab_update_ui_match_dev.py update_dev这样的调用时。#
        # 报错No hosts found. Please specify (single) host string for connection的问题
        if not hosts:
            hosts = self.ssh_hosts
        execute(task, hosts=hosts)

    @roles('dev')
    def run(self, cmd):
        return run(cmd)

    def run_in_local(self, cmds):
        cmd = ';'.join(cmds)
        handle = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = handle.communicate()[0]
        return output

