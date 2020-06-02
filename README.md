### COTOHAでビジネス敬語変換

#### memo

```
## 基本情報
利用中のアカウント: tatsu.m1969s@gmail.com
Access Token Publish URL: https://api.ce-cotoha.com/v1/oauth/accesstokens

## for Developersアカウント情報
Developer API Base URL: https://api.ce-cotoha.com/api/dev/
Developer Client id: djYOjSoNGISF7QLEk5HBfEOzYsQ1BqB5
Developer Client secret: RknIatuUPvNvAelh 
```



最終ゴール：ポンポンペインの文章校正

- input

  ```
  部長っちへ
  
  ういっすー！
  朝から、完全にぽんぽんペインで、
  つらみが深いので、
  一日お布団でスヤァしておきます。
  明日は行けたら行くマンです！
  ```

- output

  ```
  ○○部長
  
  おはようございます。△△です。
  明け方から腹痛が収まらないため、
  本日は病院に寄ってから出社させてください。
  なお出社は××時頃の予定です。
  病院を出たらもう一度ご連絡いたします。
  ご迷惑をおかけしていまい申し訳ございません。
  
  ```

![image-20200522135115050](C:\Users\Mae\AppData\Roaming\Typora\typora-user-images\image-20200522135115050.png)





### API memo

#### 文タイプ判定

文タイプ：

- modality

  - declarative(叙述)
  - interrogative(質問)
  - imperative(命令)

- dialog_act

  - | greeteing             | 挨拶                |
    | --------------------- | ------------------- |
    | information-providing | 情報提供            |
    | feedback              | フィードバック/相槌 |
    | information-seeking   | 情報獲得            |
    | agreement             | 同意                |
    | feedbackElicitation   | 理解確認            |
    | commissive            | 約束                |
    | acceptOffer           | 受領                |
    | selfCorrection        | 言い直し            |
    | thanking              | 感謝                |
    | apology               | 謝罪                |
    | stalling              | 時間埋め            |
    | directive             | 指示                |
    | goodbye               | 挨拶(別れ)          |
    | declineOffer          | 否認                |
    | turnAssign            | ターン譲渡          |
    | pausing               | 中断                |
    | acceptApology         | 謝罪受領            |
    | acceptThanking        | 感謝受領            |