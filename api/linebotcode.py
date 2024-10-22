from flask import Flask, request, abort
from linebot import LineBotApi
from linebot.v3.webhook import WebhookHandler, MessageEvent  # 從 v3 版本匯入 WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, TextSendMessage, TemplateSendMessage, CarouselColumn, \
                           CarouselTemplate, ButtonsTemplate, ConfirmTemplate, \
                           MessageAction, URIAction, ImageCarouselColumn, ImageCarouselTemplate
import os
import requests
from bs4 import BeautifulSoup
import random

line_bot_api = LineBotApi('8CtLI+CFXzbpuuAOCNa6ojQLjHaOlXOoOV1dIqyhZWdD7TCrENZ5dE7XkqsgG2oq+jly6yNse63j6vUwDImZs8pxJQMT10snC2QAT9D0Y/pvf4G8RIM6lkImgjpmFoH2sw20lnSrIJIheaYwINKx5gdB04t89/1O/w1cDnyilFU=')
line_handler = WebhookHandler("U7943cc174a84dd06f54ccdf14316fc97")

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if event.message.text == 'confirm':
        confirm_template = TemplateSendMessage(
            alt_text='confirm template',
            template=ConfirmTemplate(
                text='drink coffee?',
                actions=[
                    MessageAction(
                        label='yes',
                        text='yes'),
                    MessageAction(
                        label='no',
                        text='no')]
            )
        )
        line_bot_api.reply_message(event.reply_token, confirm_template)


    # 按鈕樣板
    if event.message.text == 'button':
        buttons_template = TemplateSendMessage(
            alt_text='buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
                title='Brown Cafe',
                text='Enjoy your coffee',
                actions=[
                    MessageAction(
                        label='咖啡有什麼好處',
                        text='讓人有精神'),
                    URIAction(
                        label='伯朗咖啡',
                        uri='https://www.mrbrown.com.tw/')]
            )
        )

        line_bot_api.reply_message(event.reply_token, buttons_template)


    # carousel 樣板
    if event.message.text == 'carousel':
        carousel_template = TemplateSendMessage(
            alt_text='carousel template',
            template=CarouselTemplate(
                columns=[
                    # 第一個
                    CarouselColumn(
                        thumbnail_image_url='https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
                        title='this is menu1',
                        text='menu1',
                        actions=[
                            MessageAction(
                                label='咖啡有什麼好處',
                                text='讓人有精神'),
                            URIAction(
                                label='伯朗咖啡',
                                uri='https://www.mrbrown.com.tw/')]),
                    # 第二個
                    CarouselColumn(
                        thumbnail_image_url='https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
                        title='this is menu2',
                        text='menu2',
                        actions=[
                            MessageAction(
                                label='咖啡有什麼好處',
                                text='讓人有精神'),
                            URIAction(
                                label='伯朗咖啡',
                                uri='https://www.mrbrown.com.tw/')])
                ])
        )

        line_bot_api.reply_message(event.reply_token, carousel_template)


    # image carousel 樣板
    if event.message.text == 'image carousel':
        image_carousel_template = TemplateSendMessage(
            alt_text='image carousel template',
            template=ImageCarouselTemplate(
                columns=[
                    # 第一張圖
                    ImageCarouselColumn(
                        image_url='https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
                        action=URIAction(
                            label='伯朗咖啡',
                            uri='https://www.mrbrown.com.tw/')),
                    # 第二張圖
                    ImageCarouselColumn(
                        image_url='https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
                        action=URIAction(
                            label='伯朗咖啡',
                            uri='https://www.mrbrown.com.tw/'))
                ])
        )

        line_bot_api.reply_message(event.reply_token, image_carousel_template)

if __name__ == "__main__":
    app.run()
