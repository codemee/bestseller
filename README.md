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
| `send_excel_email.py` | 將最新日期的排行榜 Excel 透過 Gmail 寄給多位收件者 |

## 環境需求

本專案使用 [uv](https://docs.astral.sh/uv/) 管理 Python 環境。

Windows 可執行 `pre_process.bat` 透過 [Scoop](https://scoop.sh/) 安裝缺少的 uv 或 git。Linux 與 macOS 使用 `pre_process.sh`，缺少工具時會優先透過 [Homebrew](https://brew.sh/)安裝。

Linux ARM64 會優先使用系統中的 Chromium 與 ChromeDriver；Ubuntu Snap 安裝的 `chromium.chromedriver` 亦受支援。

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

天瓏請求預設間隔 3～5 秒。遇到 HTTP 429、5xx 或暫時性連線錯誤時，會遵守 `Retry-After` 或採指數退避重試。使用 `-x` 產生 Excel 時，每完成一本就保存當日 checkpoint；中途失敗後重新執行會自動續跑。確認 100 筆資料完整後才會原子產生正式 Excel，並刪除 checkpoint。

## 透過 Gmail 寄送 Excel

將 `.env.example` 複製為 `.env`，填入 Gmail 帳號、Google 應用程式密碼與收件人：

```dotenv
GMAIL_ADDRESS=sender@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
EMAIL_RECIPIENTS=recipient1@example.com,recipient2@example.com
```

多位收件者以逗號分隔，同一封信會寄給所有列出的地址。

請使用啟用兩步驟驗證後建立的應用程式密碼，不要使用 Gmail 的一般登入密碼。

先試跑確認附件：

```bash
uv run send_excel_email.py --dry-run
```

正式寄送：

```bash
uv run send_excel_email.py
```

也可在指令後指定其他資料夾。程式會解析 `*_YYYYMMDD.xlsx`，將日期最新一天的所有 Excel 附在同一封信中。

完整執行天瓏 7 日、博客來 7 日排行榜並寄出最新 Excel：

```bash
./排行榜7.sh
```

腳本會先執行天瓏，再執行博客來。任一來源失敗時仍會完成另一來源的抓取，但不會寄出不完整的結果；兩者都成功才會寄信。

## 排行榜捷徑

Windows 可在檔案總管雙按批次檔，執行排行榜並存為 Excel：

| 批次檔 | 功能 |
|--------|------|
| `天瓏7.bat` | 天瓏 7 天排行榜 |
| `天瓏30.bat` | 天瓏 30 天排行榜 |
| `博客來7.bat` | 博客來 7 天排行榜 |
| `博客來30.bat` | 博客來 30 天排行榜 |

批次檔執行前會先呼叫 `pre_process.bat` 檢查 uv 與 git。

Linux 與 macOS 可使用對應的 shell 腳本：

| Shell 腳本 | 功能 |
|------------|------|
| `天瓏7.sh` | 天瓏 7 天排行榜 |
| `天瓏30.sh` | 天瓏 30 天排行榜 |
| `博客來7.sh` | 博客來 7 天排行榜 |
| `博客來30.sh` | 博客來 30 天排行榜 |
| `排行榜7.sh` | 依序產生天瓏與博客來 7 天排行榜，再透過 Gmail 寄出 |

Shell 腳本執行前會呼叫 `pre_process.sh` 檢查 uv 與 git；缺少工具時優先使用 Homebrew 安裝。

## 實作說明

### 博客來反爬蟲機制

1. 非瀏覽器（curl 或 requests）連續存取會被逾時封鎖，約連續兩次就會被擋，需暫停約 20 秒才能恢復。
2. 持續存取會鎖 IP，回應為 200 但頁面內容為錯誤頁面。
3. 無頭模式（headless）的 user-agent 包含 `HeadlessChrome` 字樣，會被識別為機器人後擋在驗證頁面，因此需手動設定 user-agent 偽裝成真實瀏覽器。

因此改用 Selenium 透過真實瀏覽器存取，並在每次載入單品頁前隨機等待 15～30 秒（設定於 `sites/books.py` 的 `wait_min`/`wait_max`）。

每個分頁使用獨立的 driver 載入排行榜頁面，每本書再另開一個獨立的 driver 取得單品頁資料，取完後關閉，避免長時間持有同一個瀏覽器實例造成不穩定。

### 天瓏

`best_seller.py` 使用共用 HTTP Session，並將請求限制為每 3～5 秒一次，以避免觸發 HTTP 429。若仍被限流，最多重試 5 次，預設等待時間依序為 30、60、120、240、480 秒，伺服器提供 `Retry-After` 時則優先採用。

Excel 模式的 checkpoint 檔名為 `.tenlong_{period}_YYYYMMDD.checkpoint.json`。checkpoint 只在完整產出 Excel 後刪除，因此網路中斷或網站暫時限流後可直接用相同指令續跑。
