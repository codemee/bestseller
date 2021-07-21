from pyquery import PyQuery as pq
import time
import random

f = open('books.csv', 'w', encoding='utf-8')

random.seed()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
    }
'''
博客來電腦資訊圖書 30 天排行榜
https://www.books.com.tw/web/sys_saletopb/books/19/?loc=P_0002_021
https://www.books.com.tw/web/sys_saletopb/books/19?attribute=30
'''
url = 'https://www.books.com.tw/web/sys_saletopb/books/19?attribute=30'
page = pq(url, headers=headers)                       # 取得排行版 HTML 內容
books = page(".type02_bd-a h4 a")         # 排行榜上每一本書是一個 single-book 類別的元素
for book in books:                   # 處理每一本書
    '''
    每一本書內容如下：
    <li class="item">
        <div class="stitle">
            <p class="no_list"><span class="symbol icon_01">TOP</span><strong class="no">1</strong>
            </p>
        </div><a href="https://www.books.com.tw/products/0010822522?loc=P_0001_001"><img
                class="cover"
                src="https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/082/25/0010822522.jpg&v=5cda990c&w=150&h=150"
                alt="原子習慣：細微改變帶來巨大成就的實證法則"></a>
        <div class="type02_bd-a">
            <h4><a
                    href="https://www.books.com.tw/products/0010822522?loc=P_0001_001">原子習慣：細微改變帶來巨大成就的實證法則</a>
            </h4>
            <ul class="msg">
                <li>作者：<a
                        href='//search.books.com.tw/search/query/key/%E8%A9%B9%E5%A7%86%E6%96%AF%E2%80%A7%E5%85%8B%E5%88%A9%E7%88%BE/adv_author/1/'>詹姆斯‧克利爾</a>
                </li>
                <li class="price_a">優惠價：<strong><b>79</b></strong>折<strong><b>261</b></strong>元</li>
            </ul>
        </div>
    </li>
    '''
    title = book.text       # 取得書名
    url = book.attrib['href']      # 取得單品頁連結
    rank = int(url[-3:])
    url = url[:-15]
    # print(url)
    # url = url[:url.find('?')] if url.find('?') else url
    passed = False
    multiplier = 1
    while not passed:
        try:
            page_book = pq(url, headers=headers)
            passed = True
            if multiplier > 1:
                multiplier = multiplier - 2
        except:
            sleep_time = random.randrange(20, 30) * multiplier
            print('sleep ' + str(sleep_time) + 'secs....')
            time.sleep(sleep_time)
            multiplier = multiplier + 2

    '''
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
    <html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8">
        <meta http-equiv="Content-Language" content="zh-tw">
        <title>博客來-大數據時代超吸睛視覺化工具與技術：Tableau資料分析師進階高手養成實戰經典</title>
        <meta name="keywords" content="大數據時代超吸睛視覺化工具與技術：Tableau資料分析師進階高手養成實戰經典">
        <meta name="description"
            content="書名：大數據時代超吸睛視覺化工具與技術：Tableau資料分析師進階高手養成實戰經典，語言：繁體中文，ISBN：9789864344963，頁數：384，出版社：博碩，作者：彭其捷,劉姿嘉，出版日期：2020/07/28，類別：電腦資訊">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">

    書名：大數據時代超吸睛視覺化工具與技術：Tableau資料分析師進階高手養成實戰經典，語言：繁體中文，ISBN：9789864344963，頁數：384，出版社：博碩，作者：彭其捷,劉姿嘉，出版日期：2020/07/28，類別：電腦資訊
    書名：向藝術大師學Procreate：有iPad就能畫！初學者也能上手的Procreate插畫課，原文名稱：BEGINNER’S GUIDE TO DIGITAL PAINTING IN PROCREATE，語言：繁體中文，ISBN：9789863126638，頁數：212，出版社：旗標，譯者：吳郁芸，出版日期：2021/06/23，類別：藝術設計
    書名：資料科學的建模基礎：別急著coding！你知道模型的陷阱嗎？，原文名稱：データ分析のための数理モデル入門 本質をとらえた分析のために，語言：繁體中文，ISBN：9789863126621，頁數：296，出版社：旗標，作者：江崎貴裕，譯者：王心薇，出版日期：2021/06/11，類別：電腦資訊
    書名：我也要當 YouTuber(第二版)：百萬粉絲網紅不能說的秘密 - 拍片、剪輯、直播與宣傳實戰大揭密，語言：繁體中文，ISBN：9789865027926，頁數：256，出版社：碁峰，出版日期：2021/05/04，類別：商業理財
    '''
    detail = page_book('head meta')[3].attrib['content']
    idx_author = detail.find('，作者：')
    if idx_author == -1:
        idx_author = detail.find('，譯者：')
    idx_pub = detail.find('出版社：')
    idx_date = detail.find('，出版日期：')
    pub = detail[(idx_pub+4):idx_author]
    pub_date = detail[(idx_date+6):(idx_date+16)]
    if idx_author != -1:
        author = detail[(idx_author+4):idx_date]
        if author.find('，譯者：') == -1:
            if detail.find('，作者：') == -1:
                author = author + " 譯"    
            else:
                author = author + " 著"
        else:
            author = author.replace('，譯者：', " 著 ")
            author = author + " 譯"
    else:
        lists = book_page('.type02_p003 ul li')
        for item in lists:
            author = ''
            if item.text == "編者：":
                author = author + item.find('a').text + ' 編'
            elif item.text == "原文作者：":
                author = author + ' ' + item.find('a').text + ' 著'
            elif item.text == "譯者：":
                author = author + ' ' + item.find('a').text + ' 譯'

    price = page_book('.price li em')[0].text
    print(rank)
    f.write("{:d}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\n".format( # 顯示每一本書的資料
        rank, 
        title, 
        author,
        pub,
        price,
        pub_date
    ))

f.close()    



