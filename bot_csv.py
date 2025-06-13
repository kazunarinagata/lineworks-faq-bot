
from flask import Flask, request, jsonify
import pandas as pd
import difflib

app = Flask(__name__)

# CSVファイルを読み込み
faq_df = pd.read_csv("faq.csv")

@app.route("/", methods=["GET"])
def health_check():
    return "Bot is running!"

@app.route("/bot", methods=["POST"])
def bot_response():
    data = request.json
    user_text = data.get("content", {}).get("text", "").strip()

    # 初期応答（マッチしない場合）
    reply = "恐れ入りますが、該当する回答が見つかりませんでした。"

    if not user_text:
        return jsonify({"content": {"type": "text", "text": reply}})

    # 質問リスト取得
    questions = faq_df["質問"].tolist()

    # 類似度でマッチする質問を検索（cutoff=0.6で調整可能）
    match = difflib.get_close_matches(user_text, questions, n=1, cutoff=0.6)

    if match:
        matched_row = faq_df[faq_df["質問"] == match[0]]
        if not matched_row.empty:
            reply = matched_row.iloc[0]["回答"]

    return jsonify({"content": {"type": "text", "text": reply}})
