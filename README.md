# 🎨 AI Image Generator Frontend

Frontend cho ứng dụng AI Image Generator với 3 file riêng biệt: HTML, CSS và JavaScript.

## 📁 Cấu trúc file

```
frontend/
├── index.html    # File HTML chính
├── styles.css    # File CSS styles
├── script.js     # File JavaScript logic
└── README.md     # Hướng dẫn này
```

## 🚀 Cách sử dụng

### 1. Khởi động Backend
```bash
cd backend
python app.py
```

### 2. Mở Frontend
Có thể mở file `index.html` trực tiếp trong trình duyệt:
- Double-click vào file `frontend/index.html`
- Hoặc mở file trong trình duyệt
- Hoặc bấm F5 để refresh

## ✨ Tính năng

- ✅ **Chạy trực tiếp**: Không cần local server
- ✅ **Giao diện đẹp**: Thiết kế hiện đại với gradient
- ✅ **Drag & Drop**: Kéo thả file ảnh
- ✅ **Preview**: Xem trước ảnh đã chọn
- ✅ **Validation**: Kiểm tra file và input
- ✅ **Loading states**: Hiển thị trạng thái xử lý
- ✅ **Error handling**: Xử lý lỗi thân thiện
- ✅ **Responsive**: Hoạt động tốt trên mọi thiết bị

## 🎯 Cách sử dụng

1. **Nhập mô tả**: Viết yêu cầu chuyển đổi ảnh
2. **Chọn ảnh**: Click hoặc kéo thả file ảnh
3. **Tạo ảnh**: Nhấn nút "Tạo Ảnh"
4. **Tải xuống**: Tải ảnh kết quả

## ⌨️ Phím tắt

- **Ctrl/Cmd + Enter**: Gửi form
- **F5**: Refresh trang

## 🔧 Tùy chỉnh

### Thay đổi API endpoint
Chỉnh sửa trong file `script.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

### Thay đổi màu sắc
Chỉnh sửa trong file `styles.css`:
```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

## 🐛 Xử lý lỗi

### Lỗi thường gặp:

1. **Không kết nối được backend**
   - Kiểm tra backend có đang chạy không
   - Kiểm tra URL API trong `script.js`

2. **File không upload được**
   - Kiểm tra kích thước file (< 10MB)
   - Kiểm tra định dạng file (JPG, PNG, GIF)

## 📱 Responsive Design

- **Desktop**: Layout đầy đủ
- **Tablet**: Tối ưu cho màn hình vừa
- **Mobile**: Layout đơn cột, tối ưu touch

## 📄 License

MIT License 