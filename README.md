# 書籍銷售排行榜爬蟲

這是針對天瓏、博客來網站 7/30 天排行榜的 Python 爬蟲, 可以幫助您取得排行榜資料, 並切分為以下欄位：

1. 排名
2. 書名
3. 作者
4. 出版社
5. 定價
6. 出版日期

這裡分為兩個工具程式：

1. best_seller.py 
2. books_selenium.py
3. tenlong.py

使用時需要：

- [pyquery](https://pypi.org/project/pyquery/) 模組

- [openpyxl](https://pypi.org/project/openpyxl/)模組

## best_seller.py

這個工具原本可以取得天瓏或是博客來的排行榜資料, 目前專責天瓏。用法如下：

```
best_seller.py [-h] [-c] [-x] site period

- -h, --help   顯示使用說明頁
- -c, --csv    將結果存檔, 檔名格式為 {tenlong,books}_{7,30}_YYYYMMDD_hhmm.csv
- -x, --xlsx   將結果存檔, 檔名格式為 {tenlong,books}_{7,30}_YYYYMMDD_hhmm.xlsx
site            {tenlong,books}, 指定查詢天瓏排行榜, books 為博客來, 現在已經不支援, 請改用 books_selenium.py
period          {7,30}, 指定週或是月排行榜
```

由於博客來擋爬蟲的條件越來越嚴格, 所以博客來的排行榜另外改用 selenium 透過 Edge 瀏覽器處理：

```
books_selenium.py [-h] [-c] [-x] [-b] [-l] site period

- -h, --help    顯示使用說明頁
- -c, --csv     將結果存檔, 檔名格式為 {tenlong,books}_{7,30}_YYYYMMDD_hhmm.csv
- -x, --xlsx    將結果存檔, 檔名格式為 {tenlong,books}_{7,30}_YYYYMMDD_hhmm.xlsx
- -l, --log     顯示 log, 預設不顯示, 在不顯示瀏覽器的情況下, 還是會顯示 "DevTools listening on ws://127.0.0.1..." 的訊息, 目前無解
- -b, --browser 顯示瀏覽器視窗, 預設不顯示
site            {tenlong,books}, 指定查詢天瓏排行榜, books 為博客來, 現在已經不支援, 請改用 books_selenium.py
period          {7,30}, 指定週或是月排行榜
```

### 捷徑版本的 DOS 批次檔

為了方便一般使用者, 在倉庫中隨附上了已經安裝好相關模組的 3.12.3 版 Python, 並提供以下 DOS 批次檔作為使用的捷徑：

- tenlong7.bat：擷取天瓏當週熱銷榜並儲存至 excel 檔案

- tenlong30.bat：擷取天瓏當月熱銷榜並儲存至 excel 檔案

- books7.bat：擷取博客來 7 天熱銷榜並儲存至 excel 檔案

- books30.bat：擷取博客來 30 天熱銷榜並儲存至 excel 檔案

使用時只要直接執行批次檔 (可在檔案總管中雙按執行) 即可。

## tenlong.py

這個工具可以依據指定的年份、月份以及月數, 抓取天瓏的月排行榜 (共 120 名) 之後加總積分排名, 積分計算方式如下：

1. 當月第 1 名會得到積分 120 分, 第 120 名得到積分 1 分。

1. 每本書會加總總積分以及累計上榜月數。

最後再依據總積分排序列出所有在期間內曾上榜的書, 會列出總排名、總積分、上榜月數、書名、折扣後售價。

使用方式如下：

```
tenlong.py [-y 年份] [-m 月份] [-p 月份] [-f]
- -y 年份, 若不指定, 就是今年
- -m 月份, 若不指定, 就是這個月份, 實際會從指定月份的前一個月開始往回統計
- -p 月數, 要往回統計幾個月, 若不指定, 就是 12 個月
- -f 若有加上此選項, 表示要將統計結果存檔, 不顯示在螢幕上。存檔時檔名固定為 sYYYY_MM_plus_月數.txt
```

舉例來說, 如果以如下選項執行：

```
python tenlong.py -y 2021 -m 1 -p 3 -f
```

就會從 2021/1 的前一個月, 也就是 2020/12 開始往回 3 個月, 統計 2020/10~2020/12 這 3 個月的資料, 並且存檔到 s_2020_10_plus_03.txt 中。

## 實作說明

博客來阻擋爬蟲的方式：

1. 針對非瀏覽器 (curl 或是 Python requests 模組) 連續 (無停頓) 存取網頁會採取回應逾時的方式阻擋, 目前測試約連續兩次就會被擋, 這時需要暫停約 20 秒鐘才能再度存取。

2. 再繼續存取會鎖 IP, 會得到 200 的正常連線, 但取得的是一個顯示錯誤的頁面, 不是正確的內容。

為了應付以上問題, 還是乖乖地改用 selenium 透過瀏覽器存取博客來頁面, 不過仍會有從排行榜頁面循連結轉入單品頁取得詳細資料在返回爬行榜頁面來回 60 次後會導致 Edge 關閉, 目前測試只要暫停 30 秒後再繼續就可以正常運作。

天瓏網站目前並沒有阻擋機制。