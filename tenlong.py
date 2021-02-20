from pyquery import PyQuery as pq
import time

datetime = time.localtime(time.time()) # 取得今天日期
yyyy = datetime.tm_year                # 取得西洋年份
mm = datetime.tm_mon                   # 取得月份

data = {}                              # 存放排行榜資料的字典

for i in range(12):                          # 從前一個月開始往回爬 12 個月得資料
    mm = 12 if mm == 1 else (mm - 1)         # 跨年時回到 12 月
    yyyy = (yyyy - 1) if mm == 12 else yyyy  # 跨年時調整西洋年份

    '''
    天瓏排行榜網頁格式
    https://www.tenlong.com.tw/tw/bestselling?date=2020-11-07
    '''
    for page_no in range(1, 5):              # 天瓏排行版共 4 頁
        url = "https://www.tenlong.com.tw/tw/bestselling?date={:04d}-{:02d}-28&page={:d}".format(yyyy, mm, page_no)
        # print(url)
        page = pq(url)                       # 取得排行版 HTML 內容
        books = page(".single-book")         # 排行榜上每一本書是一個 single-book 類別的元素
        for book in books:                   # 處理每一本書
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
            priceStr = book.find('div').text_content()
            price = priceStr[priceStr.rfind("$"):priceStr.rfind("\n")]
            if isbn not in data:                                        # 若是未曾出現過的書
                data[isbn] = {'title':title, 'score':0, 'months':0, 'price':price}     # 新增此書基本資料
            data[isbn]['score'] += (121 - rank)                         # 累計分數, 名次 1 得 120 分, 120 名得 1 分
            data[isbn]['months'] += 1                                   # 累計上榜月數
            # print(rank, isbn, title)

score_order = sorted(data.items(), key=lambda x:x[1]['score'], reverse=True) # 依據分數從高到低排序

for item in score_order:
    # print(item)
    print("{:4d} ({:2d}) {:s} {:s}".format(item[1]['score'], item[1]['months'], item[1]['title'], item[1]['price']))  # 顯示每一本書的資料