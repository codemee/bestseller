# 書籍銷售排行榜爬蟲

這是針對天瓏、博客來網站 7/30 天排行榜的爬蟲, 可以幫助您取得排行榜資料, 並切分為以下欄位：

1. 排名
2. 書名
3. 作者
4. 出版社
5. 定價
6. 出版日期

這裡分為兩個工具程式：

1. best_seller.py
2. tenlong.py

使用時需要 [pyquery](https://pypi.org/project/pyquery/) 模組。

## best_seller.py

這個工具可以指定參數取得天瓏或是博客來的排行榜資料, 用法如下：

```
best_seller.py [-h] [-c] site period

- -h, --help   顯示使用說明頁
- -c, --csv    將結果存檔, 檔名格式為 {tenlong,books}_{7,30}_YYYYMMDD_hhmm.csv
site            {tenlong,books}, 指定查詢天瓏或是博客來的排行榜
period          {7,30}, 指定週或是月排行榜
```

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