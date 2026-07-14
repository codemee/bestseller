from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl
import argparse
import importlib
import pkgutil
import time
import datetime
import os
import random
import platform
import shutil

import sites as sites_pkg

def wait_for_seconds(seconds):
    for i in range(seconds, 0, -1):
        print(f"Waiting for {i:02d} seconds...", end='\r')
        time.sleep(1)
    print()

sites = {}
site_names = ''
site_keys = None
chart_names = ''
chart_keys = set()

def build_site_info():
    global sites, site_names, site_keys, chart_names, chart_keys
    for _finder, name, _ispkg in pkgutil.iter_modules(sites_pkg.__path__):
        module = importlib.import_module(f'sites.{name}')
        if hasattr(module, 'sites'):
            sites.update(module.sites)
    site_keys = sites.keys()
    for key_site in sites:
        site = sites[key_site]
        site_names += "{:10}：{}\n".format(key_site, site['name'])
        chart_names += "{}：\n".format(site['name'])
        for key_chart in site['charts']:
            chart = site['charts'][key_chart]
            chart_keys.add(key_chart)
            chart_names += "\t{:3}：{}\n".format(key_chart, chart['name'])

args = None

def parse_args():
    global args
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
    parser.add_argument(
        '-b', '--browser',
        help="顯示瀏覽器視窗",
        action="store_true"
    )
    parser.add_argument(
        '-l', '--log',
        help="顯示瀏覽器的 log 資訊",
        action="store_true"
    )
    parser.add_argument(
        '-u', '--use',
        help="指定使用的瀏覽器 (預設：edge)",
        choices=['edge', 'chrome'],
        default='edge'
    )
    args = parser.parse_args()

f = None
wb = None
sh = None

def create_csv_file():
    global f
    ts = time.localtime()
    fname = '{}_{}_{:4d}{:02d}{:02d}.csv'.format(
        args.site,
        args.period,
        ts.tm_year,
        ts.tm_mon,
        ts.tm_mday
    )
    f = open(fname, 'w', encoding='utf-8')

def create_spreadsheet_file():
    global wb, sh
    wb = openpyxl.workbook.Workbook()
    sh = wb.active

options = None
service = None

def config_webdriver():
    global options, service
    if args.use == 'chrome':
        options = webdriver.ChromeOptions()
        driver_path = (
            shutil.which('chromedriver')
            or shutil.which('chromium.chromedriver')
        )
        browser_path = (
            shutil.which('google-chrome')
            or shutil.which('google-chrome-stable')
            or shutil.which('chromium')
            or shutil.which('chromium-browser')
        )

        snap_browser_path = '/snap/chromium/current/usr/lib/chromium-browser/chrome'
        if (
            driver_path
            and driver_path.endswith('chromium.chromedriver')
            and os.path.exists(snap_browser_path)
        ):
            browser_path = snap_browser_path

        if browser_path:
            options.binary_location = browser_path

        if driver_path:
            service = ChromeService(executable_path=driver_path)
        elif platform.system() == 'Linux' and platform.machine() in ('aarch64', 'arm64'):
            raise RuntimeError(
                'Linux ARM64 找不到 ChromeDriver；請安裝與 Chromium 版本相符的 '
                'chromedriver（Ubuntu Snap 可使用 chromium.chromedriver）。'
            )
        else:
            service = ChromeService(ChromeDriverManager().install())
    elif args.use == 'edge':
        # 因為微軟把 Web Driver 的下載網址從 msedgedriver.azureedge.net 改到
        # msedgedriver.microsoft.com，所以要設定環境變數強制改到新網址下載
        options = webdriver.EdgeOptions()
        os.environ["SE_DRIVER_MIRROR_URL"] = "https://msedgedriver.microsoft.com"
        service = EdgeService()

    # options.add_argument('--disable-extensions')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    if not args.browser: # 不要顯示瀏覽器畫面
        # 無頭模式下，user-agent 會包含 "HeadlessChrome" 字樣
        # 需要設定 user-agent 來偽裝成真實的瀏覽器
        # 否則會被檢測為機器人，等在驗證頁面被阻擋
        my_user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
        )
        options.add_argument(f'--user-agent={my_user_agent}')
        options.add_argument('--headless')

    # 目前 headless 模式下，還是會顯示
    # DevTools listening on ws://127.0.0.1........
    # 似乎是這裡討論的問題
    # https://github.com/SeleniumHQ/selenium/issues/13095
    if not args.log:     # 不要顯示瀏覽器的 log 資訊
        options.add_argument('--log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])


def get_driver():
    if args.use == 'edge':
        return webdriver.Edge(options=options, service=service)
    else:
        return webdriver.Chrome(options=options, service=service)


def main():
    build_site_info()
    parse_args()

    if args.csv:
        create_csv_file()
    if args.xlsx:
        create_spreadsheet_file()

    site = sites[args.site]             # 要爬取排行榜的網站
    chart = site['charts'][args.period] # 要爬取的排行榜

    config_webdriver()

    # 加入博客來會員登入的 cookie
    # 首先開啟利用 cookie_editor 外掛從已登入的網頁匯出的 cookie
    # https://cookie-editor.com/
    # 要注意匯出的檔案中 cookie 的 sameSite 要改成 "None"
    # 否則會被 selenium 過濾無法加入
    # with open('cookies.json') as f:
    #     cookies = json.load(f)

    # 先開啟博客來網頁才能加入同一 domain 的 cookie
    # driver.get('https://www.books.com.tw')

    # 將匯出的 cookie 全數加入
    # for cookie in cookies:
    #     driver.add_cookie(cookie)

    # wait_for_seconds(random.randint(10, 30))
    # 重新開啟博客來網頁
    # driver.refresh()

    # 輪流取得排行榜的每一個分頁
    for page_no in range(site['pages']):
        url = chart['url'].format(page_no + 1)

        driver = get_driver()
        driver.get(url)   # 取得排行版 HTML 內容
        # driver.implicitly_wait(5)
        books = driver.find_elements(
            # 排行榜上每一本書都具有同樣的 CSS 選擇器類別
            By.CSS_SELECTOR, chart['cssselector'])
        num_books = len(books)
        for num in range(num_books):    # 處理每一本書
            book = driver.find_elements(
                By.CSS_SELECTOR,
                chart['cssselector'])[num]
            wait_for_seconds(random.randint(site['wait_min'], site['wait_max']))
            book_driver = get_driver()
            result = site['digger'](book, book_driver)
            book_driver.close()
            if result is None:
                continue
            (rank, title, author, pub, price, discount, street_price, pub_date) = result
            # 建立以 tab 區隔欄位的一筆資料
            fmt_str = "{:d}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\n".format(
                rank,           # 排名
                title,          # 書名
                author,         # 作者
                pub,            # 出版社
                price,          # 定價
                discount,       # 折扣
                street_price,   # 售價
                pub_date        # 出版日期
            )
            print(fmt_str, end='')      # 顯示每一本書的資料
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

        driver.close()

    if args.csv:
        f.close()

    if args.xlsx:
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


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n使用者中斷程式")
