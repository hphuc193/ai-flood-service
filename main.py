from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal, AIFloodPrediction
from ai_model import EnsembleFloodModel
import uuid
import datetime

# Tạo bảng trong DB nếu chưa có
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Flood Prediction Service")
ai_model = EnsembleFloodModel()

# Dependency lấy DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# DTO (Data Transfer Object) cho Input
class RealtimeDataInput(BaseModel):
    location_id: int
    current_rainfall: float
    current_water_level: float
    weather_forecast: list = [] # Có thể chứa data từ Open-Meteo

# 1. API Nhận dữ liệu từ Node.js -> Chạy AI -> Lưu DB
@app.post("/api/ai/predict")
def run_prediction(data: RealtimeDataInput, db: Session = Depends(get_db)):
    try:
        # Chạy mô hình tổ hợp
        hourly_preds, summary = ai_model.predict_24h(
            data.current_rainfall, 
            data.current_water_level, 
            data.weather_forecast
        )

        # Xóa các dự báo cũ của location này trong tương lai để cập nhật cái mới
        now = datetime.datetime.now()
        db.query(AIFloodPrediction).filter(
            AIFloodPrediction.location_id == data.location_id,
            AIFloodPrediction.target_time > now
        ).delete()

        # Lưu 24 dòng dự báo vào Database
        for pred in hourly_preds:
            db_record = AIFloodPrediction(
                id=str(uuid.uuid4()),
                location_id=data.location_id,
                target_time=pred["target_time"],
                risk_score=pred["risk_score"],
                risk_level=pred["risk_level"],
                t_start=summary["t_start"],
                t_peak=summary["t_peak"],
                t_recede=summary["t_recede"],
                h_max=summary["h_max"],
                predicted_at=now
            )
            db.add(db_record)
        
        db.commit()

        # Tìm giờ có mức độ nguy hiểm cao nhất để trả về tóm tắt ngay lập tức
        max_risk_hour = max(hourly_preds, key=lambda x: x["risk_score"])

        return {
            "success": True,
            "message": "Dự báo thành công 24h tới",
            "current_highest_risk": max_risk_hour,
            "timeline": summary
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 2. API Phục vụ biểu đồ 24h (Mobile/Node.js gọi)
@app.get("/api/ai/forecast-chart/{location_id}")
def get_forecast_chart(location_id: int, db: Session = Depends(get_db)):
    now = datetime.datetime.now()
    end_time = now + datetime.timedelta(hours=24)
    
    # Truy vấn dữ liệu 24h tới từ DB
    predictions = db.query(AIFloodPrediction).filter(
        AIFloodPrediction.location_id == location_id,
        AIFloodPrediction.target_time >= now,
        AIFloodPrediction.target_time <= end_time
    ).order_by(AIFloodPrediction.target_time.asc()).all()

    if not predictions:
        return {"success": False, "message": "Chưa có dữ liệu dự báo cho khu vực này"}

    chart_data = []
    for p in predictions:
        chart_data.append({
            "time": p.target_time.isoformat(),
            "score": p.risk_score,
            "level": p.risk_level
        })

    return {
        "success": True,
        "location_id": location_id,
        "timeline_summary": {
            "t_start": predictions[0].t_start,
            "t_peak": predictions[0].t_peak,
            "t_recede": predictions[0].t_recede,
            "h_max": predictions[0].h_max
        },
        "chart_data": chart_data
    }