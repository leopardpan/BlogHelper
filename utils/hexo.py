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

class hexo:

    @staticmethod
    def start_server(blog_name,article_folder):

        if os.path.isdir(article_folder):
            server = hexo()
            server.creat_hexo(article_folder, blog_name)
        else:
            print 'error: 文章目录不存在，'+article_folder

    def check_title(self,file_path):
        file = open(file_path, "r")
        lines = file.readlines()
        index = 0
        for line in lines:
            if index > 2:
                return
            index=index+1
            if '---' in line:
                return True
        return False

    def add_title(self,title,categories,file_path):
        # print file_path
        # print title
        result = self.check_title(file_path)
        if result:
            print 'waring: title已存在，不需要添加. ' + file_path
            return

        file = open(file_path, "r")
        content = file.read()
        file.close()

        title = 'title: '+title + '\n'
        if categories:
            categories = 'categories: '+ '\"' + categories + '\"' + '\n'

        content = "---\n" + title + categories + '---\n\n' + content

        file = open(file_path, "w")
        file.write(content)
        file.close()
        # print "title添加完成"

    def replace_article_title(self,file_dir):
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if '.md' in file:
                    title = file.replace('.md','')
                    dirs = root.split('/')
                    categories = dirs[len(dirs)-1]
                    if categories == '_post':
                        categories = None

                    self.add_title(title,categories,root+'/'+file)


    def openWeb(self):
        time.sleep(3)
        url = 'http://127.0.0.1:4000/categories'
        webbrowser.open(url)
        print webbrowser.get()

    def insert_string_file_path(self,origin_string,string,file_path):
        file_name = file_path
        temp_file_name = file_path+'_tmp'
        fo = open(file_name, "r+")
        new_fo = open(temp_file_name, "w")

        lines = fo.readlines()
        for line in lines:
            if origin_string in line:
                line = line + string +'\n'
            new_fo.write(line)

        fo.close()
        new_fo.close()

        os.remove(file_name)
        os.rename(temp_file_name, file_name)

    def replace_string_file_path(self,old_string,new_string,file_path):
        file_name = file_path
        temp_file_name = file_path+'_tmp'
        fo = open(file_name, "r+")
        new_fo = open(temp_file_name, "w")

        lines = fo.readlines()
        for line in lines:
            if old_string in line:
                line = new_string+' \n'
            new_fo.write(line)

        fo.close()
        new_fo.close()

        os.remove(file_name)
        os.rename(temp_file_name, file_name)


    def add_themes_next(self):
        print 'start add_themes_next >>>>'
        print os.getcwd()

        if not os.path.isdir('themes/next'):
            os.makedirs('themes/next')
            os.system('curl -s https://api.github.com/repos/iissnan/hexo-theme-next/releases/latest | grep tarball_url | cut -d \'\"\' -f 4 | wget -i - -O- | tar -zx -C themes/next --strip-components=1')

        self.replace_string_file_path('theme:', 'theme: next', '_config.yml')
        self.replace_string_file_path('#categories:', '  categories: /categories/ || th', 'themes/next/_config.yml')

        if not os.path.isfile('source/categories/index.md'):
            os.system('hexo new page categories')

        self.insert_string_file_path('date:', 'type: "categories"', 'source/categories/index.md')

    def creat_hexo(self,article_folder,blog_name):

        if os.path.isdir(blog_name):
            shutil.rmtree(blog_name)

        self.creat_blog_note_folder(blog_name)
        os.system('hexo init '+ blog_name)

        dis_dir = blog_name+'/source/_posts/'+article_folder
        if os.path.isdir(dis_dir):
            shutil.rmtree(dis_dir)

        shutil.copytree(article_folder,dis_dir)

        os.chdir(blog_name)

        hello_world_file = 'source/_posts/hello-world.md'
        if os.path.isfile(hello_world_file):
            os.remove(hello_world_file)

        self.replace_article_title('source/_posts')

        self.add_themes_next()

        p = Process(target=self.openWeb)
        p.start()

        os.system('hexo s')

    def creat_blog_note_folder(self,folder):

        result = os.path.exists(folder)
        if not result:
            os.makedirs(folder)
            print 'creat new folder : ' + folder
        else:
            print 'folder existing : ' + folder
