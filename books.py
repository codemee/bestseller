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
博客來電腦資訊圖書 30 天排行榜
https://www.books.com.tw/web/sys_saletopb/books/19/?loc=P_0002_021
'''
url = 'https://www.books.com.tw/web/sys_saletopb/books/19/?loc=P_0002_021'
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
    book_id = url[url.rfind("/") + 1:]
    print("{:03d}\t{}\t{}".format(rank, book_id, title))
    rank += 1



