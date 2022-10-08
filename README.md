# Overview
説明変数CSVを入力することでユーザ満足度*（High or Low）の二値分類結果をCSV出力するWebAPIです。

*ユーザ満足度の定義
| Low | High|
|-----|-----|
| 1-3 | 4-5 |

# Installation
```
pip install uvicorn
pip install fastapi
```
# Usage
#### 1.

```bash
git clone https://github.com/Ryo0615/test.git
cd test
uvicorn main:app --reload
```

#### 2. 
```
http://127.0.0.1:8000/docs
```

#### 3. 「POST/predict」を選択
![image](https://user-images.githubusercontent.com/55380019/194704790-37ebea75-6272-4b5a-8cf4-7a6dfed0d3db.png)

#### 4. 「Try it out」→「ファイル選択」→「Execute」で実行
![スクリーンショット 2022-10-07 231927](https://user-images.githubusercontent.com/55380019/194576353-8d56c8d7-e088-4d0a-ab8c-fb4328bea144.png)

#### 5. 「Download file」で結果をダウンロード
![image](https://user-images.githubusercontent.com/55380019/194704901-d3d40202-1814-43d3-b8dd-3e4e16ff51b5.png)

# Note
※バリデーションはできてません

# Author

# License
