# -*- coding: UTF-8 -*-
'''
给博客文章添加标题
'''

import os
import sys
import webbrowser
import thread
import time
from multiprocessing import Process
import shutil


def check_title(file_path):
    file = open(file_path, "r")
    lines = file.readlines(1)
    for line in lines:
        if '---' in line:
            return True
    return False


def add_title(title,file_path):
    # print file_path
    # print title
    result = check_title(file_path)
    if result:
        # print 'title已存在，不需要添加'
        return

    file = open(file_path, "r")
    content = file.read()
    file.close()

    content = "---\n" +'title: '+title + '\n' + '---\n\n' + content
    file = open(file_path, "w")
    file.write(content)
    file.close()
    # print "title添加完成"

def replace_article_title(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if '.md' in file:
                add_title(file,root+'/'+file)


def openWeb():
    time.sleep(3)
    url = 'http://127.0.0.1:4000/archives'
    webbrowser.open(url)
    print webbrowser.get()


def add_themes_next():
    print 'start add_themes_next >>>>'
    print os.getcwd()

    if not os.path.isdir('themes/next'):
        os.makedirs('themes/next')
        os.system('curl -s https://api.github.com/repos/iissnan/hexo-theme-next/releases/latest | grep tarball_url | cut -d \'\"\' -f 4 | wget -i - -O- | tar -zx -C themes/next --strip-components=1')

    file_name = '_config.yml'
    temp_file_name = 't_config.yml'
    fo = open(file_name, "r+")
    new_fo = open(temp_file_name, "w")

    lines = fo.readlines()
    for line in lines:
        if 'theme:' in line:
            line = 'theme: next \n'
        new_fo.write(line)

    fo.close()
    new_fo.close()

    os.remove(file_name)
    os.rename(temp_file_name, file_name)

def creat_hexo(article_folder,blog_name):

    creat_blog_note_folder(blog_name)
    os.system('hexo init '+ blog_name)

    dis_dir = blog_name+'/source/_posts/'+article_folder
    if os.path.isdir(dis_dir):
        shutil.rmtree(dis_dir)

    shutil.copytree(article_folder,dis_dir)

    os.chdir(blog_name)

    hello_world_file = 'source/_posts/hello-world.md'
    if os.path.isfile(hello_world_file):
        os.remove(hello_world_file)

    replace_article_title('source/_posts')

    add_themes_next()

    p = Process(target=openWeb)
    p.start()

    os.system('hexo s')


def creat_blog_note_folder(folder):

    result = os.path.exists(folder)
    if not result:
        print '>>> ' + folder
        os.makedirs(folder)
        print 'creat new folder : ' + folder
    else:
        print 'folder existing : ' + folder

if __name__ == '__main__':

    # blog_name = 'BlogNote'
    # article_folder = 'iOSAdvanced'

    blog_name = ''
    article_folder = ''

    if len(sys.argv) == 3:
        blog_name = sys.argv[1]
        article_folder = sys.argv[2]
        creat_hexo(article_folder, blog_name);
    else:
        print '请输入参数：博客目录，文章目录'

