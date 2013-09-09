#!/usr/bin/python
# -*- coding: utf-8 -*-
# filename: lianhuanhua.py
import urllib2
from urllib2 import unquote
from bs4 import BeautifulSoup
import MySQLdb  
import os
import logging  
import re
from wordpress_xmlrpc import Client
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods import media, posts,taxonomies
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.wordpress import WordPressTerm
#import feedparser  
import requests
import urlparse
import recipe

logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), level = logging.INFO)  
#conn=MySQLdb.connect(host="localhost",user="root",passwd="wangjiacan",db="wordpress",charset="utf8")  
#,unix_socket='/opt/lampp/var/mysql/mysql.sock'
all_categorys = ['数码家电', '个护化妆', '食品保健', '家居生活', '图书音像', '服饰鞋包', '母婴玩具', '钟表首饰', '运动户外', '日用百货', '杂七杂八']
web_host = 'http://wp.free3g.cn'
all_proxys = []
cur_proxy_index = 0

def raw ( text ):
    if __debug__:
        rawOutput.write ( text )

        
class FetchApp(object):
    def __init__(self):
        self.list = []
        self.rpcClient = Client(web_host+'/xmlrpc.php', 'wangbin', 'wangjiacan')
        self.categorys = []
        self.dbConn = MySQLdb.connect(host="localhost", user="root", passwd="wangjiacan", db="wordpress", charset="utf8")

    def checkCategorys(self):
        self.categorys = self.rpcClient.call(taxonomies.GetTerms('category'))      
        if len(self.categorys)<2:    
            for category in all_categorys:
                cat = WordPressTerm()
                cat.name = category
                cat.taxonomy = 'category'
                cat.id = self.rpcClient.call(taxonomies.NewTerm(cat))
            self.categorys = self.rpcClient.call(taxonomies.GetTerms('category'))
            
    # def addItem(self, item):
    #     self.list.append(item)
    
    def itemExist(self, link):
        sql = 'select * from wp_postmeta where meta_value = "%s"' % link
        cursor = self.dbConn.cursor() 
        r = cursor.execute(sql)
        cursor.close()
        return r > 0
        
    def addItem(self, item):
        # 跳转链作为唯一标识去重
#        exist_posts = self.rpcClient.call(posts.GetPosts({'custom_fields':{'key':'link_value', 'value' : item.link}}))
        if self.itemExist(item.link):
            return
        print 'item.link = '+item.link
        res = urlparse.urlparse(item.thumb)
        if len(res.query) > 0:
            qs = urlparse.parse_qs(res.query)
#    huihui图片ID
            des = qs['id'][0]
            filename = des+'.png'
            destfile = 'temp/'+filename
        else:
            filename = item.thumb[item.thumb.rfind('/'):]
            destfile = 'temp'+filename
        downloadimage(item.thumb,destfile)
        
        # prepare metadata
        data = {
                'name': filename,
                'type': 'image/png',  # mimetype
        }
        
        # read the binary file and let the XMLRPC library encode it into base64
        with open(destfile, 'rb') as img:
                data['bits'] = xmlrpc_client.Binary(img.read())
        
        response = self.rpcClient.call(media.UploadFile(data))
        attachment_id = response['id']

        post = WordPressPost()
        post.title = item.title
        post.content = item.content
        post.thumbnail = attachment_id
        post.custom_fields = [{'key':'link_value', 'value' : item.link}]
        post.id = self.rpcClient.call(posts.NewPost(post))
    #    # attachment_id.parentid = post.id
    #    # whoops, I forgot to publish it!
        post.post_status = 'publish'
        
#        cats = self.rpcClient.call(taxonomies.GetTerms('category'))
        for cat in self.categorys:
            if cat.name == item.category:
                post.terms = [cat]
                break
                
        self.rpcClient.call(posts.EditPost(post.id, post))

    def beginFetch(self):
        fetchProxy()
        self.checkCategorys()
#        fetcher = Fetcher_smzdm()
#        fetcher = Fetcher_zhizhizhi()
        fetcher = Fetcher_huihui()
        fetcher.fetchAllCategorys()
#        url = fetcher.handlejump('http://www.smzdm.com/go/177157')

theApp = FetchApp()


class GoodsItem(object):
    def __init__(self, category, title, content, link, thumb):
        self.category = category
        self.title = title
        self.content = content
        self.link = link
        self.thumb = thumb
        
        
class Fetcher(object):
    def __init__(self):
        self.name = ''
        self.categorys = []
        self.itemTag = ''
        self.itemAttrs = {}
        
    def fetchAllCategorys(self):
        for c in self.categorys:
            self.fetchCategory(c)
            
    def fetchCategory(self, category):
        print 'fetchCategory: '+ category['url']
        redirect, html = fetchPage(category['url'])
        soup = BeautifulSoup(html)
        items = soup.findAll(self.itemTag, self.itemAttrs)
        for item in items:
            self.handleItem(category['name'],item)
            
    def handleItem(self, item):
        pass
    
    def handlejump(self, url):
        redirect,html = fetchPage(url)
        #http://www.smzdm.com/go/173789 这种多次跳转并返回400错误，不好处理，先无视        
        if redirect=='' or html=='':
            return None
        
        if redirect != None:
            if redirect.find('s.click.taobao')>0:
                return get_real_taobao(redirect)
#            新蛋gbk的url做urldecode出现非法字符
            if redirect.find('newegg.com.cn')>0:
                return redirect.split('?')[0]
            index = redirect.rfind('http')
            directUrl = unquote(redirect[index:])
            if  directUrl.find('yintai.com')>0 or directUrl.find('yihaodian.com')> 0 or directUrl.find('coo8.com')> 0:
                directUrl = directUrl.split('?')[0]
            elif directUrl.find('tmall.com')>0 or directUrl.find('taobao.com')> 0:
                directUrl = unquote(directUrl)
                directUrl = directUrl.split('&')[0]
            return directUrl
        
class Fetcher_smzdm(Fetcher):
    def __init__(self):
        Fetcher.__init__(self)
        self.name = '什么值得买'
        self.itemTag = 'div'
        self.itemAttrs = {'class':'perContentBox '}
        
        cats = ['数码家电', '个护化妆', '食品保健', '家居生活', '图书音像', '服饰鞋包', '母婴玩具', '钟表首饰', '运动户外', '杂七杂八']
        for c in cats:
            self.categorys.append({'name':c,'url':'http://www.smzdm.com/category/产品类型/'+c})
            
    def handleItem(self, category, item):
        title = item.find('span', attrs={'class':'conName'})
##正文
        content = item.find('p', attrs={'class':'p_excerpt'})
        text = content.text
#    print content.text
###附加详情    
        details = item.findAll('p', attrs={'class':'p_detail'})
        text += '\r\n'.join(dt.text for dt in details)

#直达链接
        link = item.find('a', attrs={'class':'border_radius_3'})
#        imgs = None
        if link != None:
            url = link['href']
            link = self.handlejump(url)
#            print link
#            imgs = getImages(link)
    
#小图
#        if imgs != None:
#            text = text+imgs.prettify()
        img = item.find('a', attrs={'class':'imgBox'}).find('img')['src']
        if link != None:
            theApp.addItem(GoodsItem(category,title.a.text, text, link, img))
        
    def handlejump(self, url):
        redirect,html = fetchPage(url)
        #http://www.smzdm.com/go/173789 这种多次跳转并返回400错误，不好处理，先无视        
        if redirect=='' and html=='':
            return None
        
        if redirect != None:
            index = redirect.rfind('http')
            directUrl = unquote(redirect[index:])
            if directUrl.find('newegg.com.cn')>0 or directUrl.find('yihaodian.com')> 0 or directUrl.find('coo8.com')> 0:
                directUrl = directUrl.split('?')[0]
            elif directUrl.find('tmall.com')>0 or directUrl.find('taobao.com')> 0:
                directUrl = unquote(directUrl)
                directUrl = directUrl.split('&')[0]
            return directUrl
            
        p = re.search(r'u=.*?;', html)
        if p:
            u = p.group()
            directUrl = re.search(r'url=.*?;',u)
            if directUrl:
                directUrl = directUrl.group()[4:-2]
                return directUrl
                
        soup = BeautifulSoup(html)
        to = soup.find('input', attrs={'name':'to'})
        if to != None:
            return unquote(to['value'])
        
     
class Fetcher_zhizhizhi(Fetcher):
    def __init__(self):
        Fetcher.__init__(self)
        self.name = '值值值'
        self.itemTag = 'div'
        self.itemAttrs = {'id':re.compile('^post-\d+?')}
                
        cats = ['日用百货', '服饰鞋包', '数码电脑', '家用电器', '食品酒茶', '美容美体', '母婴儿童', '手表饰品', '图书软件']
        urls = ['riyong', 'fushi', 'shuma', 'jiadian', 'shipin', 'meirong', 'muying', 'biaoshi', 'tushu']
        for i in xrange(len(cats)):
            self.categorys.append({'name':cats[i],'url':'http://www.zhizhizhi.com/c/'+urls[i]})
            
    def handleItem(self, category, item):
        title = item.find('h2').text
        c = item.find('div', attrs={'class' : 'text'})
        content = c.text
        if content.find('阅读全文')>0:
            url = c.find('a', attrs={'class' : 'read-more'})['href']
            content = self.getContent(url)
        thumb = item.find('div', attrs={'class':'thumbnail'})
        img = thumb.find('img')['src']
        tags = item.findAll('span', attrs={'class' : 'tag'})
        link = 'http://www.zhizhizhi.com' + item.find('a', attrs={'class' : 'imlink_gobuy'})['href']
        link = self.handlejump(link)
#        print title,content
        if link != None:
            theApp.addItem(GoodsItem(category,title, content, link, img))
        
    def getContent(self, url):
        redirect,html = fetchPage(url)
        soup = BeautifulSoup(html)
        content = soup.find('div', attrs={'class':'textbox'})
        return content.text
        
    def handlejump(self, url):
        redirect,html = fetchPage(url)
        #http://www.smzdm.com/go/173789 这种多次跳转并返回400错误，不好处理，先无视        
        if redirect=='' or html=='':
            return None
        
        if redirect != None:
            if redirect.find('s.click.taobao')>0:
                return get_real_taobao(redirect)
            index = redirect.rfind('http')
            directUrl = unquote(redirect[index:])
            if directUrl.find('newegg.com.cn')>0 or directUrl.find('yihaodian.com')> 0 or directUrl.find('coo8.com')> 0:
                directUrl = directUrl.split('?')[0]
            elif directUrl.find('tmall.com')>0 or directUrl.find('taobao.com')> 0:
                directUrl = unquote(directUrl)
                directUrl = directUrl.split('&')[0]
            return directUrl

#图片有水印        
class Fetcher_360zdm(Fetcher):
    def __init__(self):
        Fetcher.__init__(self)
        self.name = '360值得买'
        self.itemTag = 'div'
        self.itemAttrs = {'id':re.compile('^post-\d+?')}
        cats = ['厨房电器', '个护化妆', '家用电器', '外设配件', '手机数码', '家居生活', '摄影摄像', '服装鞋帽', '电脑硬件',
                '母婴玩具', '礼品箱包', '钟表首饰', '食品饮料']
        for c in cats:
            self.categorys.append({'name':c,'url':'http://www.360zdm.com/category/商品类型/'+c})
            
    def handleItem(self, category, item):
        title = item.find('div', attrs={'class' : 'post-title'}).text
        c = item.find('div', attrs={'class' : 'entry'})
        content = c.text
        thumb = item.find('div', attrs={'class':'thumbnail'})
        img = thumb.find('img')['src']
        tags = item.findAll('span', attrs={'class' : 'tag'})
        link = 'http://www.zhizhizhi.com' + item.find('a', attrs={'class' : 'imlink_gobuy'})['href']
        link = self.handlejump(link)
#        print title,content
        if link != None:
            theApp.addItem(GoodsItem(category,title, content, link, img))
        
    def handlejump(self, url):
        pass
        
        
class Fetcher_huihui(Fetcher):
    def __init__(self):
        Fetcher.__init__(self)
        self.name = '惠惠'
        self.itemTag = 'li'
        self.itemAttrs = {'class' : 'clearfix'}
        cats = ['数码家电', '服饰鞋包', '食品百货', '母婴玩具', '运动健康', '海外购', '美妆个护', '其他类别']
        urls = ['digital', 'dresses', 'food', 'baby', 'sport', 'abroad', 'cosmetics', 'other']
        for i in xrange(len(cats)):
            self.categorys.append({'name':cats[i],'url':'http://www.huihui.cn/all/cates/'+urls[i]})
            
    def handleItem(self, category, item):
        t1 = item.find('h3')
        t2 = item.find('h4')
        if(t1==None or t2==None):
            return
        title = t1.text+t2.text
        c = item.find('div', attrs={'class' :'hui-content-text'})
#    活动结束，没有内容
        if c==None:
            return
        content = c.text
        #        a = item.find('a', attrs={'class' : re.compile('^btn-buy\w+$')})
        a = item.find('a', attrs={'href' : re.compile('/redirect$')})
#    一些攻略没有跳转目标    
        if a==None:
            return
        link = 'http://www.huihui.cn' + a['href']
        link = self.handlejump(link)
        if theApp.itemExist(link):
            return
        
        if(content.find('......')>=0):
            detailUrl = 'http://www.huihui.cn'+item.find('a', attrs={'class':'readmore js-log'})['href']
            content = self.getContent(detailUrl)
        thumb = item.find('div', attrs={'class':'hlist-list-pic'})
        img = thumb.find('img')['data-src']
        print title,content
        if link != None:
            theApp.addItem(GoodsItem(category,title, content, link, img))
        
    def getContent(self, url):
        redirect,html = fetchPage(url, True)
        soup = BeautifulSoup(html)
        content = soup.findAll('p', attrs={'class':'Strategy-indent-p editer-content'})
        result = ''
        for c in content:
            result = result+c.text
        return result
    
    
def downloadimage(imgsrc,imgdes):
    print 'download image:'+imgsrc
    try:
        req = urllib2.Request(imgsrc)
        req.add_header('Accept', '*/*')
#        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 Safari/536.11')
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:  
        logging.error(imgsrc+e.reason)
        return None
    else:
        output = open(imgdes,'wb')
        output.write(response.read())
        output.close()
    finally:
#        response.close()
        pass
        
def fetchPage(url, proxy=False):
    url = unquote(url)
    print 'fetch page: '+url
#    httpHandler = urllib2.HTTPHandler(debuglevel=1)
#    httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
#    opener = urllib2.build_opener(httpHandler, httpsHandler)
#    urllib2.install_opener(opener)
    
    if proxy:
        proxy_handler = urllib2.ProxyHandler({"http" : all_proxys[cur_proxy_index]})
        opener = urllib2.build_opener(proxy_handler)
    else:
        null_proxy_handler = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(null_proxy_handler)
#    urllib2.install_opener(opener)
    
    html = ''
    redirect = ''
    req = urllib2.Request(url)
    response = None
#    req.add_header('Referer', 'http://www.smzdm.com/')
#    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
#    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 Safari/536.11')
    try:
        response = opener.open(req, timeout=10)
        html = response.read()
        redirect = response.geturl()
    except Exception, e:  
        print e
    else:
        if cmp(redirect, url) == 0:
            redirect = ''
    finally:
        if response in dir():
            response.close()
    return redirect, html
#        return html#.decode('gb2312').encode('utf-8')

def get_real_taobao(url):
    _refer = requests.get(url).url
    headers = {'Referer': _refer}
    return requests.get(unquote(_refer.split('tu=')[1]), headers=headers).url.split('&ali_trackid=')[0]

#    sql = '''insert into wp_posts('post_author', 'post_date', 'post_date_gmt', 
#        'post_content', 'post_title', 'post_excerpt', 'post_status', 'comment_status', 
#        'ping_status', 'post_password', 'post_name', 'to_ping', 'pinged', 'post_modified',
#         'post_modified_gmt', 'post_content_filtered', 'post_parent', 'guid', 'menu_order',
#          'post_type', 'post_mime_type', 'comment_count') values
#           ('peter','2013-1-10','2013-1-10',' '''+'content.text'+"','"+'title.a.text'+"',"+''' 
#           '','publish','open','open','','zdm','','','2013-1-10','2013-1-10','','''+str(0)+''','http://free3g.cn','''+str(0)+'''
#           'post','','''+str(0)+')'
#    sql = "insert into wp_posts(post_content, post_title) values ('"+content.text+"','"+title.a.text+"')"
#    print sql
#    cursor = conn.cursor() 
#    r = cursor.execute(sql);
#    conn.commit() 
#    cursor.close() 
      
def getImages(url):
    redirect, html = fetchPage(url)
    if url.find('51buy.com') > 0:
        soup = BeautifulSoup(html)
        div = soup.find('div', attrs={'class' : 'mod_detail_info id_pic'})
        imgs = div.find('div', attrs={'class' : 'mod_bd'})
        return imgs
        
def fetchProxy():
    redirect, html = fetchPage('http://51dai.li/http_fast.html')
    soup = BeautifulSoup(html)
    items = soup.findAll('tr')
    for item in items:
        tds = item.findAll('td');
        if len(tds)!=0:
            all_proxys.append(tds[1].text+':'+tds[2].text)
    current_proxy = 'http://'+nextProxy().next()

def nextProxy():
    for item in all_proxys:
        yield item
# def getContentLocation(link):
#     h = httplib2.Http(".cache_httplib")
#     h.follow_all_redirects = True
#     resp = h.request(link, "GET")[0]
#     contentLocation = resp['content-location']
#     return contentLocation

def main():
    theApp.beginFetch()
#    theApp.fetchProxy();
#    downloadimage('http://oimageb5.ydstatic.com/image?id=2082498371676724966&product=gouwu','temp/111.png')

#    d = feedparser.parse("http://rss.zhizhizhi.com")
#    print len(d.entries)
#    for item in d.entries:
#        print item.title
#    downloadimage('http://src.zhizhizhi.com/upfiles/2013/02/133271-180x180.jpg','temp/111.jpg')
#    fetchitems('http://www.smzdm.com/category/%E4%BA%A7%E5%93%81%E7%B1%BB%E5%9E%8B/%E6%95%B0%E7%A0%81%E5%AE%B6%E7%94%B5')
#    fetcher = Fetcher_smzdm()
#    url = fetcher.handlejump('http://www.smzdm.com/go/159601')

#    testwprpc()
#    addcategorys()

#    conn = MySQLdb.connect(host='localhost', user='root',passwd='wangjiacan')
#    conn.select_db('xrs');
#    cursor = conn.cursor()      
#    cursor.execute(sql)    
    # pool = ThreadPool(5)
    # for k in categorys:
    #     pool.add_task(fetchAllBooks,k,categorys[k],conn)
    # pool.wait_completion()
#    cursor.close()    
    # connlose()  
    # # 1) Init a Thread pool with the desired number of threads

if __name__ == "__main__":
    main()
