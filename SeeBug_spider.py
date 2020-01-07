import re
import requests
import os

url_init = r'https://paper.seebug.org/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'} 

def get_indexlink(url):
    res = requests.get(url=url,headers=headers)
    title = re.findall(r'class="fa fa-angle-right"></i>(.*)</a></li>',res.text)
    title.remove('首页')
    title.remove('归档文件')
    title.remove('如何投稿')
    link = re.findall(r'<a href="/category(.*)/"><i',res.text)
    index={}
    for i in range (0,14):
        index[title[i]] = url+'category'+link[i]
    return(index)

def get_pages(index):
    page_index = {}
    link = list(index.values())
    for i in range (0,len(index)):
        res = requests.get(url=link[i],headers=headers)
        pages = re.findall(r'<span class="page-number">Page 1 of (.*)</span>',res.text)
        page_index[str(link[i])]=''.join(pages)
    return page_index

def get_articles_link(pages,index):                 #从一个分类（比如漏洞分析）中获取其所有页面上的文章链接
    path_basic = 'D:\\pytest\\'
    link_all = list(pages.keys())                   #将所有的链接放进一个列表
    pages_all = list(pages.values())                #将所有的页码放进一个列表
    for i in range (0,len(pages_all)):
        link = link_all[i]                                 #取出当前分类的链接
        pages = pages_all[i]                        #取出当前分类的总的页码
        index_name = ''.join(list(index.keys())[list(index.values()).index(link)])    #将文件夹的名字设为当前分类的链接
        path_article = path_basic + index_name                           #设置文件路径
        for j in range (0,int(pages)):
            url_page = link + '/?page='+str(j)           #在url后面跟上当前页码    
            res = requests.get(url=url_page,headers=headers)
            article_link = re.findall(r'class="post-title"><a href="(.*)/">',res.text)
            article_title = re.findall(r'/">(.*)</a></h5>',res.text)                    
            articles_alllink = {}
            for k in range (0,len(article_link)):
                articles_alllink[str(article_title[k])] = article_link[k]
            all_link=[]
            all_title=[]
            all_title = list(articles_alllink.keys())
            for l in range(0,len(all_title)):
                all_title[l] = all_title[l].replace('/','')
                all_title[l] = all_title[l].replace('\\','')
                all_title[l] = all_title[l].replace(':','')
                all_title[l] = all_title[l].replace('*','')
                all_title[l] = all_title[l].replace('"','')
                all_title[l] = all_title[l].replace('<','')
                all_title[l] = all_title[l].replace('>','')
                all_title[l] = all_title[l].replace('|','')
                all_title[l] = all_title[l].replace('?','')
            all_link = list(articles_alllink.values())
            if not (os.path.exists(path_article)): 
                os.makedirs(path_article)
            for m in range (0,len(all_title)):
                file = open(path_article+'\\'+all_title[m]+'.html','w',encoding='utf-8')
                link_article = url_init+all_link[m]
                print(link_article)
                res = requests.get(url=link_article,headers=headers)
                res.encoding = 'utf-8'
                file.write(res.text)
                file.close()      


if __name__ == "__main__":
    index = get_indexlink(url_init)
    pages = get_pages(index)
    get_articles_link(pages,index)

