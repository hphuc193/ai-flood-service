# 🧠 Hệ thống Cảnh báo ngập lụt - Microservice Trí tuệ nhân tạo (AI)

Đây là kho lưu trữ chứa mã nguồn của module Trí tuệ nhân tạo (AI Microservice) thuộc dự án Khóa luận tốt nghiệp: **"Ứng dụng hỗ trợ chia sẻ và cảnh báo ngập lụt sớm tích hợp AI"**.

Hoạt động như một vi dịch vụ (microservice) hoàn toàn độc lập, ứng dụng này làm nhiệm vụ tiếp nhận dữ liệu khí tượng theo thời gian thực (lượng mưa, mực nước) từ server Node.js trung tâm, xử lý chúng qua một chuỗi các thuật toán Học máy tổ hợp (Ensemble Machine Learning), và trả về dự báo rủi ro ngập lụt trong 24 giờ tới.

## 🚀 Công nghệ & Thư viện sử dụng
- **Framework:** FastAPI (Web framework Python hiệu năng cao, xử lý bất đồng bộ).
- **Học máy (Machine Learning):** Scikit-learn (Mô hình Random Forest), XGBoost.
- **Xử lý dữ liệu:** Pandas, NumPy.
- **Cơ sở dữ liệu (ORM):** SQLAlchemy (Kết nối trực tiếp vào PostgreSQL/Supabase).
- **Web Server:** Uvicorn (Chuẩn ASGI cho Python).
- **Tài liệu API:** Tự động khởi tạo bằng Swagger UI.

## 🧠 Kiến trúc Mô hình AI (Học tổ hợp - Ensemble Learning)
Để đảm bảo độ chính xác và độ tin cậy cao nhất cho dự báo ngập lụt, dịch vụ này áp dụng phương pháp **Học tổ hợp (Ensemble Learning)**:
1. **Random Forest:** Nắm bắt các mối quan hệ phức tạp, phi tuyến tính của dữ liệu thủy văn (lượng mưa, mực nước, thời gian).
2. **XGBoost (Extreme Gradient Boosting):** Tối ưu hóa hiệu suất, giảm thiểu sai số thông qua việc xây dựng cây quyết định tuần tự.
3. **Cơ chế kết hợp:** Hệ thống tính toán trung bình cộng kết quả dự đoán của cả hai mô hình để cho ra một `Risk Score` (Điểm rủi ro từ 0 - 100%) ổn định và chính xác nhất.

### Thang đo Mức độ rủi ro:
- 🟢 **THẤP (0-25%):** Tình hình bình thường, không cần hành động đặc biệt.
- 🟡 **TRUNG BÌNH (25-50%):** Cần theo dõi sát sao, chuẩn bị sẵn sàng kế hoạch ứng phó.
- 🟠 **CAO (50-75%):** Nguy cơ cao, cần di dời tài sản lên cao, chuẩn bị di tản.
- 🔴 **KHẨN CẤP (75-100%):** Ngập lụt sắp/đang xảy ra, cần di tản ngay lập tức theo hướng dẫn.

## 📁 Cấu trúc thư mục
```text
ai-flood-service/
├── main.py               # File chạy chính của FastAPI & định nghĩa các API
├── database.py           # Cấu hình SQLAlchemy và kết nối Database
├── ai_model.py           # Chứa logic cốt lõi: Load mô hình và chạy AI dự đoán
├── requirements.txt      # Danh sách các thư viện Python cần thiết
├── random_forest.pkl     # File mô hình Random Forest đã được huấn luyện
├── xgboost.pkl           # File mô hình XGBoost đã được huấn luyện
└── .env                  # Biến môi trường hệ thống (Không đẩy lên Git)
```

## ⚙️ Hướng dẫn cài đặt (Môi trường Local)

### 1. Yêu cầu hệ thống
- Python 3.9 trở lên
- Cơ sở dữ liệu PostgreSQL (Chung với Database của server Node.js)

### 2. Thiết lập Môi trường ảo (Virtual Environment)
Clone repository về máy và tạo môi trường ảo:
```bash
git clone <your-repo-url>
cd ai-flood-service

# Tạo và kích hoạt môi trường ảo
python -m venv venv
# Trên Windows: venv\Scripts\activate
# Trên macOS/Linux: source venv/bin/activate
```

### 3. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 4. Biến môi trường (.env)
Tạo file `.env` ở thư mục gốc và dán chuỗi kết nối cơ sở dữ liệu của bạn vào:
```env
DATABASE_URL="postgresql://[user]:[password]@[host]:6543/postgres"
```

### 5. Khởi chạy Server
Bật ứng dụng FastAPI bằng Uvicorn:
```bash
uvicorn main:app --reload --port 8000
```
Giao diện tài liệu API tương tác trực quan (Swagger UI) sẽ có sẵn tại: 👉 `http://localhost:8000/docs`

## 🔗 Các API Endpoints chính
- `POST /api/ai/predict`: Tiếp nhận `lượng mưa` và `mực nước` hiện tại, AI sẽ tính toán và tự động ghi 24 mốc thời gian dự báo vào bảng `ai_flood_predictions` trong DB.
- `GET /api/ai/forecast-chart/{location_id}`: API dự phòng để truy xuất dữ liệu biểu đồ 24h.

## ☁️ Triển khai (Deployment)
Microservice này được tối ưu sẵn để đưa lên nền tảng **Render** dưới dạng Web Service.
- **Môi trường:** Python 3
- **Lệnh Build:** `pip install -r requirements.txt`
- **Lệnh Start:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
*(Cần đảm bảo biến `DATABASE_URL` đã được thiết lập trong phần Environment Variables của Render).*

## 🎓 Lời cảm ơn
Dự án Microservice AI này là một cấu phần kỹ thuật trọng tâm thuộc Khóa luận tốt nghiệp chuyên ngành Kỹ thuật phần mềm tại Trường Đại học Quản lý và Công nghệ TP.HCM (UMT), dưới sự hướng dẫn tận tình của **Ths. Nguyễn Lê Hoàng Dũng**.