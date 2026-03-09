from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime
import uvicorn

app = FastAPI()
host="0.0.0.0"
port=8000

# 允許跨域請求 (CORS)，這對 React Native 開發非常重要
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定義資料模型
class Contact(BaseModel):
    id: str
    name: str
    tel: str
    timestamp: str

# 模擬資料庫
db: List[Contact] = [
    Contact(id="1", name="Mike", tel="22567355", timestamp=str(datetime.now())),
    Contact(id="2", name="fds", tel="123", timestamp=str(datetime.now()))
]

# 1. 獲取所有聯絡人 (對應原本的 index_json2.php GET)
@app.get("/index_json2.php", response_model=List[Contact])
async def get_contacts():
    return db

# 2. 新增聯絡人 (對應原本的 index_json2.php POST)
# 注意：原本 PHP 使用 Form Data，所以這裡用 Form 接收
@app.post("/index_json2.php")
async def create_contact(name: str = Form(...), telephone: str = Form(...)):
    new_contact = Contact(
        id=str(uuid.uuid4()),
        name=name,
        tel=telephone,
        timestamp=str(datetime.now())
    )
    db.append(new_contact)
    return {"message": "Added", "id": new_contact.id}

# 3. 刪除聯絡人 (對應原本的 delete.php POST)
@app.post("/delete.php")
async def delete_contact(id: str = Form(...)):
    global db
    initial_len = len(db)
    db = [c for c in db if c.id != id]
    if len(db) == initial_len:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": f"ID {id} has been deleted successfully!"}

if __name__ == "__main__":
    # 啟動伺服器：uvicorn server:app --reload
    uvicorn.run(app, host=host, port=port)