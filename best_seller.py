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
    page_book = pq(url=url)                       # 取得單品頁
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
    還有這樣的：
    
                <li>
                    <span class="info-title">
                        出版商:
                    </span>
                    <span class="info-content">
                        <a href="/publishers/4">碁峰資訊</a>
                    </span>
                </li>
                <li>
                    <span class="info-title">定價:</span>
                    <span class="info-content">$580</span>
                </li>
                <li>
                <span class="info-title">售價:</span>
                <span class="info-content">
                    <span class="pricing">7.9</span> 折
                    <span class="pricing">$458</span>

                <span class="info-content">
                </li>
    '''
    author = page_book('.item-author').text()
    infos = page_book('.info-content a')
    pub = infos[0].text
    infos = page_book('.info-content')
    if infos[2].text.strip():
        street_price = price = infos[2].text
    else:
        street_price = price = infos[1].text
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
    # 有的書沒有折扣
    if discount == '100':
        street_price = price
    # if price[0] == '$':
    #     price = price[1:].replace(',', '')
    # else:
    #     price = page_book('.info-content .pricing')[0].text[1:].replace(',', '')
    pub_date = infos[1].text.replace('-', '/')
    # 有些書莫名其妙沒有出版日期
    if '/' not in pub_date:
        pub_date = ''
    pages = infos[6].text


    return rank, title, author, pub, price, discount, street_price, pub_date

# 各網站排行版資料
sites = {
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
    # 博客來已經改用 selenium 取得資料, 所以這個函數已經不用了
    # 'books': { # 博客來排行榜的資料
    #     'name': '博客來網路書店',
    #     'charts': {
    #         '30':{
    #             'name': '博客來 30 天排行榜',
    #             'url':'https://www.books.com.tw/web/sys_saletopb/books/19?attribute=30',
    #             'cssselector':'.type02_bd-a h4 a'
    #         },        
    #         '7':{
    #             'name': '博客來 7 天排行榜',
    #             'url':'https://www.books.com.tw/web/sys_saletopb/books/19?attribute=7',
    #             'cssselector':'.type02_bd-a h4 a'
    #         },
    #         '100':{
    #             'name': '博客來年度 100 大排行榜',
    #             'url':'https://www.books.com.tw/web/annual100_cat/2114?loc=P_0004_015',
    #             'cssselector':'.type02_m100 h4 a'
    #         },
    #     },
    #     'pages':1,            # 博客來排行榜都只有一頁
    #     'digger':go_books,    # 取出博客來單品頁內各項資料的函式
    # }
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
    headers['referer'] = url
    page = pq(url=url, headers=headers)               # 取得排行版 HTML 內容
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
            if pub_date:
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
