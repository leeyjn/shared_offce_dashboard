from flask import Flask, request, jsonify
from supabase import create_client, Client
import streamlit as st

app = Flask(__name__)

# Supabase 설정
supabase_url = st.secrets["supabase"]["url"]
supabase_anon_key = st.secrets["supabase"]["anon_key"]

supabase: Client = create_client(supabase_url, supabase_anon_key)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data:
        # Supabase 테이블에 데이터 삽입
        response = supabase.table("feedback").insert(data).execute()
        return jsonify({"success": True, "response": response.data})
    return jsonify({"success": False, "error": "Invalid data"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
