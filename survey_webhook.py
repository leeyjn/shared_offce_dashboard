import os
from flask import Flask, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# Supabase 클라이언트 초기화
supabase_url = os.environ.get("SUPABASE_URL")
supabase_anon_key = os.environ.get("SUPABASE_ANON_KEY")

supabase: Client = create_client(supabase_url, supabase_anon_key)

# Webhook 엔드포인트
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data:
        # 데이터 파싱 및 Supabase에 저장
        response = supabase.table("feedback").insert(data).execute()
        return jsonify({"success": True, "response": response.data})
    return jsonify({"success": False, "error": "Invalid data"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
