# 🎨 AI Image Generator

Ứng dụng tạo ảnh AI sử dụng Stable Diffusion img2img với AI Prompt Engineering từ Gemini.

## 🌟 Tính năng

- **AI Prompt Engineering**: Tự động tạo prompt tối ưu từ yêu cầu tiếng Việt
- **Image-to-Image**: Chuyển đổi ảnh với Stable Diffusion
- **Giao diện Web**: Gradio interface đẹp mắt và dễ sử dụng
- **Giao diện CLI**: Script command line cho local development
- **Chạy trên CPU**: Tối ưu hóa cho môi trường không có GPU

## 🚀 Quick Start

### Option 1: Hugging Face Spaces (Recommended)
1. Xem [README_HF.md](README_HF.md) để deploy lên Hugging Face
2. Hoặc truy cập trực tiếp Space đã deploy

### Option 2: Local Development
1. Clone repository:
```bash
git clone <repository-url>
cd gen_image
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Cấu hình environment variables:
```bash
cp .env.example .env
# Chỉnh sửa .env với GEMINI_API_KEY của bạn
```

4. Test ứng dụng:
```bash
python test_app.py
```

5. Chạy ứng dụng:
```bash
# Web interface
python app.py

# CLI interface
python main.py
```

## 📋 Cấu trúc Project

```
gen_image/
├── app.py                 # Gradio web interface
├── main.py               # CLI script
├── test_app.py           # Test script
├── requirements.txt      # Python dependencies
├── gen/                  # Core modules
│   ├── __init__.py      # Module exports
│   ├── gen_cpu.py       # Stable Diffusion CPU implementation
│   └── gen_prompt.py    # Gemini AI prompt engineering
├── image/               # Thư mục ảnh
├── README.md           # Documentation chính
├── README_HF.md        # Hugging Face deployment guide
└── .gitignore          # Git ignore rules
```

## 🎯 Cách sử dụng

### Web Interface (app.py)
1. Upload ảnh đầu vào
2. Nhập yêu cầu bằng tiếng Việt
3. Tùy chỉnh thông số (tùy chọn)
4. Nhấn "Tạo Ảnh"

### CLI Interface (main.py)
1. Đặt ảnh trong thư mục `image/`
2. Chạy `python main.py`
3. Nhập yêu cầu
4. Chờ kết quả

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

1. **"Model not found"**: Đảm bảo internet connection
2. **"API key error"**: Kiểm tra GEMINI_API_KEY
3. **"Memory error"**: Giảm image size hoặc steps
4. **"Import error"**: Chạy `python test_app.py` để debug

### Logs:
- Web interface: Kiểm tra console output
- CLI: Kiểm tra terminal output
- Hugging Face: Kiểm tra Space logs

## 📝 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 🤝 Contributing

1. Fork project
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📞 Support

Nếu gặp vấn đề:
- Tạo issue trên GitHub
- Kiểm tra [README_HF.md](README_HF.md) cho Hugging Face deployment
- Chạy `python test_app.py` để debug locally

---

**Made with ❤️ using Stable Diffusion + Gemini AI** 