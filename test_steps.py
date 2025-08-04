#!/usr/bin/env python3
"""
Test script để kiểm tra số bước thực tế
"""

import json
from gen import Answer_Question_From_Documents, Img2ImgGenerator
from PIL import Image
import numpy as np

def create_test_image():
    """Tạo ảnh test đơn giản"""
    img_array = np.zeros((512, 512, 3), dtype=np.uint8)
    img_array[:, :] = [128, 128, 128]  # Màu xám
    return Image.fromarray(img_array)

def test_steps():
    """Test số bước thực tế"""
    print("🧪 Bắt đầu test số bước...")
    
    # Tạo prompt test
    test_request = "Chuyển thành phong cách anime"
    
    # Tạo prompt từ AI
    print("🔄 Đang tạo prompt...")
    prompt_data = Answer_Question_From_Documents(test_request).run
    prompt_data = prompt_data.replace("```json", "").replace("```", "").strip()
    prompt_data = json.loads(prompt_data)
    
    print("📝 Prompt được tạo:")
    print(json.dumps(prompt_data, indent=2, ensure_ascii=False))
    
    # Tạo ảnh test
    test_image = create_test_image()
    test_image.save("test_input.png")
    
    # Khởi tạo generator
    generator = Img2ImgGenerator()
    
    # Test với số bước từ AI
    expected_steps = prompt_data["parameters"]["steps"]
    print(f"🎯 Số bước mong đợi: {expected_steps}")
    
    # Tạo ảnh
    result = generator.generate(
        input_image_path="test_input.png",
        prompt=prompt_data["prompt"],
        output_path="test_output.png",
        strength=0.8,
        steps=expected_steps,
        guidance=prompt_data["parameters"]["cfg_scale"]
    )
    
    print("✅ Test hoàn thành!")

if __name__ == "__main__":
    test_steps() 