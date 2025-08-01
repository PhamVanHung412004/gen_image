import torch
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import os

class Img2ImgGenerator:
    def __init__(self):
        self.pipe = self.setup_pipeline()
    
    def setup_pipeline(self):
        model_id = "runwayml/stable-diffusion-v1-5"
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch.float16,
            use_safetensors=True
        )
        
        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
            print("Using GPU")
        else:
            print("Using CPU")
        
        return pipe
    
    def generate(self, input_image_path, prompt, output_path="result.png", 
                strength=0.7, steps=20, guidance=7.5):
        
        # Kiểm tra file tồn tại
        if not os.path.exists(input_image_path):
            raise FileNotFoundError(f"Input image not found: {input_image_path}")
        
        # Load ảnh
        print(f"Loading image: {input_image_path}")
        init_image = Image.open(input_image_path).convert("RGB")
        
        # Resize giữ tỷ lệ
        init_image = self.resize_image(init_image, 512, 512)
        
        # Generate
        print(f"Generating with prompt: {prompt}")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        with torch.autocast(device):
            result = self.pipe(
                prompt=prompt,
                image=init_image,
                strength=strength,
                num_inference_steps=steps,
                guidance_scale=guidance,
                height=512,
                width=512
            ).images[0]
        
        # Save
        result.save(output_path)
        print(f"Saved result: {output_path}")
        return result
    
    def resize_image(self, image, target_width, target_height):
        # Resize giữ tỷ lệ và crop center
        w, h = image.size
        ratio = min(target_width/w, target_height/h)
        new_w, new_h = int(w*ratio), int(h*ratio)
        
        image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Crop center nếu cần
        left = (new_w - target_width) // 2
        top = (new_h - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        
        if left < 0 or top < 0:
            # Pad nếu ảnh nhỏ hơn target
            new_image = Image.new('RGB', (target_width, target_height), (255, 255, 255))
            paste_x = (target_width - new_w) // 2
            paste_y = (target_height - new_h) // 2
            new_image.paste(image, (paste_x, paste_y))
            return new_image
        else:
            return image.crop((left, top, right, bottom))

# Sử dụng
generator = Img2ImgGenerator()

# Ví dụ sử dụng
# examples = [
#     {
#         "input": "portrait.jpg",
#         "prompt": "convert to anime style, beautiful anime girl, detailed",
#         "output": "anime_result.png",
#         "strength": 0.8
#     },
    # {
    #     "input": "landscape.jpg", 
    #     "prompt": "cyberpunk city, neon lights, futuristic, detailed",
    #     "output": "cyberpunk_result.png",
    #     "strength": 0.6
    # },
    # {
    #     "input": "person.jpg",
    #     "prompt": "oil painting style, renaissance art, masterpiece",
    #     "output": "painting_result.png", 
    #     "strength": 0.7
    # }
# ]
image = generator.generate(
    input_image_path="image.png",
    prompt="Bạn hãy chuyển cho tôi thành thanh kiếm Nhật",
    output_path="a.png",
    strength=0.8
)
image.show()