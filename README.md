# 0925SQL｜SQL Analytics Mart

一個用 SQLite 做的小型分析型資料庫專案。

這個 repo 原本是課堂 SQLite / GUI 練習。現在重做成一個可重建、可測試的 analytics mart，重點放在：

- schema 設計
- foreign key
- index
- reproducible seed
- 分析 SQL
- integrity checks
- query result tests

## 資料模型

```text
customers
    │
    └──< orders
           │
           └──< order_items >── products
```

### customers

客戶維度：`customer_id`、名稱、segment。

### products

商品維度：`product_id`、category、unit_cost。

### orders

訂單 header：客戶、日期、狀態。

### order_items

訂單 line item：商品、數量、成交單價。

Revenue 與 margin 都由 line item 計算，不在多個地方重複存 summary。

## 快速執行

不需要第三方 Python 套件。

```bash
python scripts/build_db.py demo.db
python scripts/run_query.py demo.db queries/monthly_revenue.sql
python -m unittest discover -s tests -v
```

## 分析查詢

### monthly_revenue.sql

依月份計算 completed orders：

- orders
- units
- revenue
- gross margin

### customer_value.sql

每個客戶：

- completed orders
- revenue
- last order date
- revenue rank

### category_margin.sql

依商品類別計算：

- units
- revenue
- gross margin
- margin rate

## Integrity checks

`src/warehouse.py` 會檢查：

- SQLite `PRAGMA integrity_check`
- `foreign_key_check`
- quantity 是否 > 0
- unit_price 是否 >= 0
- product unit_cost 是否 >= 0
- completed 訂單是否至少有一個 line item

## 為什麼不用 ORM

這個作品刻意直接寫 SQL。

如果所有邏輯都藏在 ORM，反而很難展示：

- table grain
- join
- aggregation
- window function
- constraint
- index

這裡的目標就是把 SQL 能力本身做清楚。

## 測試資料

`seed.sql` 是小型合成資料，用來讓測試結果固定且可重現。

目前已知總 completed revenue：

```text
515.00
```

這不是商業資料，也沒有拿來宣稱實際營收。

## 限制

- SQLite，不是分散式 warehouse
- 沒有 slowly changing dimension
- 沒有增量 ETL / CDC
- 沒有 timezone warehouse policy
- 資料量刻意很小，重點是模型與驗證方式
