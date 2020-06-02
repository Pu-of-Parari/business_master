# -*- coding:utf-8 -*-
import os
import urllib.request
import json
import configparser
import codecs
import csv

from api_sample import CotohaApi

DICT_DIR = "./keigo_dict.csv"

def loadDict():
    dict_dir = DICT_DIR
    DICT_LIST = []
    with open (dict_dir) as dictf:
        reader = csv.DictReader(dictf)
        #header = next(reader)

        for line in reader:
            DICT_LIST.append(line)
    
    return DICT_LIST

def replaceKeigo(word, DICT_LIST):
    for w in DICT_LIST:
        if w['org'] == word: word = w['keigo']
    
    return word


def politize(sentence):
    DICT_LIST = loadDict()

    par_result = cotoha_api.parse(sentence)
    polite_sent = "" #処理後の出力文
    pre_tok = "" #1つ前の処理を行った単語
    #pre_pre_tok = "" #2つ前の処理を行った単語
    transed_flag = 0

    # 構文解析結果出力用
    #print(par_result)
    result_formated = json.dumps(par_result, indent=4, separators=(',', ': '))
    result_formated = codecs.decode(result_formated, 'unicode-escape')
    #print(result_formated)

    par_res = par_result['result']
    #par_token = par_res[1]['tokens']
    
    for token in par_res:
        #print(token['tokens'])
        par_token = token['tokens']

        #単語ごとの処理 ここにルールを適宜追加していく
        for tok in par_token:
            #print(tok) ## idごとに表示
            tok_form = tok['form'] ## 単語
            tok_kana = tok['kana'] ## 読み
            tok_lemma = tok['lemma'] ## 原形
            tok_pos = tok['pos'] ## 品詞
            tok_features = tok['features'] ## 副品詞
            
            tok_form = replaceKeigo(tok_form, DICT_LIST)
            
            print(tok_form,"\t",tok_pos,"\t",tok_features)
            
            # 以下ルール
            # 食べる->食べます、食べた->食べました
            if tok_pos == "動詞接尾辞" and "終止" in tok_features:
                if tok_form == "た": tok_form = "ました"
                elif tok_form == "たい": tok_form = "たいです"
                #elif tok_form == "う": tok_form = "ましょう"
                elif tok_form == "ない" or tok_form == "ません": tok_form = "ません"
                else: tok_form = "ます"
            
            if tok_pos == "判定詞" and ("終止" in tok_features):
                if tok_form == "なの": tok_form = "でしょう"
                else: tok_form = "です"


            if "終止" in tok_features and tok_form == "い":
                tok_form = "いです"
            
            if tok_pos == "動詞語幹":
                v_flag = 1
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
                    v_flag = 0
                elif "KURU" in tok_features:
                    tok_form = "来ます"
                    v_flag = 0
                else:
                    tok_form = tok_form 
                    v_flag = 0

            # 連体形の処理
            if '連体' in tok_features:
                polite_sent = polite_sent[:-len(pre_tok["form"])]
                tok_form = pre_tok["form"] + tok_form
                
            # １つ前が動詞語幹の場合
            if tok_pos=="動詞活用語尾" and pre_tok['pos'] == "動詞語幹":
                tok_form = "" 
            
            # 動詞接尾辞の処理
            if tok_pos=="動詞接尾辞":
                # 連用形の処理
                if "連用" in tok_features:# and pre_tok['pos'] == "動詞語幹":
                    if pre_tok['features'] == []:
                        polite_sent = polite_sent[:-len(pre_tok["form"])]
                        tok_form = pre_tok["form"] + tok_form                        
                    # 仮定形の処理
                    elif tok_form=="たら":
                        polite_sent = polite_sent[:-len(pre_tok["form"])]
                        tok_form = pre_tok["form"] + tok_form
                    elif tok_form=="ば":
                        polite_sent = polite_sent[:-len(pre_tok["form"])]
                        tok_form = pre_tok["form"] + tok_form
                    else: tok_form = "" 
                
                # 接続形の処理
                elif "接続" in tok_features:
                    if v_flag == 1: polite_sent = polite_sent[:-len(pre_tok["form"])-1] # 動詞語幹で1文字加えた場合
                    else: polite_sent = polite_sent[:-len(pre_tok["form"])] 
                    tok_form = pre_tok["form"] + tok_form

                # 命令形の処理
                elif "命令" in tok_features:
                    #if tok_form == "": 
                    tok_form = "なさってください"
                

            # 連用形の場合は一つ前の処理を取り消し
            ##print(pre_tok)
            if tok_pos == "動詞語幹" and "連用" in tok_features:
                #se = se[len(pre_tok["form"])+1]
                polite_sent = polite_sent[:-len(pre_tok["form"])]
                tok_form = pre_tok["form"] + tok_form
                
            
            if tok_pos == "名詞" and ("姓" in tok_features or "名" in tok_features):
                tok_form = tok_form + "さん"
                
            if tok_pos == "名詞接尾辞" and pre_tok != "" and ("姓" in pre_tok['features'] or "名" in pre_tok['features']):
                tok_form = ""

            if tok_pos == "形容詞接尾辞" and "終止" in tok_features:
                tok_form = "かったです"
            
            if tok_pos == "接続接尾辞" and "終止" in tok_features:
                tok_form = "でしょう"


            polite_sent += tok_form
            #pre_pre_tok = pre_tok
            pre_tok = tok
    

    return polite_sent




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
    sentence = "マジでやっておくよ。やばいです"
    #sentence = str(input("input>>>"))
    #sentence = "部長っちへういっすー！朝から、完全にぽんぽんペインで、つらみが深いので、一日お布団でスヤァしておきます。明日は行けたら行くマンです！"
    print("input>>",sentence)

    # 感情析API実行
    emo_result = cotoha_api.sentimentType(sentence)
    #print(emo_result)
    # 感情分析結果出力
    emo = emo_result['result']['sentiment']
    emoPhrase = emo_result['result']['emotional_phrase']
    print(emo)
    for i, p in enumerate(emoPhrase):
        print(p)
    
    # 敬語付与
    poli_sent = politize(sentence)
    print(poli_sent)
    


    