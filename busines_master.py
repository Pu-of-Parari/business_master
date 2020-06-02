# -*- coding:utf-8 -*-

import os
import urllib.request
import json
import configparser
import codecs

from api_sample import CotohaApi

if __name__ == '__main__':
    # ソースファイルの場所取得
    APP_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"

    # 設定値取得
    config = configparser.ConfigParser()
    config.read(APP_ROOT + "config.ini")
    CLIENT_ID = config.get("COTOHA API", "Developer Client id")
    CLIENT_SECRET = config.get("COTOHA API", "Developer Client secret")
    DEVELOPER_API_BASE_URL = config.get("COTOHA API", "Developer API Base URL")
    ACCESS_TOKEN_PUBLISH_URL = config.get("COTOHA API", "Access Token Publish URL")

    # COTOHA APIインスタンス生成
    cotoha_api = CotohaApi(CLIENT_ID, CLIENT_SECRET, DEVELOPER_API_BASE_URL, ACCESS_TOKEN_PUBLISH_URL)

    # 解析対象文
    sentence = "行けたら行く"
    sentence = str(input("input>>>"))
    #sentence = "部長っちへういっすー！朝から、完全にぽんぽんペインで、つらみが深いので、一日お布団でスヤァしておきます。明日は行けたら行くマンです！"
    print("input>>",sentence)

    # 構文解析API実行
    par_result = cotoha_api.parse(sentence)
    emo_result = cotoha_api.sentimentType(sentence)
    #print(">> result: ", result)

    # 出力結果を見やすく整形
    #result_formated = json.dumps(result, indent=4, separators=(',', ': '))
    #print(codecs.decode(result_formated, 'unicode-escape'))

    # 感情分析結果出力
    #print(emo_result)
    emo = emo_result['result']['sentiment']
    emoPhrase = emo_result['result']['emotional_phrase']
    print(emo)
    for i, p in enumerate(emoPhrase):
        print(p)


    # 構文解析結果出力
    #print(par_result)
    result_formated = json.dumps(par_result, indent=4, separators=(',', ': '))
    #print(codecs.decode(result_formated, 'unicode-escape'))
    result_formated = codecs.decode(result_formated, 'unicode-escape')
    #print(result_formated)

    par_res = par_result['result']
    
    #par_token = par_res[1]['tokens']
    word_list = []
    se = ""
    pre_tok = ""
    for token in par_res:
        #print(token['tokens'])
        par_token = token['tokens']

        for tok in par_token:
            #print(tok) ## idごとに表示
            tok_form = tok['form'] ## 単語
            tok_kana = tok['kana'] ## 読み
            tok_lemma = tok['lemma'] ## 原形
            tok_pos = tok['pos'] ## 品詞
            tok_features = tok['features'] ## 副品詞

            print(tok_form,"\t",tok_pos,"\t",tok_features)
            # 食べる->食べます、食べた->食べました
            if tok_pos == "動詞接尾辞" and "終止" in tok_features:
                if tok_form == "た": tok_form = "ました"
                if tok_form == "たい": tok_form = "たいです"
                if tok_form == "う": tok_form = "ましょう"
                if tok_form == "ない": tok_form = "ません"
                else: tok_form = "ます"
            

            
            if tok_pos == "判定詞" and ("終止" in tok_features):
                if tok_form == "なの": tok_form = "でしょう"
                else: tok_form = "です"

            if "終止" in tok_features and tok_form == "い":
                tok_form = "いです"
            
            if tok_pos == "動詞語幹":
                if "M" in tok_features:
                    tok_form = tok_form + "み"
                elif "K" in tok_features:
                    tok_form = tok_form + "き"
                elif "G" in tok_features:
                    tok_form = tok_form + "ぎ"
                elif "S" in tok_features:
                    tok_form = tok_form + "し"
                elif "T" in tok_features:
                    tok_form = tok_form + "ち"
                elif "N" in tok_features:
                    tok_form = tok_form + "に"
                elif "B" in tok_features:
                    tok_form = tok_form + "び"
                elif "R" in tok_features:
                    tok_form = tok_form + "り"
                elif "IKU" in tok_features:
                    tok_form = tok_form + "き"
                elif "W" in tok_features:
                    tok_form = tok_form + "い"
                elif "SURU" in tok_features:
                    tok_form = "し"
                elif "KURU" in tok_features:
                    tok_form = "来ます"
                else: tok_form = tok_form 

            # １つ前が動詞語幹なら活用語尾は上で修正済みなので今のは消す
            if tok_pos=="動詞活用語尾" and pre_tok['pos'] == "動詞語幹":
                tok_form = "" 
            if tok_pos=="動詞接尾辞" and "連用" in tok_features and pre_tok['pos'] == "動詞語幹":
                tok_form = "" 

            # 連用形の場合は一つ前の処理を取り消し
            ##print(pre_tok)
            if tok_pos == "動詞語幹" and "連用" in tok_features:
                #se = se[len(pre_tok["form"])+1]
                se = se[:-len(pre_tok["form"])]
                tok_form = pre_tok["form"] + tok_form
                

            word_list.append(tok_form)
            se += tok_form

            pre_tok = tok
    
    #for i in word_list:
    #    print(i)
    print("output>>",se)
