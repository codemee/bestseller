from pyquery import PyQuery as pq
import time
import random

random.seed()

datetime = time.localtime(time.time()) # 取得今天日期
yyyy = datetime.tm_year                # 取得西洋年份
mm = datetime.tm_mon                   # 取得月份

data = []                              # 存放排行榜資料的字典
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
    }
'''
博客來即時榜網址
https://www.books.com.tw/web/sys_tdrntb/books/
'''
url = 'https://www.books.com.tw/web/sys_tdrntb/books/'
page = pq(url, headers=headers)                       # 取得排行版 HTML 內容
books = page(".type02_bd-a h4 a")         # 排行榜上每一本書是一個 single-book 類別的元素
rank = 1
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
    url = url[:url.find('?')] if url.find('?') else url
    print(url)
    done =False
    while not done:
        try:
            time.sleep(random.randint(10,30))
            detailPage = pq(url, headers=headers)             # 取得單品頁
            '''
            單品頁詳細資料格式：
            <h3>詳細資料</h3>
            <div class="bd">
                <ul>
                    <li>ISBN：9789869739061</li>
                    <li>叢書系列：<a
                            href='https://www.books.com.tw/web/sys_puballb/books/?se=%E5%89%B5%E5%AF%8C%E7%B3%BB%E5%88%97&pubid=berich3'>創富系列</a>
                    </li>
                    <li>規格：平裝 / 236頁 / 17 x 23 x 1.18 cm / 普通級 / 雙色印刷 / 初版</li>
                    <li>出版地：台灣 </li>
                </ul>
                <ul class="sort">
                    <li>本書分類：<a href='https://www.books.com.tw/web/books_topm_02/'>商業理財</a>&gt; <a
                            href='https://www.books.com.tw/web/books_bmidm_0209/'>投資理財</a>&gt; <a
                            href='https://www.books.com.tw/web/sys_bbotm/books/020903/'>股票／證券</a></li>
                </ul>
            </div>
            '''
            data = detailPage('.bd li')      # 取得詳細資料
            isbn = data[0].text[5:]
            if isbn:
                print("{:3d} {:s} {:s}".format(rank, isbn, title))
                done = True
        except ex:
            print(str(ex))
            pass
        if not done:
            print('retry...')  
            time.sleep(random.randint(60, 80))       # 博客來有防爬蟲, 間隔 10 秒存取才不會被強制斷線
    rank = rank + 1



