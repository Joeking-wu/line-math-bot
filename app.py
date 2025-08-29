from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    TemplateSendMessage,
    CarouselTemplate,
    CarouselColumn,
    ButtonsTemplate,
    ImagemapSendMessage, # 新增 ImagemapSendMessage
    BaseSize, # 新增 BaseSize
    URIImagemapAction, # 新增 URIImagemapAction
    ImagemapArea, # 新增 ImagemapArea
    URITemplateAction,
)
import os

app = Flask(__name__)

# 從環境變數讀取
line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        # 處理來自 LINE 的請求
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 簽名無效時拋出錯誤
        abort(400)
    except Exception as e:
        # 其他錯誤處理
        print("Error:", e)
        abort(500)

    return 'OK', 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 將使用者傳來的文字轉為小寫並移除前後空白
    user_text = event.message.text.strip().lower()

    # 如果使用者輸入 "圖片選單" 或 "image"
    if user_text in ["圖片選單", "image"]:
        # 圖片選單的圖片網址
        # 建議使用您自己製作的圖片，並上傳到可公開存取的空間
        image_url = "https://github.com/Joeking-wu/line-math-bot/blob/main/blue.png?raw=true"
        
        # 建立一個 ImagemapSendMessage 訊息
        imagemap_message = ImagemapSendMessage(
            base_url=image_url.rsplit('/', 1)[0],
            alt_text='網頁遊戲選單',
            base_size=BaseSize(height=86, width=380),
            actions=[
                # 第一個按鈕 (加法遊戲)
                URIImagemapAction(
                    link_uri='https://joeking-wu.github.io/multiplication-game/math_game_add.html',
                    area=ImagemapArea(x=0, y=0, width=200, height=15)
                ),
                # 第二個按鈕 (減法遊戲)
                URIImagemapAction(
                    link_uri='https://joeking-wu.github.io/multiplication-game/math_game_dec.html',
                    area=ImagemapArea(x=0, y=25, width=200, height=15)
                ),
                # 第三個按鈕 (寶可夢遊戲)
                URIImagemapAction(
                    link_uri='https://joeking-wu.github.io/multiplication-game/pokemon_vocab_game.html',
                    area=ImagemapArea(x=0, y=50, width=1040, height=15)
                ),
                # 第四個按鈕 (時鐘遊戲)
                URIImagemapAction(
                    link_uri='https://joeking-wu.github.io/multiplication-game/clock_matching_game.html',
                    area=ImagemapArea(x=0, y=200, width=200, height=86)
                ),
            ]
        )
        # 回覆 Imagemap 訊息
        line_bot_api.reply_message(event.reply_token, imagemap_message)

    # 如果使用者輸入 "選單" 或 "menu"
    elif user_text in ["選單", "menu"]:
        # 建立一個按鈕樣板訊息
        buttons_template = TemplateSendMessage(
            alt_text='課程遊戲選單',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/3s1uL7y.png', # 您可以替換為課程相關圖片
                title='我的網頁遊戲',
                text='請選擇您想玩的遊戲：',
                actions=[
                    URITemplateAction(
                        label='加法遊戲',
                        uri='https://joeking-wu.github.io/multiplication-game/math_game_add.html'
                    ),
                    URITemplateAction(
                        label='減法遊戲',
                        uri='https://joeking-wu.github.io/multiplication-game/math_game_dec.html'
                    ),
                    URITemplateAction(
                        label='寶可夢遊戲',
                        uri='https://joeking-wu.github.io/multiplication-game/pokemon_vocab_game.html'
                    ),
                    URITemplateAction(
                        label='時鐘遊戲',
                        uri='https://joeking-wu.github.io/multiplication-game/clock_matching_game.html'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)

    # 如果使用者輸入 "遊戲選單" 或 "game"
    elif user_text in ["遊戲選單", "game"]:
        # 輪播樣板訊息 (保留您原本的程式碼)
        carousel_template = TemplateSendMessage(
            alt_text='遊戲選單',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='數學與遊戲',
                        text='第一排遊戲',
                        actions=[
                            URITemplateAction(
                                label='加法GAME',
                                uri='https://joeking-wu.github.io/multiplication-game/math_game_add.html'
                            ),
                            URITemplateAction(
                                label='減法GAME',
                                uri='https://joeking-wu.github.io/multiplication-game/math_game_dec.html'
                            ),
                            URITemplateAction(
                                label='寶可夢GAME',
                                uri='https://joeking-wu.github.io/multiplication-game/pokemon_vocab_game.html'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        title='數學與遊戲',
                        text='第二排遊戲',
                        actions=[
                            URITemplateAction(
                                label='時鐘GAME',
                                uri='https://joeking-wu.github.io/multiplication-game/clock_matching_game.html'
                            ),
                            URITemplateAction(
                                label='九九乘法表GAME',
                                uri='https://joeking-wu.github.io/multiplication-game/99_50.html'
                            ),
                            URITemplateAction(
                                label='小朋友珠算入門',
                                uri='https://joeking-wu.github.io/multiplication-game/Abacus.html'
                            ),
                        ]
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template)
    else:
        # 預設回覆
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"你傳的是：{event.message.text}")
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


