from flask import Flask, request, jsonify
from supabase import create_client, Client
import streamlit as st

app = Flask(__name__)

# Supabase 설정
supabase_url = st.secrets["supabase"]["url"]
supabase_anon_key = st.secrets["supabase"]["anon_key"]

supabase: Client = create_client(supabase_url, supabase_anon_key)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Typeform에서 수신한 데이터
    print("Received data:", data)  # 디버깅을 위해 전체 데이터 출력

    try:
        # Typeform 응답에서 필요한 값 추출
        site_id = data["form_response"]["answers"][0]["choice"]["label"]  # 지점 선택
        satisfaction = data["form_response"]["answers"][1]["number"]  # 별점

        # Supabase에 데이터 삽입
        response = supabase.table("feedback").insert({
            "site_id": site_id,
            "satisfaction": satisfaction
        }).execute()
        print("Inserted into Supabase:", response)
        return jsonify({"status": "success"}), 200
    except KeyError as e:
        print(f"Missing key in payload: {e}")
        return jsonify({"status": "error", "message": f"Missing key: {e}"}), 400
    except Exception as e:
        print("Error inserting into Supabase:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
