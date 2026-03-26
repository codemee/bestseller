from selenium.webdriver.common.by import By


def go_tenlong(book, driver):
    '''
    排行榜頁面每一本書的 HTML 結構如下：

    <li class="single-book">
        <a class="cover" href="/products/9789865501457?list_name=b-m-zh_tw-2020-10">
            <span class="label-blue">79折</span>
            <span class="rank">21</span>
        </a>
        <strong class="title">
            <a title="Python 資料可視化之美：極專業圖表製作高手書 (全彩印刷)"
               href="/products/9789865501457?list_name=b-m-zh_tw-2020-10">
               Python 資料可視化之美 ...
            </a>
        </strong>
    </li>

    單品頁 .info-content 結構：
    [0] 出版商（含 <a>）
    [1] 出版日期
    [2] 定價 or 空白
    ...
    .info-content .pricing：[0] 折扣, [1] 售價（若有折扣）; [0] 售價（無折扣）
    '''
    href = book.find_element(By.CSS_SELECTOR, 'a.cover').get_attribute('href')
    isbn = href.split('/products/')[1][:13]
    title = book.find_element(By.CSS_SELECTOR, 'strong.title a').get_attribute('title')

    rank_elems = book.find_elements(By.CSS_SELECTOR, 'span.rank')
    rank = int(rank_elems[0].text) if rank_elems else 0

    url = 'https://www.tenlong.com.tw/products/{:s}?list_name=r-zh_tw'.format(isbn)
    driver.get(url)

    try:
        author = driver.find_element(By.CSS_SELECTOR, '.item-author').text

        infos_a = driver.find_elements(By.CSS_SELECTOR, '.info-content a')
        pub = infos_a[0].text

        infos = driver.find_elements(By.CSS_SELECTOR, '.info-content')
        if infos[2].text.strip():
            street_price = price = infos[2].text
        else:
            street_price = price = infos[1].text

        discount = '100'
        prices = driver.find_elements(By.CSS_SELECTOR, '.info-content .pricing')
        if len(prices) > 1:
            street_price = prices[1].text
            discount = prices[0].text
        else:
            price = prices[0].text

        price = price[1:].replace(',', '')
        street_price = street_price[1:].replace(',', '')
        discount = discount.replace('.', '')
        if discount == '100':
            street_price = price

        pub_date = infos[1].text.replace('-', '/')
        if '/' not in pub_date:
            pub_date = ''

        return rank, title, author, pub, price, discount, street_price, pub_date

    except Exception as e:
        print(f"[錯誤] 解析網頁失敗 (排名 {rank}, {title}, {url}): {e}")
        return None


sites = {
    'tenlong': {
        'name': '天瓏書局',
        'charts': {
            '30': {
                'name': '天瓏 30 天排行榜',
                'url': 'https://www.tenlong.com.tw/zh_tw/recent_bestselling?page={:d}&range=30',
                'cssselector': '.single-book'
            },
            '7': {
                'name': '天瓏 7 天排行榜',
                'url': 'https://www.tenlong.com.tw/zh_tw/recent_bestselling?page={:d}&range=7',
                'cssselector': '.single-book'
            },
        },
        'pages': 4,             # 分成 4 頁
        'digger': go_tenlong,   # 取出天瓏單品頁內各項資料的函式
        'wait_min': 0,
        'wait_max': 1,
    }
}
