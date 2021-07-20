from pyquery import PyQuery as pq

f = open('tenlong.csv', 'w', encoding='utf-8')

'''
天瓏排行榜網頁格式
https://www.tenlong.com.tw/tw/bestselling?date=2020-11-07
'''
for page_no in range(1, 5):              # 天瓏排行版共 4 頁
    # url = "https://www.tenlong.com.tw/tw/bestselling?date={:04d}-{:02d}-{:02d}&page={:d}".format(yyyy, mm, dd, page_no)
    url = 'https://www.tenlong.com.tw/zh_tw/recent_bestselling?page={:d}&range=30'.format(page_no)
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
        price_start = priceStr.rfind("$")
        price_end = priceStr.find("\n", price_start)
        price = priceStr[price_start:price_end]
        # data.append({                                               # 新增此書基本資料
        #     'rank':rank, 
        #     'title':title, 
        #     'price':price
        # })
        url = 'https://www.tenlong.com.tw/products/{:s}?list_name=r-zh_tw'.format(isbn)
        page_book = pq(url)                       # 取得單品頁
        '''

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

# for item in data:
#     print("[{:03d}] {:s} {:s}".format( # 顯示每一本書的資料
#         item['rank'], 
#         item['title'], 
#         item['price']))
