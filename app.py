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
    ImagemapSendMessage,
    BaseSize,
    URIImagemapAction,
    ImagemapArea,
    URITemplateAction,
    MessageImagemapAction,
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
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        print("Error:", e)
        return 'Error', 200 

    return 'OK', 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip().lower()

    if user_text in ["圖片選單", "2"]:
        # 這裡使用您提供的圖片網址。
        image_url = "https://i.imgur.com/mB9yDO0.png"

        print(image_url.rsplit('/', 1)[0])
        # 建立一個 ImagemapSendMessage 訊息
        # BaseSize 的 height 和 width 必須與您圖片的實際尺寸相符。
        # 您的圖片尺寸為 1040x235 像素。
        imagemap_message = ImagemapSendMessage(
        base_url='https://joeking-wu.github.io/line-math-bot/imagemap',
        alt_text='數學機器人選單',
        base_size=BaseSize(height=1040, width=1040),
        actions=[
            MessageImagemapAction(text='基礎運算', area=ImagemapArea(x=0, y=0, width=520, height=520)),
            MessageImagemapAction(text='進階數學', area=ImagemapArea(x=520, y=0, width=520, height=520)),
            MessageImagemapAction(text='方程式求解', area=ImagemapArea(x=0, y=520, width=520, height=520)),
            MessageImagemapAction(text='圖形計算', area=ImagemapArea(x=520, y=520, width=520, height=520))
        ]
        )
        # 回覆 Imagemap 訊息
        line_bot_api.reply_message(event.reply_token, imagemap_message)

    elif user_text in ["選單1", "menu"]:
        buttons_template = TemplateSendMessage(
            alt_text='課程遊戲選單',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/3s1uL7y.png',
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

    elif user_text in ["遊戲選單", "game"]:
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
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"你傳的是：{event.message.text}")
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render 會自動給 PORT
    app.run(host="0.0.0.0", port=port)















