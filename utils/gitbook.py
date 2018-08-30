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

class gitbook:
    @staticmethod
    def start_server(blog_name,article_folder):

        if os.path.isdir(article_folder):
            server = gitbook()
            server.creat_gitbook(article_folder, blog_name)
        else:
            print 'gitbook error: 文章目录不存在，' + article_folder

    def openWeb(self):
        time.sleep(3)
        url = 'http://127.0.0.1:4000'
        webbrowser.open(url)
        print webbrowser.get()

    def add_readme_file(self,dir):
        print 'add_readme_file start, '+dir
        has_readme = False
        for file in os.listdir(dir):
            if 'README.md' in file:
                has_readme = True

        if has_readme:
            print 'README.md existing '

        if not has_readme:
            readme_file = open(dir+'/'+'README.md', "w")
            content = '## 文章列表：\n\n'
            for file in os.listdir(dir):
                if 'README.md' in file:
                    continue
                content = content+file.replace('.md','\n')+'\n'
            readme_file.write(content)
            readme_file.close()

    def modify_summary(self,root_dir):
        print 'modify_summary >>> start\n'

        root_list = []
        for file in os.listdir(os.getcwd()):
            if not os.path.isdir(file):
                print 'error not\'s dir : ' + file
                continue
            if file == root_dir:
                # 根Readme 首页描述
                if os.path.isfile(file+'/'+'README.md'):
                    print 'error root README existing !!!' 
                    shutil.copyfile(file+'/README.md','README.md')
                    continue

            self.add_readme_file(file)

            chapter_list = []
            for file_md in os.listdir(os.getcwd()+'/'+file):
                if not '.md' in file_md:
                    # 不是.md文件，跳过
                    print 'error not\'s .md : ' + file_md
                    continue
                if 'README.md' == file_md:
                    # 每个模块的描述
                    file_name = '* [' + file + ']' + '(' + file+'/' + file_md + ')'
                    chapter_list.append(file_name)
                else:
                    file_name = ' * ['+file_md.replace('.md','')+']'+'('+file+'/'+file_md+')'
                    chapter_list.append(file_name)

            root_list.append(chapter_list)

        summary_file = 'SUMMARY.md'
        temp_summary_file = summary_file+'_tmp'
        temp_fo = open(temp_summary_file, "w")

        content = '# Summary\n\n'
        for chapter_list in root_list:
            for line in chapter_list:
                if 'README.md' in line:
                    content = content+line+'\n'
            for line in chapter_list:
                if 'README.md' in line:
                    continue
                content = content + line + '\n'

        print 'content = '+content
        temp_fo.write(content)
        temp_fo.close()
        os.remove(summary_file)
        os.rename(temp_summary_file, summary_file)

    def creat_gitbook(self,article_folder,blog_name):

        # os.system('npm install gitbook-cli -g')

        dis_dir = blog_name
        if os.path.isdir(dis_dir):
            shutil.rmtree(dis_dir)

        self.creat_blog_note_folder(blog_name)

        for file in os.listdir(article_folder):
            file_path = article_folder+'/'+file
            if os.path.isdir(file_path):
                if os.listdir(file_path) == 0 or '.' in file:
                    print 'dir error : ' + file_path
                    continue
                shutil.copytree(file_path,dis_dir+'/'+file)
            else:
                if not '.md' in file:
                    print 'file error : ' + file_path
                    continue
                new_file_path = dis_dir+'/'+article_folder
                if not os.path.isfile(new_file_path):
                    self.creat_blog_note_folder(new_file_path)
                shutil.copyfile(file_path,new_file_path+'/'+file)

        os.chdir(blog_name)
        os.system('gitbook init')

        self.modify_summary(article_folder)

        p = Process(target=self.openWeb)
        p.start()

        os.system('gitbook serve')

    def creat_blog_note_folder(self,folder):

        result = os.path.exists(folder)
        if not result:
            os.makedirs(folder)
            print 'creat new folder : ' + folder
        else:
            print 'folder existing : ' + folder





