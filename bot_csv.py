
from flask import Flask, request, jsonify
import pandas as pd
import difflib
import re

app = Flask(__name__)

# CSVファイルを読み込み
faq_df = pd.read_csv("faq.csv")

@app.route("/", methods=["GET"])
def health_check():
    return "Bot is running!"

@app.route("/bot", methods=["POST"])
def bot_response():
    data = request.json

    # ユーザーの発言を取り出す（空白や記号もきれいにする）
    user_text = data.get("content", {}).get("text", "").strip()
    user_text = re.sub(r"\s+", "", user_text)

    # 初期の返答（見つからないとき）
    reply = "ごめんなさい、該当する回答が見つかりませんでした。"

    if not user_text:
        return jsonify({"content": {"type": "text", "text": reply}})

    # 質問だけのリストを作成
    questions = faq_df["質問"].tolist()

    # 質問に近い言葉を見つける（0.4以上の精度で探す）
    match = difflib.get_close_matches(user_text, questions, n=1, cutoff=0.4)

    if match:
        matched_row = faq_df[faq_df["質問"] == match[0]]
        if not matched_row.empty:
            reply = matched_row.iloc[0]["回答"]

    return jsonify({"content": {"type": "text", "text": reply}})
