import torch
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import os

num_cores = os.cpu_count()
torch.set_num_threads(num_cores)
torch.set_num_interop_threads(num_cores)

class Img2ImgGenerator:
    def __init__(self):
        self.pipe = self.setup_pipeline()
    
    def setup_pipeline(self):
        model_id = "runwayml/stable-diffusion-v1-5"
        
        # Force CPU usage and appropriate dtype
        if torch.cuda.is_available():
            print("GPU available but forcing CPU usage")
        
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float32,  # Use float32 for CPU
            use_safetensors=True,
            device_map=None,  # Prevent automatic device mapping
            low_cpu_mem_usage=True  # Optimize memory usage
        )
        
        # Explicitly move to CPU
        pipe = pipe.to("cpu")
        print("Using CPU with float32 precision")
        
        # Disable safety checker to save memory (optional)
        pipe.safety_checker = None
        pipe.requires_safety_checker = False
        
        # Enable CPU optimizations
        pipe.enable_attention_slicing()
        
        return pipe
    
    def generate(self, input_image_path, prompt, output_path="result.png",
                 strength=0.7, steps=40, guidance=7.5):
        
        # Check if file exists
        if not os.path.exists(input_image_path):
            raise FileNotFoundError(f"Input image not found: {input_image_path}")
        
        # Load image
        print(f"Loading image: {input_image_path}")
        init_image = Image.open(input_image_path).convert("RGB")
        
        # Resize keeping aspect ratio
        init_image = self.resize_image(init_image, 512, 512)
        
        # Generate without autocast for CPU
        print(f"Generating with prompt: {prompt}")
        print("Note: CPU generation will be slower than GPU")
        
        # CPU generation without autocast
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
        # Resize keeping aspect ratio and crop center
        w, h = image.size
        ratio = min(target_width/w, target_height/h)
        new_w, new_h = int(w*ratio), int(h*ratio)
        
        image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Crop center if needed
        left = (new_w - target_width) // 2
        top = (new_h - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        
        if left < 0 or top < 0:
            # Pad if image is smaller than target
            new_image = Image.new('RGB', (target_width, target_height), (255, 255, 255))
            paste_x = (target_width - new_w) // 2
            paste_y = (target_height - new_h) // 2
            new_image.paste(image, (paste_x, paste_y))
            return new_image
        else:
            return image.crop((left, top, right, bottom))