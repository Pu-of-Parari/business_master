# Business_master
[COTOHA API](https://api.ce-cotoha.com/contents/index.html)を用いた自動敬語変換ツール

絶賛開発中

## Usage

`python app.py`

```
$ python app.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

```

- ブラウザから`localhost:5000`にアクセス



## 目的
- 一般的な言葉遣いの文を敬語表現を用いた文に自動校正するツールを作る

- 裏目的
  - フロントエンド修行
  - Git開発に慣れる
  - agileっぽく開発できたらいいな

## 仕様
`input: str` 一般的な言葉遣いの文章

`output: str` ビジネス敬語に変換された文書

フロント、サーバに関する仕様も順次追加していく



## TODO
- フロント関係
   - ~~HTML/CSSでプロトタイプUI作成~~
   - CSSで装飾
   - React用いてWebアプリ化
- サーバ関係
   - ~~flaskを用いて仮サーバ建てる~~
- ルールをさらに深堀り
   - できたらテスト書く
