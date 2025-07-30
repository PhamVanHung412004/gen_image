import torch
from diffusers import StableDiffusionInpaintPipeline
from PIL import Image, ImageDraw
import numpy as np
import os
import os

# Tối ưu hóa cho CPU
torch.set_num_threads(os.cpu_count())  # Sử dụng tất cả CPU cores
torch.set_flush_denormal(True)  # Tăng tốc CPU

class SDInpaintingTool:
    def __init__(self, model_id="runwayml/stable-diffusion-inpainting"):
        """Khởi tạo Inpainting Pipeline"""
        print("Đang tải model inpainting...")
        
        self.pipe = StableDiffusionInpaintPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float32,
            safety_checker=None,
            requires_safety_checker=False,
            low_cpu_mem_usage=True
        ).to("cpu")
        
        # Tối ưu cho CPU
        self.pipe.enable_attention_slicing(1)
        print("Model sẵn sàng!")
    
    def make_size_divisible_by_8(self, size):
        """Điều chỉnh kích thước về số chia hết cho 8 gần nhất"""
        width, height = size
        new_width = (width // 8) * 8
        new_height = (height // 8) * 8
        return (new_width, new_height)
    
    def resize_image_and_mask(self, image, mask=None):
        """Resize ảnh và mask về kích thước chia hết cho 8"""
        # Lấy kích thước mới
        new_size = self.make_size_divisible_by_8(image.size)
        
        if new_size != image.size:
            print(f"Điều chỉnh kích thước từ {image.size} sang {new_size}")
            image = image.resize(new_size, Image.LANCZOS)
            
            if mask is not None:
                mask = mask.resize(new_size, Image.LANCZOS)
        
        return image, mask
    
    def create_circle_mask(self, size, center, radius):
        """Tạo mask hình tròn"""
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        
        left = center[0] - radius
        top = center[1] - radius
        right = center[0] + radius
        bottom = center[1] + radius
        
        draw.ellipse([left, top, right, bottom], fill=255)
        return mask
    
    def create_rectangle_mask(self, size, top_left, bottom_right):
        """Tạo mask hình chữ nhật"""
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle([top_left, bottom_right], fill=255)
        return mask
    
    def create_polygon_mask(self, size, points):
        """Tạo mask đa giác từ list các điểm"""
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.polygon(points, fill=255)
        return mask
    
    @torch.no_grad()
    def add_object(
        self,
        image_path,
        mask,
        prompt,
        negative_prompt="",
        strength=1.0,
        guidance_scale=7.5,
        num_inference_steps=30,
        seed=None,
        preserve_original_size=True
    ):
        """
        Thêm đối tượng vào ảnh
        
        Args:
            image_path: Đường dẫn ảnh gốc
            mask: PIL Image mask hoặc path đến file mask
            prompt: Mô tả đối tượng muốn thêm
            negative_prompt: Mô tả những gì không muốn
            strength: Mức độ thay đổi (1.0 = thay đổi hoàn toàn vùng mask)
            guidance_scale: Mức độ tuân theo prompt
            num_inference_steps: Số bước
            seed: Seed cho kết quả nhất quán
            preserve_original_size: Có giữ nguyên kích thước gốc không
        """
        # Load ảnh gốc
        image = Image.open(image_path).convert("RGB")
        original_size = image.size
        
        # Load mask nếu là string path
        if isinstance(mask, str):
            mask = Image.open(mask).convert("L")
        
        # Resize mask cho khớp với ảnh
        mask = mask.resize(image.size, Image.LANCZOS)
        
        # Điều chỉnh kích thước chia hết cho 8
        image, mask = self.resize_image_and_mask(image, mask)
        
        # Set seed
        generator = None
        if seed is not None:
            generator = torch.Generator("cpu").manual_seed(seed)
        
        print(f"Đang thêm: {prompt}")
        print(f"Kích thước xử lý: {image.size}")
        
        # Inpainting
        result = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image=image,
            mask_image=mask,
            strength=strength,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            generator=generator
        )
        
        result_image = result.images[0]
        
        # Resize về kích thước gốc nếu cần
        if preserve_original_size and result_image.size != original_size:
            print(f"Resize về kích thước gốc: {original_size}")
            result_image = result_image.resize(original_size, Image.LANCZOS)
        
        return result_image
    
    def remove_object(
        self,
        image_path,
        mask,
        prompt="clean background, empty space",
        negative_prompt="object, person, thing",
        **kwargs
    ):
        """
        Xóa đối tượng khỏi ảnh (ví dụ: xóa text, watermark)
        """
        return self.add_object(
            image_path=image_path,
            mask=mask,
            prompt=prompt,
            negative_prompt=negative_prompt,
            **kwargs
        )

# Hàm tiện ích để tạo mask cho việc xóa text
def create_text_removal_mask(image_path, text_area):
    """
    Tạo mask cho vùng text cần xóa
    
    Args:
        image_path: Đường dẫn ảnh
        text_area: Tuple (x1, y1, x2, y2) - tọa độ vùng text
    """
    image = Image.open(image_path)
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    
    # Vẽ vùng text với padding
    padding = 5
    x1, y1, x2, y2 = text_area
    draw.rectangle(
        [x1-padding, y1-padding, x2+padding, y2+padding], 
        fill=255
    )
    
    # Làm mờ viền một chút
    from PIL import ImageFilter
    mask = mask.filter(ImageFilter.GaussianBlur(radius=2))
    
    return mask

# Ví dụ sử dụng
if __name__ == "__main__":
    # Khởi tạo tool
    inpaint_tool = SDInpaintingTool()
    
    
    # Ví dụ 2: Thêm đối tượng với auto-resize
    print("\n2. Thêm người vào ảnh:")
    
    # Load ảnh để lấy kích thước
    path_image : str = "/home/phamvanhung/system/test_stable/input.png"
    test_image = Image.open(path_image)
    
    # Tạo mask (tự động điều chỉnh theo kích thước mới)
    person_mask = inpaint_tool.create_rectangle_mask(
        size=test_image.size,
        top_left=(200, 200),
        bottom_right=(350, 450)
    )
    
    result = inpaint_tool.add_object(
        image_path=path_image,
        mask=person_mask,
        prompt="professional woman in business suit standing",
        negative_prompt="deformed, bad anatomy, blurry",
        preserve_original_size=True
    )
    result.save("output.png")