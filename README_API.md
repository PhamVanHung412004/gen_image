# 🎨 AI Image Generator API

Ứng dụng web để chuyển đổi ảnh sử dụng AI với Stable Diffusion và Gemini AI.

## 🚀 Tính năng

- **Chuyển đổi ảnh với AI**: Sử dụng Stable Diffusion img2img
- **Tự động tối ưu prompt**: Sử dụng Gemini AI để tạo prompt tối ưu
- **Giao diện web đẹp mắt**: Frontend responsive với thiết kế hiện đại
- **API RESTful**: Có thể tích hợp với các ứng dụng khác
- **Xử lý ảnh thông minh**: Tự động resize và tối ưu ảnh đầu vào

## 📋 Yêu cầu hệ thống

- Python 3.8+
- RAM: Tối thiểu 8GB (khuyến nghị 16GB+)
- CPU: Đa nhân (khuyến nghị 4+ cores)
- Dung lượng ổ cứng: 5GB+ cho model

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
gen_image_cpu\Scripts\activate  # Windows
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

### Khởi động server
```bash
python api_server.py
```

### Truy cập ứng dụng
- **Giao diện web**: http://localhost:5000
- **Health check**: http://localhost:5000/health

## 📖 API Endpoints

### 1. GET `/`
- **Mô tả**: Trang chủ với giao diện web
- **Response**: HTML page

### 2. POST `/generate`
- **Mô tả**: Tạo ảnh từ ảnh đầu vào và prompt
- **Content-Type**: `multipart/form-data`

#### Parameters:
- `userRequest` (string): Mô tả yêu cầu chuyển đổi ảnh
- `imageFile` (file): File ảnh đầu vào
- `strength` (float, optional): Độ mạnh chuyển đổi (0.1-1.0, default: 0.8)
- `steps` (int, optional): Số bước inference (10-50, default: 35)
- `guidance` (float, optional): Guidance scale (1-20, default: 7)
- `useAutoParams` (boolean, optional): Tự động tối ưu thông số (default: true)

#### Response:
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

### 3. GET `/health`
- **Mô tả**: Kiểm tra trạng thái server
- **Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "service": "AI Image Generator API"
}
```

## 🎯 Cách sử dụng

### 1. Qua giao diện web
1. Truy cập http://localhost:5000
2. Nhập mô tả yêu cầu chuyển đổi ảnh
3. Chọn file ảnh đầu vào
4. Điều chỉnh thông số (tùy chọn)
5. Nhấn "Tạo Ảnh"
6. Chờ xử lý và tải xuống kết quả

### 2. Qua API
```bash
curl -X POST http://localhost:5000/generate \
  -F "userRequest=Chuyển ảnh này thành phong cách anime" \
  -F "imageFile=@input_image.jpg" \
  -F "strength=0.8" \
  -F "useAutoParams=true"
```

## 🔧 Cấu hình nâng cao

### Thay đổi model
Chỉnh sửa file `gen/gen_cpu.py`:
```python
model_id = "runwayml/stable-diffusion-v1-5"  # Thay đổi model ở đây
```

### Tối ưu hiệu suất
- Tăng/giảm `num_cores` trong `gen/gen_cpu.py`
- Điều chỉnh `low_cpu_mem_usage` và `attention_slicing`
- Thay đổi kích thước ảnh output (mặc định 512x512)

## 🐛 Xử lý lỗi

### Lỗi thường gặp:

1. **Out of Memory**
   - Giảm kích thước ảnh input
   - Giảm số steps
   - Tăng swap memory

2. **Model download failed**
   - Kiểm tra kết nối internet
   - Xóa cache: `rm -rf ~/.cache/huggingface`

3. **API key error**
   - Kiểm tra file `.env`
   - Đảm bảo API key hợp lệ

## 📁 Cấu trúc thư mục

```
gen_image/
├── api_server.py          # Server chính
├── requirements_api.txt   # Dependencies
├── gen/                   # Core modules
│   ├── gen_cpu.py        # Image generator
│   └── gen_prompt.py     # Prompt generator
├── temp_images/          # Temporary files
└── image/               # Sample images
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

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra logs trong terminal
2. Xem phần "Xử lý lỗi" ở trên
3. Tạo issue trên GitHub với thông tin chi tiết 