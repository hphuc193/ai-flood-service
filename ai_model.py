import datetime
import pandas as pd
import joblib

class EnsembleFloodModel:
    def __init__(self):
        # Nạp (Load) các mô hình đã được huấn luyện vào bộ nhớ (RAM)
        try:
            self.rf_model = joblib.load('random_forest.pkl')
            self.xgb_model = joblib.load('xgboost.pkl')
            self.model_loaded = True
            print("Đã load thành công Ensemble Models (RF & XGBoost)")
        except Exception as e:
            print(f"Lỗi load model: {e}. Vui lòng chạy file train_models.py trước.")
            self.model_loaded = False

    def get_risk_level_and_action(self, score):
        if score <= 25:
            return "THẤP", "Tình hình bình thường, không cần hành động đặc biệt."
        elif score <= 50:
            return "TRUNG BÌNH", "Cần theo dõi sát sao, chuẩn bị sẵn sàng kế hoạch ứng phó."
        elif score <= 75:
            return "CAO", "Nguy cơ cao, cần di dời tài sản lên cao, chuẩn bị di tản."
        else:
            return "KHẨN CẤP", "Ngập lụt sắp/đang xảy ra, cần di tản ngay lập tức theo hướng dẫn."

    def predict_24h(self, current_rainfall, current_water_level, weather_forecast):
        predictions = []
        now = datetime.datetime.now()
        
        t_start, t_peak, t_recede = None, None, None
        h_max = 0

        # Nếu chưa có model (quên chưa chạy train), trả về lỗi
        if not self.model_loaded:
            raise Exception("AI Models chưa được khởi tạo.")

        # Lặp 24 giờ để dự đoán cho từng giờ
        for hour in range(1, 25):
            target_time = now + datetime.timedelta(hours=hour)
            
            input_df = pd.DataFrame([{
                'rainfall': current_rainfall,
                'water_level': current_water_level,
                'target_hour': hour
            }])

            # Mô hình Tổ hợp (Ensemble)
            rf_pred = self.rf_model.predict(input_df)[0]
            xgb_pred = self.xgb_model.predict(input_df)[0]
            
            # 1. Ép kiểu (Casting) ngay tại đây để bẻ gãy liên kết với Numpy
            ensemble_score = float((rf_pred + xgb_pred) / 2)
            
            # 2. Ép điểm về khoảng 0-100
            risk_score = float(max(0, min(ensemble_score, 100)))
            
            level, action = self.get_risk_level_and_action(risk_score)

            # --- Logic tính Timeline và Mực nước dựa trên điểm số ---
            simulated_water_level = risk_score * 0.8 
            if simulated_water_level > h_max:
                h_max = simulated_water_level
                t_peak = target_time
            if risk_score > 50 and t_start is None:
                t_start = target_time
            if risk_score < 50 and t_start is not None and t_recede is None:
                t_recede = target_time

            predictions.append({
                "target_time": target_time,
                "risk_score": round(risk_score, 2),
                "risk_level": level,
                "action_guide": action,
                "water_level_cm": round(simulated_water_level, 2)
            })

        summary = {
            "t_start": t_start,
            "t_peak": t_peak,
            "t_recede": t_recede,
            "h_max": round(h_max, 2)
        }

        return predictions, summary