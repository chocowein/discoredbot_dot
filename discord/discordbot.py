# インストールした discord.py を読み込む
from unicodedata import name
import discord
import cv2
import numpy as np
from imread_from_url import imread_from_url


# 自分のBotのアクセストークンに置き換えてください
TOKEN = ''

# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()  # デフォルトのIntentsオブジェクトを生成
intents.typing = False  # typingを受け取らないように
client = discord.Client(intents=intents)
# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
#dot変換
def sub_color(src, K):
    Z = src.reshape((-1,3))# 次元数を1落とす
    Z = np.float32(Z)# float32型に変換
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)# 基準の定義
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)# K-means法で減色
    center = np.uint8(center)# UINT8に変換
    res = center[label.flatten()]
    return res.reshape((src.shape))# 配列の次元数と入力画像と同じに戻す

def mosaic(img, alpha):
    h, w, ch = img.shape# 画像の高さ、幅、チャンネル数
    img = cv2.resize(img,(int(w*alpha), int(h*alpha)))
    img = cv2.resize(img,(w, h), interpolation=cv2.INTER_NEAREST)# 縮小→拡大でモザイク加工
    return img

def pixel_art(img, alpha=2, K=4):
    img = mosaic(img, alpha)# モザイク処理
    return sub_color(img, K)# 減色処理


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if '!dot' in message.content:
        await message.channel.send('変換中')
        url = message.attachments[0].url
        print(url)
        name = message.author.id
        print(name)
        img = imread_from_url(url)
        dst = pixel_art(img, 0.5, 8)# ドット絵化
        cv2.imwrite("./img/"+str(name)+".png", dst)# 結果を出力
        await message.channel.send(file=discord.File("./img/"+str(name)+".png"))
        await message.channel.send('変換完了')


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)