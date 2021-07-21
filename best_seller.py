from pyquery import PyQuery as pq
import argparse
import time
import random

parser = argparse.ArgumentParser(
    description="抓取天瓏/博客來電腦書熱銷排行榜資料"
)
parser.add_argument(
    'site', 
    help="指定網站, 可用 tenlong, books 指定天瓏或是博客來",
    choices=['tenlong', 'books']
)
parser.add_argument(
    'period', 
    help="指定期間, 可用 7, 30 指定 7 天或是 30 天熱銷榜",
    choices=['7', '30']
)
parser.add_argument(
    '-c', '--csv', 
    help="將資料儲存到 .csv 檔",
    action="store_true"
)
args = parser.parse_args()

def go_tenlong(book):
    '''
    每一本書內容如下：

    <li class="single-book">
        <a class="cover" href="/products/9789865501457?list_name=b-m-zh_tw-2020-10">
            <img alt="Python 資料可視化之美：極專業圖表製作高手書 (全彩印刷)-cover"
                src="https://cf-assets2.tenlong.com.tw/products/images/000/152/375/medium/%E6%B7%B1%E6%99%BA-DM2038-%E7%AB%8B%E9%AB%94%E6%9B%B8.jpg?1599473075" />
            <span class="label-blue">79折</span>
            <span class="rank">21</span>
        </a>
        <div class="pricing">
            <del>$780</del>
            $616
        </div>
        <strong class="title">
            <a title="Python 資料可視化之美：極專業圖表製作高手書 (全彩印刷)" href="/products/9789865501457?list_name=b-m-zh_tw-2020-10">Python
                資料可視化之美：極專業圖表製作高手書 (全彩印刷)</a>
        </strong>
    </li>
    '''
    isbn = book.find('a').attrib['href'][10:23]                 # 從單品頁網址中取得 ISBN 號碼
    title = book.find('strong').find('a').attrib['title']       # 取得書名
    span = book.find('a').find('span')                          # 找到包含排行榜名次的元素
    while span is not None and span.attrib['class'] != 'rank':
        span = span.getnext()
    rank = 0
    if span is not None:
        rank = int(span.text)                                   # 取得名次數值
    url = 'https://www.tenlong.com.tw/products/{:s}?list_name=r-zh_tw'.format(isbn)
    page_book = pq(url)                       # 取得單品頁
    '''
    單品頁內個書籍料如下：

    <div class="item-info">
        <div class="item-header">
            <h1 class="item-title">
                自學機器學習 - 上 Kaggle 接軌世界，成為資料科學家
                <small>Kaggleで学んでハイスコアをたたき出す！ Python機械学習&amp;データ分析</small>
            </h1>
            <h3 class="item-author">
                チーム・カルポ 著
                温政堯 譯；施威銘研究室 監修
            </h3>
        </div>
        <div class="grid grid-cols-12">
            <div class="img-wrapper col-span-12 sm:col-span-4 lg:col-span-3 mx-auto">
                <a data-featherlight="https://cf-assets2.tenlong.com.tw/products/images/000/164/481/original/F1366_%E5%A4%A9%E7%93%8F.jpg?1626240465"
                    href="#">
                    <picture>
                        <source type="image/webp"
                            srcset="https://cf-assets2.tenlong.com.tw/products/images/000/164/481/webp/F1366_%E5%A4%A9%E7%93%8F.webp?1626240465" />
                        <img alt="自學機器學習 - 上 Kaggle 接軌世界，成為資料科學家"
                            src="https://cf-assets2.tenlong.com.tw/products/images/000/164/481/medium/F1366_%E5%A4%A9%E7%93%8F.jpg?1626240465" />
                    </picture>
                </a>
                <a href="#" class="item-preview btn btn-plain"><i
                        class="fa fa-eye fa-before"></i>預覽內頁</a>
            </div>

            <ul class="item-sub-info col-span-12 sm:col-span-8 lg:col-span-9 sm:px-4">
                <li>
                    <span class="info-title">
                        出版商:
                    </span>
                    <span class="info-content">
                        <a href="/publishers/8">旗標科技</a>
                    </span>
                </li>
                <li>
                    <span class="info-title">
                        出版日期:
                    </span>
                    <span class="info-content">2021-08-05</span>
                </li>
                <li>
                    <span class="info-title">定價:</span>
                    <span class="info-content">$680</span>
                </li>
                <li>
                    <span class="info-title">售價:</span>
                    <span class="info-content">
                        <span class="pricing">7.5</span> 折
                        <span class="pricing">$510</span>
                        <span class="info-content">
                </li>
                <li>
                    <span class="info-title">語言:</span>
                    <span class="info-content">繁體中文</span>
                </li>
                <li>
                    <span class="info-title">頁數:</span>
                    <span class="info-content">496</span>
                </li>
    '''
    author = page_book('.item-author').text()
    infos = page_book('.info-content a')
    pub = infos[0].text
    infos = page_book('.info-content')
    price = infos[2].text[1:]
    pub_date = infos[1].text
    pages = infos[6].text
    return rank, title, author, pub, price, pub_date

def go_books(book):
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

    在 content 屬性內的資料在作譯者欄位有時候不一致, 要特別小心：

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
    pub_date = detail[(idx_date+6):(idx_date+16)]
    if idx_author != -1:
        pub = detail[(idx_pub+4):idx_author]
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
        '''
        有些書在 content 屬性中沒有作譯者, 必須到頁面內去挖：

        <div class="type02_p003 clearfix">
            <ul>
                <li>編者： <a
                        href="//search.books.com.tw/search/query/key/%E6%96%87%E6%B7%B5%E9%96%A3%E5%B7%A5%E4%BD%9C%E5%AE%A4/adv_author/1/">文淵閣工作室</a>
                <li>出版社：<a
                        href="https://www.books.com.tw/web/sys_puballb/books/?pubid=gotop           "><span>碁峰</span></a>
                    &nbsp;<a id="trace_btn2" class="type02_btn02" href=""><span><span
                                class="trace_txt">&nbsp;</span></span></a>
                    <a href="//www.books.com.tw/activity/2015/06/trace/index.html#publisher" title="新功能介紹"
                        target="_blank"><cite class="help">新功能介紹</cite></a></li>
                <li>出版日期：2021/05/04</li>
                <li>語言：繁體中文 </li>
            </ul>
        </div>
        '''
        pub = detail[(idx_pub+4):idx_date]
        lists = page_book('.type02_p003 ul li')
        author = ''
        for item in lists:
            if item.text.startswith("編者："):
                author = author + item.find('a').text + ' 編'
            elif item.text.startswith("原文作者："):
                author = author + ' ' + item.find('a').text + ' 著'
            elif item.text.startswith("譯者："):
                author = author + ' ' + item.find('a').text + ' 譯'

    '''
    <p class="price">原價：<strong>380</strong>元</p>
    '''
    price = page_book('.price li em')[0].text
    return rank, title, author, pub, price, pub_date

# 各網站排行版資料
sites = {
    'tenlong': {                      # 天瓏排行版的資料
                                      # 本月熱銷排行榜的網址
        '30':'https://www.tenlong.com.tw/zh_tw/recent_bestselling?page={:d}&range=30',
                                      # 本週熱銷排行榜的網址
        '7':'https://www.tenlong.com.tw/zh_tw/recent_bestselling?page={:d}&range=7',
        'pages':4,                    # 分成 4 頁
        'digger':go_tenlong,          # 拆解單品頁資料的函式
        'cssselector':'.single-book'  # 排行榜頁面單一本書標籤的 CSS 選擇器
    },
    'books': {
        '30':'https://www.books.com.tw/web/sys_saletopb/books/19?attribute=30',
        '7':'https://www.books.com.tw/web/sys_saletopb/books/19?attribute=7',
        'pages':1,
        'digger':go_books,
        'cssselector':'.type02_bd-a h4 a'
    }
}

# 設定亂數種子初始值
random.seed()

# 瀏覽器識別字串
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
}

# 如果要將輸出結果存檔
if args.csv:
    # 利用目前時間組成 books_7_20210721_1331.csv 格式的檔名
    ts = time.localtime()
    fname = '{}_{}_{:4d}{:02d}{:02d}.csv'.format(
        args.site,
        args.period,
        ts.tm_year,
        ts.tm_mon,
        ts.tm_mday
    )
    # 建立檔案
    f = open(fname, 'w', encoding='utf-8')

# 論流取得排行榜的每一個分頁
for page_no in range(sites[args.site]['pages']):
    url = sites[args.site][args.period].format(page_no + 1)
    page = pq(url, headers=headers)               # 取得排行版 HTML 內容
    books = page(sites[args.site]['cssselector']) # 排行榜上每一本書是一個 single-book 類別的元素
    for book in books:                            # 處理每一本書
        rank, title, author, pub, price, pub_date = sites[args.site]['digger'](book)
        # 建立以 tab 區隔欄位的一筆資料
        fmt_str = "{:d}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\n".format( 
            rank,                                 # 排名
            title,                                # 書名
            author,                               # 作者
            pub,                                  # 出版社
            price,                                # 定價
            pub_date                              # 出版日期
        )
        print(fmt_str, end='')                    # 顯示每一本書的資料
        if args.csv:
            f.write(fmt_str)

if args.csv:
    f.close()