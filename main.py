# インポートするライブラリ
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)
import os
import re

## 関数の作成

# yyyy/mm/ddかチェック
def checkAlnum(word):
    #alnum = re.compile(r'^[a-zA-Z0-9]+$')
    alnum = re.compile(r"\d{4}/\d{1,2}/\d{1,2}")
    result = alnum.match(word) is not None
    return result


# 指定の桁になるまで各桁の合計値を計算
master = ["11", "22", "33"]
def digitSum(n, i):
    if n in master:
        return n
    if len(n) == i:
        return n
    dst = sum(list(map(int, str(n))))
    return digitSum(str(dst), i)

# 辞書作成
dict_group = {"1":"みんなの中心「リーダー」グループ",
              "2":"陰でソッと支える「サポーター」グループ",
              "3":"無邪気で好奇心旺盛な「子ども」グループ",
              "4":"真面目で誠実な「堅実家」グループ",
              "5":"行動力バツグンの「自由人」グループ",
              "6":"弱者の見方！面倒見のいい「先生」グループ",
              "7":"自らのスタイルにこだわる「職人」グループ",
              "8":"常にチャレンジする熱血「ファイター」グループ",
              "9":"常に周りの空気を読む「優等生」グループ",
              "11":"「スピリチャルな才能を持つ」グループ",
              "22":"「スピリチャルな才能を持つ」グループ",
              "33":"「スピリチャルな才能を持つ」グループ"
             }

dict_pn = {"宿命数":"【生まれた時から宿っている基本的性格や特徴を表す数字】主に「過去生」から引き継いできた、持って生まれた才能、長所、得意分野などを象徴する。「宿命数」は主に「宿命期」を中心に人生の基礎・土台をつくる。",
          "運命数":"【運命を左右する、人の核となる重要な数字】「今生」での性質、価値観、考え方、行動指針、人間関係の作り方など、人格やパーソナリティ、運気を象徴する。「運命数」は主に「運命期」を中心に人生の流れ・方向性を支配する。",
          "使命数":"【抱える人生のテーマ、目標，課題、使命を表す数字】今生のチャレンジ目標を象徴し、この使命を十分に達成できないと、同じテーマが「来世」に引き継がれる場合がある。「使命数」は主に「使命期」以降、人生の後半にクローズアップされてくる。",
          "天命数":"【人生全体を陰から支え、影響を与える数字】「宿命数」「運命数」「使命数」の3つの数字が「表の数字」とするなら、「天命数」は「裏の数字」。「天命数」が示す生き方を全うする人は少ないものの、その人の後半生に特に影響を与える陰のキーナンバー。"
          }

dict_num = {"0":"あの世、宇宙、ニュートラル",
           "1":"一番、始まり、ひとつ",
           "2":"調和、受容、バランス",
           "3":"創造、笑い、子ども",
           "4":"安定、継続、形成",
           "5":"自由、変化、つながり",
           "6":"愛、美、母性",
           "7":"完成、自立、ひとり",
           "8":"情熱、無限大、豊かさ",
           "9":"完結、智慧、手放し"
           }

dict_syuku_num = {"1":"わが道を行く",
                 "2":"奥ゆかしい",
                 "3":"天真爛漫",
                 "4":"しっかり者",
                 "5":"フットワークが軽い",
                 "6":"感激屋",
                 "7":"頑固",
                 "8":"情熱的",
                 "9":"大志を抱く",
                 "10":"スケールが大きい",
                 "11":"不思議系",
                 "12":"負けず嫌い",
                 "13":"正義の味方",
                 "14":"守りが固い",
                 "15":"行動的",
                 "16":"お人好し",
                 "17":"意志が強い",
                 "18":"気さく",
                 "19":"完璧主義",
                 "20":"面倒見のいい",
                 "21":"照れ屋",
                 "22":"カリスマ性がある",
                 "23":"バランス感覚がいい",
                 "24":"協調性がある",
                 "25":"芸術家肌",
                 "26":"心優しき",
                 "27":"気高い",
                 "28":"気前がいい",
                 "29":"頼りになる",
                 "30":"自由奔放",
                 "31":"いつもニコニコ",
                 "33":"スピリチャル"
                 }

## 関数の作成：生年月日を入力すると、数秘術の分析結果を出力
def get_pn(birth = "2000/1/1"):
    print("あなたの生年月日は【" + str(birth) + "】ですね。\n")

    # 年/月/日を取得
    y, m, d = birth.split("/")

    # 各値の計算
    syukumei, unmei, shimei, tenmei = 0, 0, 0, 0
    syukumei = digitSum(d, 1)
    unmei = digitSum(y+m+d, 1)
    shimei = digitSum(m+d, 1)
    tenmei = str(sum(list(map(int, digitSum(syukumei + unmei + shimei, 1)))))

    # 結果
    #print([syukumei, unmei, shimei, tenmei])
    #print("\n")

    # アウトプット
    t1 = "■あなたの宿命数は「" + syukumei + "」です。"
    t2 = "「" + syukumei + "」は、" + dict_group[syukumei] + "に属し、特徴は「" + dict_syuku_num[syukumei] + "」です。"

    t3 = "■あなたの運命数は「" + unmei + "」です。"
    t4 = "「" + unmei + "」は、" + dict_group[unmei] + "に属し、特徴は「" + dict_syuku_num[unmei] + "」です。"

    t5 = "■あなたの使命数は「" + shimei + "」です。"
    t6 = "「" + shimei + "」は、" + dict_group[shimei] + "に属し、特徴は「" + dict_syuku_num[shimei] + "」です。"

    t7= "■あなたの天命数は「" + tenmei + "」です。"
    t8 = "「" + tenmei + "」は、" + dict_group[tenmei] + "に属し、特徴は「" + dict_syuku_num[tenmei] + "」です。"

    result = t1 + "\n" + t2 + "\n" + t3 + "\n" + t4 + "\n" + t5 + "\n" + t6 + "\n" + t7 + "\n" + t8

    #print(result)
    return result


# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)


#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_text = event.message.text
    output_text = "「" + input_text + "」ってお酒があるの？"
    #if checkAlnum(input_text):
    #    output_text = get_pn(input_text)
    #else:
    #    output_text = "生年月日を「1980/2/14」のように入力してね！"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = output_text)
     )

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
