# 🎨 AI Image Generator - Hugging Face Spaces

Ứng dụng tạo ảnh AI sử dụng Stable Diffusion img2img với AI Prompt Engineering từ Gemini.

## 🌟 Tính năng

- **AI Prompt Engineering**: Tự động tạo prompt tối ưu từ yêu cầu tiếng Việt
- **Image-to-Image**: Chuyển đổi ảnh với Stable Diffusion
- **Giao diện Web**: Gradio interface đẹp mắt và dễ sử dụng
- **Tùy chỉnh thông số**: Điều chỉnh strength, steps, guidance scale
- **Chạy trên CPU**: Tối ưu hóa cho môi trường không có GPU

## 🚀 Deployment trên Hugging Face Spaces

### Bước 1: Tạo Space mới
1. Truy cập [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Chọn:
   - **Owner**: Tài khoản của bạn
   - **Space name**: `ai-image-generator` (hoặc tên bạn muốn)
   - **Space SDK**: `Gradio`
   - **Space hardware**: `CPU` (hoặc `T4` nếu có)
   - **License**: Chọn license phù hợp

### Bước 2: Upload code
Upload các file sau vào Space:

```
├── app.py                 # File chính chứa Gradio interface
├── requirements.txt       # Dependencies
├── gen/                   # Thư mục chứa modules
│   ├── __init__.py
│   ├── gen_cpu.py
│   └── gen_prompt.py
└── README.md             # File này
```

### Bước 3: Cấu hình Environment Variables
Trong Settings của Space, thêm:
- `GEMINI_API_KEY`: API key của Google Gemini

### Bước 4: Deploy
Space sẽ tự động build và deploy sau khi upload code.

## 📋 Cấu trúc Project

```
ai-image-generator/
├── app.py                 # Gradio interface chính
├── main.py               # Script CLI (không dùng cho HF)
├── requirements.txt      # Python dependencies
├── gen/                  # Core modules
│   ├── __init__.py      # Module exports
│   ├── gen_cpu.py       # Stable Diffusion CPU implementation
│   └── gen_prompt.py    # Gemini AI prompt engineering
├── image/               # Thư mục ảnh (không cần cho HF)
└── README.md           # Documentation
```

## 🎯 Cách sử dụng

1. **Upload ảnh**: Chọn ảnh đầu vào bạn muốn chuyển đổi
2. **Nhập yêu cầu**: Mô tả bằng tiếng Việt (VD: "Chuyển thành anime", "Thêm hiệu ứng neon")
3. **Tùy chỉnh** (tùy chọn): Điều chỉnh các thông số nếu cần
4. **Tạo ảnh**: Nhấn nút "Tạo Ảnh" và chờ kết quả

## 🔧 Thông số kỹ thuật

- **Model**: Stable Diffusion v1.5 (img2img)
- **AI Prompt**: Google Gemini 2.5 Flash
- **Framework**: Gradio 4.44.0
- **Hardware**: CPU optimized
- **Input**: PIL Image
- **Output**: PIL Image + Metadata

## ⚙️ Environment Variables

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

## 🐛 Troubleshooting

### Lỗi thường gặp:

1. **"Model not found"**: Đảm bảo internet connection để download model
2. **"API key error"**: Kiểm tra GEMINI_API_KEY trong Settings
3. **"Memory error"**: Giảm image size hoặc steps
4. **"Timeout"**: Tăng timeout settings trong Space

### Logs:
- Kiểm tra logs trong Space Settings > Logs
- Gradio logs sẽ hiển thị trong console

## 📝 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 🤝 Contributing

1. Fork project
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📞 Support

Nếu gặp vấn đề, hãy tạo issue trên GitHub hoặc liên hệ qua Hugging Face.

---

**Made with ❤️ using Stable Diffusion + Gemini AI** 