# 🎨 AI Image Generator - Backend & Frontend

Ứng dụng chuyển đổi ảnh với AI sử dụng Stable Diffusion và Gemini AI, được chia thành backend API và frontend web riêng biệt.

## 📁 Cấu trúc dự án

```
gen_image/
├── backend/                 # Backend API
│   └── app.py              # Flask API server
├── frontend/               # Frontend web
│   ├── index.html          # Trang chính
│   ├── styles.css          # CSS styles
│   ├── script.js           # JavaScript logic
│   └── README.md           # Hướng dẫn frontend
├── gen/                    # Core modules
│   ├── gen_cpu.py         # Image generator
│   └── gen_prompt.py      # Prompt generator
├── requirements_api.txt    # Backend dependencies
├── README_API.md          # Hướng dẫn API
└── README_SEPARATE.md     # Hướng dẫn này
```

## 🚀 Tính năng chính

### Backend API
- **Flask REST API**: API thuần túy không có frontend
- **Image Processing**: Xử lý ảnh với Stable Diffusion
- **AI Prompt Generation**: Tự động tạo prompt tối ưu với Gemini AI
- **File Management**: Quản lý file tạm thời
- **Error Handling**: Xử lý lỗi toàn diện
- **CORS Support**: Hỗ trợ cross-origin requests

### Frontend Web
- **Modern UI**: Giao diện hiện đại với gradient và animation
- **Responsive Design**: Hoạt động tốt trên mọi thiết bị
- **Drag & Drop**: Upload ảnh bằng kéo thả
- **Real-time Validation**: Kiểm tra input real-time
- **Loading States**: Hiển thị trạng thái xử lý
- **Error Handling**: Xử lý lỗi thân thiện

## 🛠️ Cài đặt

### 1. Clone repository
```bash
git clone <repository-url>
cd gen_image
```

### 2. Tạo môi trường ảo
```bash
python -m venv gen_image_cpu
source gen_image_cpu/bin/activate  # Linux/Mac
# hoặc
gen_image_cpu\Scripts\activate     # Windows
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements_api.txt
```

### 4. Cấu hình API key (tùy chọn)
Tạo file `.env` trong thư mục gốc:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

## 🚀 Chạy ứng dụng

### 1. Khởi động Backend
```bash
cd backend
python app.py
```

Backend sẽ chạy tại: `http://localhost:5000`

### 2. Mở Frontend
Có thể mở file `frontend/index.html` trực tiếp hoặc sử dụng local server:

```bash
cd frontend
python -m http.server 8000
```

Frontend sẽ chạy tại: `http://localhost:8000`

## 📖 API Endpoints

### POST `/api/generate`
Tạo ảnh từ ảnh đầu vào và prompt

**Parameters:**
- `userRequest` (string): Mô tả yêu cầu chuyển đổi ảnh
- `imageFile` (file): File ảnh đầu vào
- `strength` (float, optional): Độ mạnh chuyển đổi (0.1-1.0)
- `steps` (int, optional): Số bước inference (10-50)
- `guidance` (float, optional): Guidance scale (1-20)
- `useAutoParams` (boolean, optional): Tự động tối ưu thông số

**Response:**
```json
{
  "success": true,
  "prompt": "Generated prompt from AI",
  "parameters": {
    "steps": 35,
    "cfg_scale": 7.5,
    "strength": 0.8
  },
  "image": "base64_encoded_image_data"
}
```

### GET `/api/health`
Kiểm tra trạng thái server

### GET `/api/test`
Test endpoint

## 🎯 Cách sử dụng

### 1. Qua Frontend Web
1. Mở `http://localhost:8000` trong trình duyệt
2. Nhập mô tả yêu cầu chuyển đổi ảnh
3. Chọn hoặc kéo thả file ảnh
4. Điều chỉnh thông số (tùy chọn)
5. Nhấn "Tạo Ảnh"
6. Chờ xử lý và tải xuống kết quả

### 2. Qua API trực tiếp
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "userRequest=Chuyển ảnh này thành phong cách anime" \
  -F "imageFile=@input_image.jpg" \
  -F "strength=0.8" \
  -F "useAutoParams=true"
```

## 🔧 Cấu hình nâng cao

### Thay đổi model AI
Chỉnh sửa file `gen/gen_cpu.py`:
```python
model_id = "runwayml/stable-diffusion-v1-5"  # Thay đổi model ở đây
```

### Thay đổi API endpoint
Chỉnh sửa trong `frontend/script.js`:
```javascript
const API_BASE_URL = 'http://your-server:port/api';
```

### Tối ưu hiệu suất
- Tăng/giảm `num_cores` trong `gen/gen_cpu.py`
- Điều chỉnh `low_cpu_mem_usage` và `attention_slicing`
- Thay đổi kích thước ảnh output (mặc định 512x512)

## 🐛 Xử lý lỗi

### Lỗi thường gặp:

1. **Backend không khởi động**
   - Kiểm tra Python version (3.8+)
   - Kiểm tra dependencies đã cài đầy đủ
   - Kiểm tra port 5000 có bị chiếm không

2. **Frontend không kết nối được backend**
   - Kiểm tra backend có đang chạy không
   - Kiểm tra URL API trong `script.js`
   - Kiểm tra CORS settings

3. **Out of Memory**
   - Giảm kích thước ảnh input
   - Giảm số steps
   - Tăng swap memory

4. **Model download failed**
   - Kiểm tra kết nối internet
   - Xóa cache: `rm -rf ~/.cache/huggingface`

## 📱 Responsive Design

Frontend hỗ trợ đầy đủ responsive:
- **Desktop**: > 1024px (2 cột layout)
- **Tablet**: 768px - 1024px (1 cột)
- **Mobile**: < 768px (1 cột, tối ưu touch)

## 🔒 Bảo mật

- **File validation**: Kiểm tra type và size
- **Input sanitization**: Làm sạch input
- **CORS**: Chỉ cho phép domain được phép
- **HTTPS**: Khuyến nghị sử dụng HTTPS cho production

## 📈 Performance Tips

1. **Backend**:
   - Sử dụng GPU nếu có thể
   - Tối ưu model loading
   - Cache model weights

2. **Frontend**:
   - Nén ảnh trước khi upload
   - Sử dụng CDN cho static assets
   - Minify CSS/JS cho production

## 🚀 Deployment

### Backend (Production)
```bash
# Sử dụng Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app

# Hoặc sử dụng uWSGI
pip install uwsgi
uwsgi --http :5000 --module backend.app:app
```

### Frontend (Production)
```bash
# Build và deploy static files
# Có thể deploy lên:
# - GitHub Pages
# - Netlify
# - Vercel
# - AWS S3
# - Nginx
```

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📄 License

MIT License - xem file LICENSE để biết thêm chi tiết.

## 🆘 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra logs trong terminal
2. Xem phần "Xử lý lỗi" ở trên
3. Tạo issue trên GitHub với thông tin chi tiết
4. Kiểm tra documentation của từng component

## 🔗 Links

- **Backend API**: http://localhost:5000/api
- **Frontend Web**: http://localhost:8000
- **Health Check**: http://localhost:5000/api/health
- **Test Endpoint**: http://localhost:5000/api/test 