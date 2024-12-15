# survey_webhook.py
from fastapi import FastAPI, Request
from supabase import create_client, Client
import uvicorn

app = FastAPI()

# Supabase 설정
url = "https://<project_id>.supabase.co"
anon_key = "<anon_key>"
supabase: Client = create_client(url, anon_key)

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    response = supabase.table("feedback").insert(payload).execute()
    return {"status": "success", "data": response.data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
