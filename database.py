import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# 1. Kích hoạt thư viện để đọc file .env
load_dotenv()

# 2. Lấy giá trị DATABASE_URL từ môi trường
DATABASE_URL = os.getenv("DATABASE_URL")

# Lớp phòng ngự: Báo lỗi ngay lập tức nếu quên tạo file .env hoặc quên set biến
if not DATABASE_URL:
    raise ValueError("Lỗi: Không tìm thấy DATABASE_URL trong file .env hoặc biến môi trường!")

# 3. Khởi tạo kết nối như bình thường
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AIFloodPrediction(Base):
    __tablename__ = "ai_flood_predictions"

    id = Column(String, primary_key=True) # UUID
    location_id = Column(Integer, nullable=True)
    target_time = Column(DateTime, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    t_start = Column(DateTime, nullable=True)
    t_peak = Column(DateTime, nullable=True)
    t_recede = Column(DateTime, nullable=True)
    h_max = Column(Float, nullable=True)
    predicted_at = Column(DateTime, default=datetime.datetime.utcnow)