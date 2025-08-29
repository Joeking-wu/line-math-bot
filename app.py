from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)  # LINE 簽名驗證失敗
    except Exception as e:
        print("Error:", e)
        abort(500)  # 其他錯誤
    
    return 'OK', 200  # 必須回傳 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 簡單回覆測試
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"你傳的是：{event.message.text}")
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
