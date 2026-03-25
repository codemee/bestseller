# 書籍銷售排行榜爬蟲

針對天瓏、博客來網站 7/30 天排行榜的 Python 爬蟲，可取得排行榜資料並切分為以下欄位：

1. 排名
2. 書名
3. 作者
4. 出版社
5. 定價
6. 折扣
7. 售價
8. 出版日期

## 工具程式

| 檔案 | 說明 |
|------|------|
| `books_selenium.py` | 主要爬蟲，以 Selenium 瀏覽器驅動抓取天瓏與博客來排行榜 |
| `best_seller.py` | 舊版爬蟲，以 pyquery 直接抓取，目前僅支援天瓏 |

## 環境需求

本專案使用 [uv](https://docs.astral.sh/uv/) 管理 Python 環境。

若尚未安裝 uv 或 git，可執行 `pre_process.bat` 自動安裝（透過 [scoop](https://scoop.sh/)）。

## books_selenium.py

以 Selenium 控制 Edge 或 Chrome 瀏覽器抓取排行榜，可支援博客來及天瓏。

### 用法

```
uv run books_selenium.py [-h] [-c] [-x] [-b] [-l] [-u {edge,chrome}] site period

site        網站識別碼：books（博客來）、tenlong（天瓏）
period      排行榜期間：7（週榜）、30（月榜）
            博客來另支援：100_comp（年度電腦書百大）、100_art（年度藝術書百大）

-h, --help              顯示使用說明
-c, --csv               將結果存為 .csv 檔，檔名格式：{site}_{period}_YYYYMMDD.csv
-x, --xlsx              將結果存為 .xlsx 檔，檔名格式：{site}_{period}_YYYYMMDD.xlsx
-b, --browser           顯示瀏覽器視窗（預設：隱藏）
-l, --log               顯示瀏覽器 log（預設：隱藏）
-u, --use {edge,chrome} 指定使用的瀏覽器（預設：edge）
```

### 範例

```bash
# 抓取博客來 7 天排行榜並存為 Excel
uv run books_selenium.py books 7 -x

# 抓取天瓏 30 天排行榜，使用 Chrome
uv run books_selenium.py tenlong 30 -x -u chrome

# 顯示瀏覽器視窗以便除錯
uv run books_selenium.py books 7 -b
```

### 擴充新網站

各網站的爬取邏輯定義在 `sites/` 資料夾下，每個 `.py` 檔案需提供：

- `sites` 字典：包含網站名稱、各排行榜的 URL、CSS 選擇器、頁數、每頁等待時間 (`wait_min`/`wait_max`)，以及 `digger` 函式
- `digger` 函式：簽名為 `digger(book, driver)`，接收排行榜頁面上的書籍元素與 WebDriver 實例，回傳 `(rank, title, author, pub, price, discount, street_price, pub_date)`

新增 `sites/新網站.py` 後無需修改主程式，`build_site_info()` 會自動載入。

## best_seller.py

舊版工具，以 pyquery 直接抓取，目前僅支援天瓏排行榜。

```
uv run best_seller.py [-h] [-c] [-x] site period

site    tenlong（天瓏）
period  7 或 30
```

## 捷徑批次檔

直接在檔案總管雙按執行即可，會自動更新程式碼並存為 Excel 檔：

| 批次檔 | 功能 |
|--------|------|
| `天瓏7.bat` | 天瓏 7 天排行榜 |
| `天瓏30.bat` | 天瓏 30 天排行榜 |
| `博客來7.bat` | 博客來 7 天排行榜 |
| `博客來30.bat` | 博客來 30 天排行榜 |

所有批次檔執行前都會先呼叫 `pre_process.bat` 確認 uv 與 git 已安裝，並執行 `git pull` 更新程式碼。

## 實作說明

### 博客來反爬蟲機制

1. 非瀏覽器（curl 或 requests）連續存取會被逾時封鎖，約連續兩次就會被擋，需暫停約 20 秒才能恢復。
2. 持續存取會鎖 IP，回應為 200 但頁面內容為錯誤頁面。
3. 無頭模式（headless）的 user-agent 包含 `HeadlessChrome` 字樣，會被識別為機器人後擋在驗證頁面，因此需手動設定 user-agent 偽裝成真實瀏覽器。

因此改用 Selenium 透過真實瀏覽器存取，並在每次載入單品頁前隨機等待 15～30 秒（設定於 `sites/books.py` 的 `wait_min`/`wait_max`）。

每個分頁使用獨立的 driver 載入排行榜頁面，每本書再另開一個獨立的 driver 取得單品頁資料，取完後關閉，避免長時間持有同一個瀏覽器實例造成不穩定。

### 天瓏

天瓏目前無反爬蟲機制，每次等待 0～1 秒（設定於 `sites/tenlong.py`）。
