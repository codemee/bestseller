from pyquery import PyQuery as pq
import openpyxl
import argparse
import time
import datetime
import random

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

    有些單品頁的價格長這樣, 要特別處理：

                    <span class="info-title">售價:</span>
                    <span class="info-content">
                        <span class="pricing">$620</span>
                    <span class="info-content">
    '''
    author = page_book('.item-author').text()
    infos = page_book('.info-content a')
    pub = infos[0].text
    infos = page_book('.info-content')
    street_price = price = infos[2].text
    discount = '100'
    prices = page_book('.info-content .pricing')
    if len(prices) > 1:
        street_price = prices[1].text
        discount = prices[0].text
    else:
        price = prices[0].text

    price = price[1:].replace(',', '')
    street_price = street_price[1:].replace(',', '')
    discount = discount.replace('.', '')
    # if price[0] == '$':
    #     price = price[1:].replace(',', '')
    # else:
    #     price = page_book('.info-content .pricing')[0].text[1:].replace(',', '')
    pub_date = infos[1].text.replace('-', '/')
    pages = infos[6].text


    return rank, title, author, pub, price, discount, street_price, pub_date

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
    title = book.text              # 取得書名
    url = book.attrib['href']      # 取得單品頁連結
    rank = int(url[-3:])           # 單品頁網址的最後 3 碼是排名
    url = url[:-15]                # 單品頁網址的參數是博客來追蹤用使用者路徑使用, 不用留
    
    # 連續讀取博客來頁面會被擋, 通常等 20 秒可通過
    # 但落連續次數太多, 就需要等約 1 分鐘以後才能讀取
    passed = False                 # 尚未通過博客來擋爬蟲
    multiplier = 1                 # 等候時間的乘數

    # 測試用, 只處理單一本書
    # if rank != 1:
    #     return rank, title, 'mee', 'mee', '800', '2021/07/21'
    
    # 先隨機等待時間, 不過好像沒差
    # sleep_time = random.randrange(2, 10)           # 用亂數決定等待時間
    # print('sleep ' + str(sleep_time) + ' secs....') # 假裝不是爬蟲機器人
    # time.sleep(sleep_time)                         # 等待

    while not passed:
        try:
            page_book = pq(url, headers=headers)  # 嘗試取得頁面
            passed = True                         # 成功取得頁面
            if multiplier > 1:                    # 如果是多次等待
                multiplier = multiplier - 2       # 遞減乘數
        except:                                   # 被擋無法取得頁面
            sleep_time = random.randrange(20, 30) * multiplier # 用亂數決定等待時間
            print('sleep ' + str(sleep_time) + ' secs....')    # 假裝不是爬蟲機器人
            time.sleep(sleep_time)                # 等待
            multiplier = multiplier + 2           # 每失敗一次, 乘數加 2

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
    <ul class="price">
    <li>定價：<em>680</em>元</li>
    <li>優惠價：<strong><b>95</b></strong>折<strong class="price01"><b>646</b></strong>元</li><li>
    '''
    price = page_book('.price li em')[0].text
    street_price = page_book('.price01 b')[0].text
    discount = page_book('.price li strong b')[0].text
    '''
    <ul class="price">
    <li>定價：<em>500</em>元</li>
    <li>優惠價：<strong><b>5</b></strong>折<strong class="price01"><b>250</b></strong>元</li>
    '''
    if len(discount) == 1:          # 處理 5 折這樣的狀況        
        discount = discount + '0'   # 補 0
    return rank, title, author, pub, price, discount, street_price, pub_date

# 各網站排行版資料
sites = {
    # 每個排行榜的資料結構如下：
    # '網站識別名稱 (自取)': {
    #    'name': '網站完整名稱',
    #    'charts': {
    #       '排行榜識別代號': {
    #            'name': '排行榜完整名稱',
    #           'url': '排行榜網址',
    #           'cssselector': '單本書在網頁內的 CSS 選擇器'
    #       },
    #    }
    #    'pages': 排行榜的頁數,
    #    'digger': 從排行榜單本書元素再取出單品頁找出細項資料的函式
    # }
    'tenlong': { # 天瓏排行榜的資料
        'name': '天瓏書局',
        'charts': {
            '30':{
                'name': '天瓏 30 天排行榜',
                'url':'https://www.tenlong.com.tw/zh_tw/recent_bestselling?page={:d}&range=30',
                'cssselector':'.single-book'
            },                                      
            '7':{
                'name': '天瓏 7 天排行榜',
                'url':'https://www.tenlong.com.tw/zh_tw/recent_bestselling?page={:d}&range=7',
                'cssselector':'.single-book'
            },
        },                              
        'pages':4,             # 分成 4 頁
        'digger':go_tenlong,   # 取出天瓏單品頁內各項資料的函式
    },
    'books': { # 博客來排行榜的資料
        'name': '博客來網路書店',
        'charts': {
            '30':{
                'name': '博客來 30 天排行榜',
                'url':'https://www.books.com.tw/web/sys_saletopb/books/19?attribute=30',
                'cssselector':'.type02_bd-a h4 a'
            },        
            '7':{
                'name': '博客來 7 天排行榜',
                'url':'https://www.books.com.tw/web/sys_saletopb/books/19?attribute=7',
                'cssselector':'.type02_bd-a h4 a'
            },
            '100':{
                'name': '博客來年度 100 大排行榜',
                'url':'https://www.books.com.tw/web/annual100_cat/2114?loc=P_0004_015',
                'cssselector':'.type02_m100 h4 a'
            },
        },
        'pages':1,            # 博客來排行榜都只有一頁
        'digger':go_books,    # 取出博客來單品頁內各項資料的函式
    }
}

site_names = ''          # 取得所有的網站識別名稱與完整名稱
site_keys = sites.keys() # 取得所有網站的代碼
chart_names = ''         # 取得所有排行榜的代碼與完整名稱
chart_keys = set()       # 取得所有排行榜的代碼

for key_site in sites:
    site = sites[key_site]
    site_names += "{:10}：{}\n".format(key_site, site['name'])
    chart_names += "{}：\n".format(site['name'])
    for key_chart in site['charts']:
        chart = site['charts'][key_chart]
        chart_keys.add(key_chart)
        chart_names += "\t{:3}：{}\n".format(key_chart, chart['name'])

parser = argparse.ArgumentParser(
    description="抓取天瓏/博客來電腦書熱銷排行榜資料",
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument(
    'site', 
    help=f"網站識別名稱, 可用的網站識別名稱如下：\n{site_names}\n",
    choices=site_keys
)

parser.add_argument(
    'period', 
    help=f"期間代號, 可用的代號如下：\n{chart_names}\n",
    choices=list(chart_keys)
)

parser.add_argument(
    '-c', '--csv', 
    help="將資料儲存到 .csv 檔",
    action="store_true"
)

parser.add_argument(
    '-x', '--xlsx', 
    help="將資料儲存到 .xlsx 檔",
    action="store_true"
)

args = parser.parse_args()   # 解析命令列參數

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

# 如果要將輸出結果存檔
if args.xlsx:
    # 建立空的試算表
    wb = openpyxl.workbook.Workbook()
    sh = wb.active

# 設定亂數種子初始值
random.seed()

# 瀏覽器識別字串
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
}

site = sites[args.site]                # 要爬取排行榜的網站
chart = site['charts'][args.period]    # 要爬取的排行榜

# 論流取得排行榜的每一個分頁
for page_no in range(site['pages']):
    url = chart['url'].format(page_no + 1)
    page = pq(url, headers=headers)               # 取得排行版 HTML 內容
    books = page(chart['cssselector'])            # 排行榜上每一本書都具有同樣的 CSS 選擇器類別
    for book in books:                            # 處理每一本書
        rank, title, author, pub, price, discount, street_price, pub_date = site['digger'](book)
        # 建立以 tab 區隔欄位的一筆資料
        fmt_str = "{:d}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\n".format( 
            rank,                                 # 排名
            title,                                # 書名
            author,                               # 作者
            pub,                                  # 出版社
            price,                                # 定價
            discount,                             # 折扣
            street_price,                         # 售價
            pub_date                              # 出版日期
        )
        print(fmt_str, end='')                    # 顯示每一本書的資料
        if args.csv:
            f.write(fmt_str)

        # 使用 openpyxl 寫入 excel 檔
        if args.xlsx:
            sh['A' + str(rank)].value = int(rank)
            sh['B' + str(rank)].value = title
            sh['C' + str(rank)].value = author
            sh['D' + str(rank)].value = pub
            sh['E' + str(rank)].value = int(price)
            sh['F' + str(rank)].value = float(discount)
            sh['G' + str(rank)].value = int(street_price)
            sh['H' + str(rank)].value = datetime.datetime.strptime(pub_date, '%Y/%m/%d')
            sh['H' + str(rank)].number_format = 'YYYY/MM/DD'

if args.csv:
    f.close()

if args.xlsx:
    # 利用目前時間組成 books_7_20210721_1331.xlsx 格式的檔名
    ts = time.localtime()
    fname = '{}_{}_{:4d}{:02d}{:02d}.xlsx'.format(
        args.site,
        args.period,
        ts.tm_year,
        ts.tm_mon,
        ts.tm_mday
    )
    wb.save(fname)
    wb.close()
