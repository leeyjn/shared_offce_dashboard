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
    try:
        # Typeform에서 받은 데이터
        data = request.json
        responses = data.get("form_response", {}).get("answers", [])

        # Supabase 테이블에 삽입할 데이터 생성
        feedback_data = {
            "site_id": next((ans["choice"]["label"] for ans in responses if ans["field"]["type"] == "multiple_choice"), None),
            "satisfaction": next((ans["number"] for ans in responses if ans["field"]["type"] == "number"), None),
        }

        # Supabase에 삽입
        supabase.table("feedback").insert(feedback_data).execute()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
