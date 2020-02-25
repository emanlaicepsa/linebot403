from __future__ import unicode_literals
from flask import Flask, request, abort


import datetime
import errno
import json
import os
import sys
import tempfile
from argparse import ArgumentParser

from flask import Flask, request, abort, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)

from predict403.predict import pred
from text_recognition import recognize,decode_predictions

app = Flask(__name__)

line_bot_api = LineBotApi('vqwvbwQRzcDc1DsswhpZk1p95E+Jhc8WyiHBW//3Qj09kuY6iM+RYMTepYHH1MlLsoQA0yeL3M/EoBbMPrdyQ27CuX+iqs4/cVCaIUNts3bg6jXkgn1TL2nXyr7BsBmLSE3pV4B3iDrMGY1plL9WvgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f2440c38419f7a2438de2587e5a45cf4')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_content_message(event):
    ext='jpg'
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir="D:\Desktop\linebot403\queries", prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name
    
    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)
    OCRtext = recognize(dist_path)
    result = pred(dist_path)
    
    if OCRtext != "":
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text= OCRtext)
            ])
    else:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text= result)
            ])


if __name__ == "__main__":
    app.run()