from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import Perfume, Order
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Perfume Store API")

class OrderCreate(BaseModel):
    perfume_id: int
    customer_name: str
    customer_email: str
    address: str

# 1. 首页轮播图数据接口
@app.get("/api/banners")
def get_banners():
    return [
        {
            "id": 1,
            "image": "https://images.unsplash.com/photo-1523293182086-7651a899d37f?q=80&w=1200&auto=format&fit=crop",
            "title": "夏日限定：清新柑橘调",
            "subtitle": "寻找属于你的阳光记忆"
        },
        {
            "id": 2,
            "image": "https://images.unsplash.com/photo-1594035910387-fea47794261f?q=80&w=1200&auto=format&fit=crop",
            "title": "优雅木质，沉香之夜",
            "subtitle": "高贵深邃，尽显独特个人魅力"
        },
        {
            "id": 3,
            "image": "https://images.unsplash.com/photo-1541643600914-78b084683601?q=80&w=1200&auto=format&fit=crop",
            "title": "浪漫玫瑰花园",
            "subtitle": "经典法式浪漫，全场限时8折"
        }
    ]

# 2. 获取所有香水列表
@app.get("/api/perfumes")
def get_perfumes(db: Session = Depends(get_db)):
    return db.query(Perfume).all()

# 3. 用户提交下单
@app.post("/api/orders")
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    perfume = db.query(Perfume).filter(Perfume.id == order_data.perfume_id).first()
    if not perfume:
        raise HTTPException(status_code=404, detail="Perfume not found")
    
    if perfume.stock <= 0:
        raise HTTPException(status_code=400, detail="Out of stock")

    new_order = Order(
        customer_name=order_data.customer_name,
        customer_email=order_data.customer_email,
        address=order_data.address,
        total_price=perfume.price,
        status="Pending"
    )
    
    perfume.stock -= 1
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    return {"message": "Order placed successfully!", "order_id": new_order.id}
