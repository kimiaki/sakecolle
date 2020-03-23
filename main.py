# インポートするライブラリ
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction, FlexSendMessage
)
import os
import re

#########################ベタ打ちで「酒→コナンキャラ」を作成##########

# library
import csv
import pandas as pd
import numpy as np

## 関数：酒名(orキャラ)から最も近いキャラ(or酒名)をdf_sake_konanから取得
def get_similar_name(df_sake_konan, intxt = "", sake = "", konan = ""):
    if intxt == "お酒から選ぶ":
        # お酒からキャラを選択
        rows = list(df_sake_konan.loc[sake])
        num = np.argmax(rows)
        konan = list(df_sake_konan.columns)[num]
        
    elif intxt == "コナンのキャラから選ぶ":
        # キャラからお酒を選択
        rows = list(df_sake_konan[konan])
        num = np.argmax(rows)
        sake = list(df_sake_konan.index)[num]
    
    else:
        print("Errow：データベースに存在しない値が入力されました。管理者へご連絡お願いいたします。")
        
    return [sake, konan] # [お酒, コナンキャラ]        

# csv読み込み
df_konan= pd.read_csv("./data/konan.csv",encoding="UTF-8", index_col=0)
df_sake= pd.read_csv("./data/sake.csv",encoding="UTF-8", index_col=0)

## sake-konanの距離を計算し、列を追加

# 酒とコナンキャラのリスト取得
sake_name = list(df_sake.index)
konan_name = list(df_konan.index)

# 酒とキャラの距離を格納するdfを準備
df_sake_konan = pd.DataFrame(index=list(sake_name), columns=list(konan_name))

# 酒とキャラの距離を最短二乗法で算出し、df_sake_konanに格納
for index_sake, rows_sake in df_sake.iterrows():
    rows = []
    for index_konan, rows_konan in df_konan.iterrows():
        value = np.sqrt(np.power(rows_sake - rows_konan, 2).sum())
        rows.append(value)
    #rows.append(konan_name[np.argmax(rows)])
    df_sake_konan.loc[index_sake] = rows
#df_sake_konan

#########################ここまで######################################

####################ベタ打ちでFlex Message用のjsonリスト作成###########
sake_json = {
    "type": "carousel",
    "contents": [
        {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "AKABU F 吟醸酒",
                        "size": "md",
                        "weight": "bold",
                        "style": "normal",
                        "decoration": "none",
                        "position": "relative",
                        "align": "center",
                        "gravity": "bottom",
                        "action": {
                            "type": "message",
                            "label": "action",
                            "text": "AKABU F 吟醸酒"
                        }
                    }
                ]
            },
            "action": {
                "type": "message",
                "label": "action",
                "text": "AKABU F 吟醸酒"
            }
        },
        {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "花の香 桜花 純米大吟醸",
                        "size": "md",
                        "weight": "bold",
                        "style": "normal",
                        "decoration": "none",
                        "position": "relative",
                        "align": "center",
                        "gravity": "bottom",
                        "action": {
                            "type": "message",
                            "label": "action",
                            "text": "花の香 桜花 純米大吟醸"
                        }
                    }
                ]
            },
            "action": {
                "type": "message",
                "label": "action",
                "text": "花の香 桜花 純米大吟醸"
            }
        },
        {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "七賢 風凛美山 純米",
                        "size": "md",
                        "weight": "bold",
                        "style": "normal",
                        "decoration": "none",
                        "position": "relative",
                        "align": "center",
                        "gravity": "bottom",
                        "action": {
                            "type": "message",
                            "label": "action",
                            "text": "七賢 風凛美山 純米"
                        }
                    }
                ]
            },
            "action": {
                "type": "message",
                "label": "action",
                "text": "七賢 風凛美山 純米"
            }
        },
        {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "東一 山田錦 純米",
                        "size": "md",
                        "weight": "bold",
                        "style": "normal",
                        "decoration": "none",
                        "position": "relative",
                        "align": "center",
                        "gravity": "bottom",
                        "action": {
                            "type": "message",
                            "label": "action",
                            "text": "東一 山田錦 純米"
                        }
                    }
                ]
            },
            "action": {
                "type": "message",
                "label": "action",
                "text": "東一 山田錦 純米"
            }
        },
        {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "二世古 特別純米「吟風」60％\u3000黄色ラベル",
                        "size": "md",
                        "weight": "bold",
                        "style": "normal",
                        "decoration": "none",
                        "position": "relative",
                        "align": "center",
                        "gravity": "bottom",
                        "action": {
                            "type": "message",
                            "label": "action",
                            "text": "二世古 特別純米「吟風」60％\u3000黄色ラベル"
                        }
                    }
                ]
            },
            "action": {
                "type": "message",
                "label": "action",
                "text": "二世古 特別純米「吟風」60％\u3000黄色ラベル"
            }
        },
        {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "白瀑 ど辛 純米酒",
                        "size": "md",
                        "weight": "bold",
                        "style": "normal",
                        "decoration": "none",
                        "position": "relative",
                        "align": "center",
                        "gravity": "bottom",
                        "action": {
                            "type": "message",
                            "label": "action",
                            "text": "白瀑 ど辛 純米酒"
                        }
                    }
                ]
            },
            "action": {
                "type": "message",
                "label": "action",
                "text": "白瀑 ど辛 純米酒"
            }
        },
        {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "明鏡止水 本醸造 辛口",
                        "size": "md",
                        "weight": "bold",
                        "style": "normal",
                        "decoration": "none",
                        "position": "relative",
                        "align": "center",
                        "gravity": "bottom",
                        "action": {
                            "type": "message",
                            "label": "action",
                            "text": "明鏡止水 本醸造 辛口"
                        }
                    }
                ]
            },
            "action": {
                "type": "message",
                "label": "action",
                "text": "明鏡止水 本醸造 辛口"
            }
        },
        {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "三井の寿 +14 大辛口純米吟醸 山田錦",
                        "size": "md",
                        "weight": "bold",
                        "style": "normal",
                        "decoration": "none",
                        "position": "relative",
                        "align": "center",
                        "gravity": "bottom",
                        "action": {
                            "type": "message",
                            "label": "action",
                            "text": "三井の寿 +14 大辛口純米吟醸 山田錦"
                        }
                    }
                ]
            },
            "action": {
                "type": "message",
                "label": "action",
                "text": "三井の寿 +14 大辛口純米吟醸 山田錦"
            }
        },
        {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "冩樂 純米酒",
                        "size": "md",
                        "weight": "bold",
                        "style": "normal",
                        "decoration": "none",
                        "position": "relative",
                        "align": "center",
                        "gravity": "bottom",
                        "action": {
                            "type": "message",
                            "label": "action",
                            "text": "冩樂 純米酒"
                        }
                    }
                ]
            },
            "action": {
                "type": "message",
                "label": "action",
                "text": "冩樂 純米酒"
            }
        },
        {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "獺祭 純米大吟醸45",
                        "size": "md",
                        "weight": "bold",
                        "style": "normal",
                        "decoration": "none",
                        "position": "relative",
                        "align": "center",
                        "gravity": "bottom",
                        "action": {
                            "type": "message",
                            "label": "action",
                            "text": "獺祭 純米大吟醸45"
                        }
                    }
                ]
            },
            "action": {
                "type": "message",
                "label": "action",
                "text": "獺祭 純米大吟醸45"
            }
        }        
    ]
}





#########################ここまで######################################



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

# 表現検索イベント発生のテキストリスト
event_text = ["お酒から選ぶ", "コナンのキャラから選ぶ"]

# 初期設定
event_flag1 = False
event_flag2 = False
intxt = ""
sake = ""
konan = ""

# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 入力コメントの取得
    input_text = event.message.text
    
    # イベント発生か判断
    if input_text in event_text:
        event_flag1 = True
        intxt = input_text
    if input_text in sake_name:
        event_flag2 = True
        sake = input_text
    if input_text in konan_name:
        event_flag2 = True
        konan = input_text
        
    # イベント発生時の処理
    if event_flag1:
        if event_flag2:
            # 値が入力されたら、対応するコナンのキャラ(orお酒)を取得
            sake_konan = get_similar_name(df_sake_konan, intxt = intxt , sake = sake, konan = sake)
            if sake == "":
                output_text = konan + "に最も近いお酒は『" + sake_konan[0] + "』です！"
            elif konan == "":
                output_text = sake + "に最も近いコナンのキャラクターは『" + sake_konan[1] + "』です！"
            
            # flagのリセット
            event_flag1 = False
            event_flag2 = False
            
        else:        
            # "お酒から選ぶ"と"コナンのキャラから選ぶ"に合わせて、何を調べるか、リストを返してあげる。
            # 未コーディング
            
            if input_text == "お酒から選ぶ":
                #container_obj = FlexSendMessage.new_from_json_dict(sake_json)
                output_text = "次のリストから選んで入力してね！\n※テキストをコピーして、1つだけ残して送信してください。\n\nAKABU F 吟醸酒\n花の香 桜花 純米大吟醸\n七賢 風凛美山 純米\n東一 山田錦 純米\n二世古 特別純米「吟風」60％\u3000黄色ラベル\n白瀑 ど辛 純米酒\n明鏡止水 本醸造 辛口\n三井の寿 +14 大辛口純米吟醸 山田錦\n冩樂 純米酒\n獺祭 純米大吟醸45"
            
            elif input_text == "コナンのキャラから選ぶ":
                output_text = "次のリストから選んで入力してね！\n※テキストをコピーして、1つだけ残して送信してください。\n\nジン\nウォッカ\nベルモット\nバーボン\nキャンティ\nコルン"
            
            else:
                output_text = "※実装中（リストを表示）"

                # flagのリセット（※今だけ）
                event_flag1 = False
                event_flag2 = False
        
    # 未発生時の処理（オウム返し）
    else:
        output_text = "「" + input_text + "」ってお酒があるの？\n美味しそう！！\n\nどういう表現をすると面白くなるか今考えてるから、" + input_text + "を飲みながら待っててね^^"

    # メッセージ送信

    #if input_text == "お酒から選ぶ":
    #    profile = line_bot_api.get_profile(event.source.user_id)
    #    line_user_id = profile.user_id
    #    line_bot_api.push_message(
    #        line_user_id,
    #        messages=container_obj
    #    )        
    #    
    #else:
    #    line_bot_api.reply_message(
    #        event.reply_token,
    #        TextSendMessage(text = output_text)
    #    )
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = output_text)
    )
    
    

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
