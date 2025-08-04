# 🌐 Hướng dẫn sử dụng ngrok với AI Image Generator

## 📋 Tổng quan

Ngrok giúp tạo HTTPS tunnel để expose local Flask API ra internet, cho phép frontend có thể gọi API từ bất kỳ đâu.

## 🚀 Cách sử dụng

### Phương pháp 1: Sử dụng script tự động

```bash
# Chạy script tự động
./run_ngrok.sh
```

Script này sẽ:
- Khởi động Flask app (nếu chưa chạy)
- Khởi động ngrok tunnel
- Tự động cập nhật URL trong frontend
- Hiển thị thông tin kết nối

### Phương pháp 2: Chạy thủ công

#### Bước 1: Khởi động Flask app
```bash
python app.py
```

#### Bước 2: Mở terminal mới và chạy ngrok
```bash
ngrok http 5000
```

#### Bước 3: Cập nhật frontend
Sau khi ngrok chạy, copy URL HTTPS và cập nhật `frontend/script.js`:
```javascript
const API_BASE_URL = 'https://your-ngrok-url.ngrok.io/api';
```

## 📊 Thông tin kết nối

Khi ngrok chạy thành công, bạn sẽ thấy:

```
✅ Ngrok tunnel đã sẵn sàng!
🌐 HTTPS URL: https://abc123.ngrok.io
🔗 API Base URL: https://abc123.ngrok.io/api
🔍 Ngrok Dashboard: http://localhost:4040
```

## 🔧 Cấu hình ngrok

### Ngrok Dashboard
Truy cập `http://localhost:4040` để xem:
- Traffic logs
- Request details
- Tunnel status

### Các lệnh ngrok hữu ích

```bash
# Xem danh sách tunnels
ngrok list

# Dừng tunnel
ngrok stop

# Chạy với custom domain (cần tài khoản ngrok)
ngrok http 5000 --subdomain=myapp

# Chạy với authentication
ngrok http 5000 --authtoken=your_token
```

## 🌍 Sử dụng với frontend

### Cách 1: Mở file HTML trực tiếp
```bash
# Sau khi có ngrok URL, mở frontend/index.html
# Frontend sẽ tự động gọi API qua HTTPS
```

### Cách 2: Deploy frontend lên hosting
- Upload files trong thư mục `frontend/` lên hosting
- Cập nhật `script.js` với ngrok URL
- Frontend sẽ gọi API qua HTTPS

## 🔒 Bảo mật

### Lưu ý quan trọng:
- Ngrok URL sẽ thay đổi mỗi lần khởi động (trừ khi dùng tài khoản ngrok)
- URL ngrok có thể được truy cập bởi bất kỳ ai
- Chỉ sử dụng cho development/testing

### Tăng cường bảo mật:
```bash
# Chạy với authentication
ngrok http 5000 --authtoken=your_ngrok_token

# Sử dụng custom domain
ngrok http 5000 --subdomain=myapp
```

## 🐛 Xử lý lỗi

### Lỗi "ngrok command not found"
```bash
# Cài đặt ngrok
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

### Lỗi "tunnel not found"
- Đợi thêm vài giây để ngrok khởi động hoàn toàn
- Kiểm tra ngrok dashboard tại `http://localhost:4040`

### Lỗi CORS
- Ngrok tự động xử lý CORS
- Nếu vẫn lỗi, kiểm tra Flask app có CORS enabled

## 📱 Test API

### Test health endpoint
```bash
curl https://your-ngrok-url.ngrok.io/api/health
```

### Test generate endpoint
```bash
curl -X POST https://your-ngrok-url.ngrok.io/api/generate \
  -F "userRequest=Chuyển thành phong cách anime" \
  -F "imageFile=@test.jpg"
```

## 🎯 Lợi ích của ngrok

1. **HTTPS tự động**: Không cần cấu hình SSL
2. **Public access**: Có thể truy cập từ internet
3. **Real-time logs**: Xem traffic qua dashboard
4. **Easy setup**: Chỉ cần 1 lệnh
5. **CORS support**: Tự động xử lý cross-origin

## 💡 Tips

- Lưu ngrok URL để sử dụng lại
- Sử dụng ngrok dashboard để debug
- Restart ngrok nếu gặp lỗi kết nối
- Cân nhắc upgrade tài khoản ngrok để có custom domain

---

**Lưu ý**: Ngrok free plan có giới hạn về số lượng requests và thời gian sử dụng. 