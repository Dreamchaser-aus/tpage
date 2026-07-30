from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

class Perfume(Base):
    __tablename__ = "perfumes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)         # 香水名称
    brand = Column(String, index=True)        # 品牌
    price = Column(Float)                     # 价格
    volume = Column(String)                   # 容量 (如 50ml, 100ml)
    description = Column(Text)                # 描述/香调金字塔
    image_url = Column(String)                # 图片链接
    stock = Column(Integer, default=10)       # 库存

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)            # 顾客姓名
    customer_email = Column(String)           # 顾客邮箱
    address = Column(String)                  # 收货地址
    total_price = Column(Float)               # 总金额
    status = Column(String, default="Pending")# 订单状态 (Pending/Paid)
