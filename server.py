# -*- coding: UTF-8 -*-
'''
给博客文章添加标题
'''
from utils.gitbook import *
from utils.hexo import *

blog_name = ''
article_folder = ''
server_type = ''

print len(sys.argv) 
if len(sys.argv) == 4:
    blog_name = sys.argv[1]
    article_folder = sys.argv[2]
    server_type = sys.argv[3]
else:
    blog_name = raw_input('请输入博客名字:')
    article_folder = raw_input('请输入文章目录:')
    server_type = raw_input('请输入服务类型序号: \n1:hexo; \n2:gitbook; \n')

if os.path.isdir(article_folder):
    if server_type == '1':
        hexo.start_server(blog_name, article_folder)
    elif server_type == '2':
        gitbook.start_server(blog_name, article_folder)
    else:
        print 'blogServer error: 请输入正确的服务类型'
else:
    print 'blogServer error: 文章目录不存在，'+article_folder



