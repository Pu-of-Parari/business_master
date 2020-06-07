from flask import Flask, render_template, request, redirect, url_for
from keigo_func import loadDict, replaceKeigo, politize


# 自身の名称をappという名前でインスタンス化する
app = Flask(__name__)

# ここからウェブアプリケーション用のルーティングを記述
# indexにアクセスしたときの処理
@app.route('/')
def index():
    title = "敬語ジェネレータ"
    # message = picked_up()
    message = ""
    # index.html をレンダリングする
    return render_template('index.html',
                           message=message, title=title)

# /post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "敬語ジェネレータ"
    if request.method == 'POST':
        # リクエストフォームからテキストを取得
        name_in = request.form['name']
        name_out = politize(name_in)
        # index.html をレンダリングする
        return render_template('index.html',
                               name=name_in, name_=name_out, title=title)
    else:
        # エラーなどでリダイレクトしたい場合
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(debug=False, host='0.0.0.0') # どこからでもアクセス可能にする
    