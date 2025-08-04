#!/usr/bin/env python3
"""
Test script để kiểm tra ứng dụng locally
Chạy: python test_app.py
"""

import os
import sys
from PIL import Image
import numpy as np

# Thêm thư mục hiện tại vào path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_test_image():
    """Tạo ảnh test đơn giản"""
    # Tạo ảnh gradient đơn giản
    img_array = np.zeros((512, 512, 3), dtype=np.uint8)
    
    # Tạo gradient màu
    for i in range(512):
        for j in range(512):
            img_array[i, j] = [
                int(255 * i / 512),  # Red gradient
                int(255 * j / 512),  # Green gradient
                128  # Blue constant
            ]
    
    # Tạo ảnh test
    test_image = Image.fromarray(img_array)
    test_image.save("test_input.png")
    print("✅ Đã tạo ảnh test: test_input.png")
    return test_image

def test_imports():
    """Test import các modules"""
    try:
        from gen import Img2ImgGenerator, Answer_Question_From_Documents
        print("✅ Import modules thành công")
        return True
    except Exception as e:
        print(f"❌ Lỗi import: {e}")
        return False

def test_gradio_import():
    """Test import Gradio"""
    try:
        import gradio as gr
        print(f"✅ Gradio version: {gr.__version__}")
        return True
    except Exception as e:
        print(f"❌ Lỗi import Gradio: {e}")
        return False

def main():
    """Test chính"""
    print("🧪 Bắt đầu test ứng dụng...")
    
    # Test imports
    if not test_imports():
        print("❌ Test imports thất bại")
        return
    
    if not test_gradio_import():
        print("❌ Test Gradio thất bại")
        return
    
    # Tạo ảnh test
    test_image = create_test_image()
    
    print("✅ Tất cả tests đã pass!")
    print("🚀 Bạn có thể chạy: python app.py")
    print("📝 Hoặc deploy lên Hugging Face Spaces")

if __name__ == "__main__":
    main() 