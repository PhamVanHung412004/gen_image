from gen import (
    Img2ImgGenerator,
    Answer_Question_From_Documents
)

from typing import (
    List,
    Dict
)

import json

def convert_dict(text : str) -> str:
    list_array : List[str] = text.split("\n")
    return '\n'.join(list_array[1 : len(list_array) - 1])


def main() -> None:
    # Lấy yêu cầu từ người dùng
    user_request : str = input("Bạn hãy nhập vào yêu cầu của bạn: ")
    
    # Tạo prompt từ yêu cầu
    prompt_data : str = Answer_Question_From_Documents(user_request).run
    prompt_data = prompt_data.replace("```json","")
    prompt_data = prompt_data.replace("```","")
    prompt_data = json.loads(prompt_data)
    
    print("Generated prompt data:")
    print(json.dumps(prompt_data, indent=2, ensure_ascii=False))
    
    # Khởi tạo generator
    generator = Img2ImgGenerator()
    
    # Tạo ảnh với các thông số từ prompt
    try:
        image = generator.generate(
            input_image_path="image/image.png",
            prompt=prompt_data["prompt"],
            output_path="image/generated_image.png",
            strength=0.8,
            steps=prompt_data["parameters"]["steps"],
            guidance=prompt_data["parameters"]["cfg_scale"]
        )
        
        print("✅ Ảnh đã được tạo thành công!")
        print(f"📁 Lưu tại: image/generated_image.png")
        
        # Hiển thị ảnh nếu có thể
        try:
            image.show()
        except:
            print("⚠️ Không thể hiển thị ảnh tự động. Vui lòng mở file image/generated_image.png")
            
    except Exception as e:
        print(f"❌ Lỗi khi tạo ảnh: {str(e)}")
        print("🔧 Thử với thông số mặc định...")
        
        # Fallback với thông số mặc định
        try:
            image = generator.generate(
                input_image_path="image/image.png",
                prompt=prompt_data["prompt"],
                output_path="image/generated_image_fallback.png",
                strength=0.8,
                steps=35,
                guidance=7
            )
            print("✅ Ảnh đã được tạo với thông số mặc định!")
            print(f"📁 Lưu tại: image/generated_image_fallback.png")
        except Exception as e2:
            print(f"❌ Lỗi nghiêm trọng: {str(e2)}")



if __name__ == "__main__":
    main()