from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, URITemplateAction
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
        abort(500)

    return 'OK', 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip().lower()
    if user_text in ["遊戲選單", "game"]:
        carousel_template = TemplateSendMessage(
    alt_text='遊戲選單',
    template=CarouselTemplate(
        columns=[
            # 第一排
            CarouselColumn(
                title='加法GAME',
                text='點擊開始加法遊戲',
                actions=[URITemplateAction(
                    label='玩加法',
                    uri='https://joeking-wu.github.io/multiplication-game/math_game_add.html'
                )]
            ),
            CarouselColumn(
                title='減法GAME',
                text='點擊開始減法遊戲',
                actions=[URITemplateAction(
                    label='玩減法',
                    uri='https://joeking-wu.github.io/multiplication-game/math_game_dec.html'
                )]
            ),
            CarouselColumn(
                title='寶可夢GAME',
                text='點擊開始寶可夢遊戲',
                actions=[URITemplateAction(
                    label='玩寶可夢',
                    uri='https://joeking-wu.github.io/multiplication-game/pokemon_vocab_game.html'
                )]
            ),
            # 第二排
            CarouselColumn(
                title='時鐘GAME',
                text='點擊開始時鐘遊戲',
                actions=[URITemplateAction(
                    label='玩時鐘',
                    uri='https://joeking-wu.github.io/multiplication-game/clock_matching_game.html'
                )]
            ),
            CarouselColumn(
                title='九九乘法表GAME',
                text='點擊開始九九乘法表遊戲',
                actions=[URITemplateAction(
                    label='玩九九乘法表',
                    uri='https://joeking-wu.github.io/multiplication-game/99_50.html'
                )]
            ),
            CarouselColumn(
                title='小朋友珠算入門',
                text='點擊開始珠算遊戲',
                actions=[URITemplateAction(
                    label='小朋友珠算入門',
                    uri='https://joeking-wu.github.io/multiplication-game/Abacus.html'
                )]
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

