# 🎨 AI Image Generator

Ứng dụng tạo ảnh AI sử dụng Stable Diffusion và Gemini AI để tối ưu hóa prompt.

## ✨ Tính năng

- 🖼️ **Image-to-Image Generation**: Chuyển đổi ảnh với Stable Diffusion
- 🤖 **AI Prompt Engineering**: Tự động tạo prompt tối ưu từ yêu cầu tiếng Việt
- 🎯 **Auto Parameters**: Tự động điều chỉnh thông số cho kết quả tốt nhất
- 📱 **Responsive UI**: Giao diện đẹp, dễ sử dụng
- ⚡ **Fast Processing**: Tối ưu hóa cho CPU

## 🚀 Cách sử dụng

1. **Upload ảnh**: Chọn ảnh đầu vào bạn muốn chuyển đổi
2. **Nhập yêu cầu**: Mô tả bằng tiếng Việt (VD: "Chuyển thành phong cách anime")
3. **Tạo ảnh**: Nhấn nút "Tạo Ảnh" và chờ kết quả
4. **Tải xuống**: Tải ảnh kết quả về máy

## 🔧 Công nghệ

- **Backend**: Flask API
- **Frontend**: HTML, CSS, JavaScript
- **AI Model**: Stable Diffusion Img2Img
- **Prompt AI**: Google Gemini
- **Deployment**: Hugging Face Spaces

## 📁 Cấu trúc dự án

```
├── app.py              # Flask app chính
├── requirements.txt    # Dependencies
├── frontend/          # Frontend files
│   ├── index.html     # Main HTML
│   ├── styles.css     # CSS styles
│   └── script.js      # JavaScript logic
└── gen/              # AI modules
    ├── gen_cpu.py    # Stable Diffusion
    └── gen_prompt.py # Gemini AI
```

## 🌟 Ví dụ sử dụng

- "Chuyển ảnh này thành phong cách anime"
- "Thêm hiệu ứng neon và cyberpunk"
- "Tạo phiên bản hoạt hình Disney"
- "Chuyển thành tranh vẽ bằng sơn dầu"

## 📝 Lưu ý

- Hỗ trợ file: JPG, PNG, GIF (tối đa 10MB)
- Quá trình xử lý có thể mất vài phút
- Kết quả phụ thuộc vào chất lượng ảnh đầu vào và mô tả

---

Made with ❤️ using Stable Diffusion + Gemini AI 