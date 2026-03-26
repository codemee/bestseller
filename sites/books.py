from selenium.webdriver.common.by import By
import random


def go_books(book, driver):
    title = book.text                  # 取得書名
    url = book.get_attribute('href')   # 取得單品頁連結
    rank = int(url[-3:])               # 單品頁網址的最後 3 碼是排名
    url = url[:-15]                    # 單品頁網址的參數是博客來追蹤用使用者路徑使用, 不用留

    print(f"Getting URL: {url}")
    driver.get(url)                       # 點選書名連結
    driver.implicitly_wait(random.randint(1, 3))

    try:
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
        書名：向藝術大師學Procreate：有iPad就能畫！初學者也能上手的Procreate插畫課，原文名稱：BEGINNER'S GUIDE TO DIGITAL PAINTING IN PROCREATE，語言：繁體中文，ISBN：9789863126638，頁數：212，出版社：旗標，譯者：吳郁芸，出版日期：2021/06/23，類別：藝術設計
        書名：資料科學的建模基礎：別急著coding！你知道模型的陷阱嗎？，原文名稱：データ分析のための数理モデル入門 本質をとらえた分析のために，語言：繁體中文，ISBN：9789863126621，頁數：296，出版社：旗標，作者：江崎貴裕，譯者：王心薇，出版日期：2021/06/11，類別：電腦資訊
        書名：我也要當 YouTuber(第二版)：百萬粉絲網紅不能說的秘密 - 拍片、剪輯、直播與宣傳實戰大揭密，語言：繁體中文，ISBN：9789865027926，頁數：256，出版社：碁峰，出版日期：2021/05/04，類別：商業理財
        '''
        detail = driver.find_elements(By.CSS_SELECTOR, 'head meta')[3].get_attribute('content')
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
            lists = driver.find_elements(By.CSS_SELECTOR, '.type02_p003 ul li')
            author = ''
            for item in lists:
                if item.text.startswith("編者："):
                    author += item.text[3:] + ' 編'
                elif item.text.startswith("原文作者："):
                    author += item.text[5:] + ' 著'
                elif item.text.startswith("譯者："):
                    author += item.text[3:] + ' 譯'

        if len(driver.find_elements(By.CSS_SELECTOR, '.price li em')) > 0:
            '''
            <ul class="price">
            <li>定價：<em>680</em>元</li>
            <li>優惠價：<strong><b>95</b></strong>折<strong class="price01"><b>646</b></strong>元</li><li>
            '''
            price = driver.find_elements(By.CSS_SELECTOR, '.price li em')[0].text
            street_price = driver.find_elements(By.CSS_SELECTOR, '.price01 b')[0].text
            discount = driver.find_elements(By.CSS_SELECTOR, '.price li strong b')[0].text
        else:
            '''
            <ul class="price">
            <li>定價：<strong class="price01"><b>599</b></strong>元</li></ul>
            '''
            street_price = price = driver.find_elements(By.CSS_SELECTOR, '.price li strong b')[0].text
            discount = '100'

        '''
        <ul class="price">
        <li>定價：<em>500</em>元</li>
        <li>優惠價：<strong><b>5</b></strong>折<strong class="price01"><b>250</b></strong>元</li>
        '''
        if len(discount) == 1:          # 處理 5 折這樣的狀況
            discount = discount + '0'   # 補 0

        return rank, title, author, pub, price, discount, street_price, pub_date

    except Exception as e:
        print(f"[錯誤] 解析網頁失敗 (排名 {rank}, {title}, {url}): {e}")
        return None


sites = {
    'books': {
        'name': '博客來網路書店',
        'charts': {
            '30': {
                'name': '博客來 30 天排行榜',
                'url': 'https://www.books.com.tw/web/sys_saletopb/books/19?attribute=30',
                'cssselector': '.type02_bd-a h4 a'
            },
            '7': {
                'name': '博客來 7 天排行榜',
                'url': 'https://www.books.com.tw/web/sys_saletopb/books/19?attribute=7',
                'cssselector': '.type02_bd-a h4 a'
            },
            '100_comp': {
                'name': '博客來 2024 年度 100 大排行榜電腦書',
                'url': 'https://www.books.com.tw/web/annual100_cat/0116?loc=M_0005_017',
                'cssselector': 'h4 a'
            },
            '100_art': {
                'name': '博客來 2024 年度 100 大排行榜藝術書',
                'url': 'https://www.books.com.tw/web/annual100_cat/0110?loc=P_0004_011',
                'cssselector': 'h4 a'
            },
        },
        'pages': 1,           # 博客來排行榜都只有一頁
        'digger': go_books,   # 取出博客來單品頁內各項資料的函式
        'wait_min': 15,
        'wait_max': 30,
    }
}
