import gradio as gr
import json
import os
from PIL import Image
import io
import base64
import torch
from diffusers import StableDiffusionImg2ImgPipeline
from google import genai
from google.genai.types import GenerateContentConfig
from dotenv import load_dotenv

# Thiết lập CPU threads
num_cores = os.cpu_count()
torch.set_num_threads(num_cores)
torch.set_num_interop_threads(num_cores)

# Load biến môi trường
load_dotenv()

# Khởi tạo Google AI client
client = genai.Client(api_key="AIzaSyAhSbaTFz87GxeS0rc2IFMxhMWKHJMg2YM")

# System prompt cho AI
SYSTEM_PROMPT = """
Bạn là một CHUYÊN GIA TẠO PROMPT cho Stable Diffusion img2img với chuyên môn sâu về AI Art Generation.
Nhiệm vụ của bạn là chuyển đổi yêu cầu đơn giản của người dùng thành prompt chi tiết, tối ưu cho việc tạo ảnh chất lượng cao.

### VAI TRÒ & CHUYÊN MÔN
- **AI Art Expert**: Hiểu sâu về cách Stable Diffusion hoạt động và tạo ảnh
- **Prompt Engineer**: Tạo prompt tối ưu cho chất lượng ảnh tốt nhất
- **Technical Specialist**: Đề xuất parameters phù hợp cho từng loại chuyển đổi

### CẤU TRÚC JSON BẮT BUỘC
Bạn PHẢI trả về đúng cấu trúc JSON này:
{
  "prompt": "",
  "negative_prompt": "",
  "parameters": {
    "steps": 0,
    "cfg_scale": 0,
    "sampler": "",
    "seed": 0
  }
}

### QUY TẮC TẠO PROMPT
1. **prompt**: Tạo mô tả ngắn gọn (dưới 60 từ) về chủ thể, materials, style, lighting, quality tags tối ưu nhất
2. **negative_prompt**: Tự động chọn các từ khóa tiêu cực phù hợp nhất để tránh lỗi
3. **parameters**: Tự động điều chỉnh các thông số tối ưu cho từng loại ảnh

### LƯU Ý QUAN TRỌNG
- Prompt phải ngắn gọn, dưới 60 từ để tránh vượt quá giới hạn token
- Ưu tiên các từ khóa quan trọng nhất
- Tránh mô tả quá chi tiết và dài dòng

### QUY TẮC BẮT BUỘC
1. **LUÔN bắt đầu** với mô tả chính xác về đối tượng cần chuyển đổi
2. **Thêm chi tiết** về materials, colors, textures cụ thể
3. **Chỉ định style** phù hợp (realistic, artistic, game asset, anime, etc.)
4. **Kết thúc** với quality tags: "highly detailed, 4K, 8K, masterpiece"
5. **Tránh từ ngữ mơ hồ**, abstract concepts
6. **KHÔNG dùng** từ "like", "similar to", "convert to"
7. **Sử dụng tiếng Anh** technical terms cho prompt
8. **Luôn trả lời bằng tiếng Việt** ngoài phần JSON

### CHÚ Ý QUAN TRỌNG
1. Chỉ hiển thị JSON object, không có text nào khác
2. Đảm bảo JSON hợp lệ và đúng cú pháp
3. Không thêm markdown formatting (```json)
""".strip()

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

class PromptGenerator:
    def __init__(self):
        pass
    
    def generate_prompt(self, user_request):
        prompt = f"""      
        Câu yêu cầu của người dùng:
        {user_request}
        Trả lời:"""
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=GenerateContentConfig(
                system_instruction=[SYSTEM_PROMPT]
            )
        )
        return response.text

# Khởi tạo generators toàn cục - chỉ load 1 lần
generator = None
prompt_generator = None

def initialize_generators():
    """Khởi tạo tất cả generators khi app khởi động - chỉ load 1 lần"""
    global generator, prompt_generator
    try:
        print("🔄 Đang khởi tạo Stable Diffusion model...")
        generator = Img2ImgGenerator()
        print("✅ Đã load Stable Diffusion model thành công!")
        
        print("🔄 Đang khởi tạo Prompt Generator...")
        prompt_generator = PromptGenerator()
        print("✅ Đã khởi tạo Prompt Generator thành công!")
        
        return "✅ Đã khởi tạo thành công tất cả models! Sẵn sàng tạo ảnh."
    except Exception as e:
        return f"❌ Lỗi khởi tạo models: {str(e)}"

def process_image_generation(input_image, user_request):
    """Xử lý tạo ảnh từ input - sử dụng models đã load sẵn"""
    global generator, prompt_generator
    
    try:
        # Kiểm tra models đã được khởi tạo
        if generator is None or prompt_generator is None:
            return None, "❌ Models chưa được khởi tạo! Vui lòng đợi hoặc refresh trang."
        
        # Kiểm tra input
        if input_image is None:
            return None, "❌ Vui lòng upload ảnh đầu vào!"
        
        if not user_request or user_request.strip() == "":
            return None, "❌ Vui lòng nhập yêu cầu của bạn!"
        
        # Tạo prompt từ yêu cầu - sử dụng prompt_generator đã load sẵn
        print("🔄 Đang tạo prompt từ yêu cầu...")
        prompt_data = prompt_generator.generate_prompt(user_request)
        
        # Xử lý JSON response
        prompt_data = prompt_data.replace("```json", "").replace("```", "").strip()
        prompt_data = json.loads(prompt_data)
        
        print("📝 Prompt được tạo:")
        print(json.dumps(prompt_data, indent=2, ensure_ascii=False))
        
        # Lưu ảnh input tạm thời
        temp_input_path = "temp_input.png"
        input_image.save(temp_input_path)
        
        # Tạo ảnh với các thông số từ AI - sử dụng generator đã load sẵn
        print("🎨 Đang tạo ảnh...")
        print(f"🔧 Thông số được sử dụng:")
        print(f"   - Steps: {prompt_data['parameters']['steps']}")
        print(f"   - Guidance: {prompt_data['parameters']['cfg_scale']}")
        print(f"   - Strength: 0.8")
        
        result_image = generator.generate(
            input_image_path=temp_input_path,
            prompt=prompt_data["prompt"],
            output_path="temp_output.png",
            strength=0.8,  # Giá trị mặc định
            steps=prompt_data["parameters"]["steps"],
            guidance=prompt_data["parameters"]["cfg_scale"]
        )
        
        # Xóa file tạm
        if os.path.exists(temp_input_path):
            os.remove(temp_input_path)
        
        # Tạo thông tin kết quả
        result_info = f"""
        ✅ **Ảnh đã được tạo thành công!**
        
        📝 **Prompt được sử dụng:**
        {prompt_data['prompt']}
        
        🔧 **Thông số:**
        - Strength: 0.8 (mặc định)
        - Steps: {prompt_data['parameters']['steps']}
        - Guidance: {prompt_data['parameters']['cfg_scale']}
        
        🎯 **Negative Prompt:**
        {prompt_data.get('negative_prompt', 'Không có')}
        
        💡 **Lưu ý:** Số bước đã được AI tối ưu để tương thích với scheduler
        """
        
        return result_image, result_info
        
    except json.JSONDecodeError as e:
        return None, f"❌ Lỗi xử lý prompt JSON: {str(e)}"
    except Exception as e:
        return None, f"❌ Lỗi khi tạo ảnh: {str(e)}"

def create_interface():
    """Tạo giao diện Gradio"""
    
    # CSS tùy chỉnh
    css = """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main-header {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 20px;
    }
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .status-ready {
        color: #27ae60;
        font-weight: bold;
    }
    .status-loading {
        color: #f39c12;
        font-weight: bold;
    }
    """
    
    with gr.Blocks(css=css, title="AI Image Generator - Stable Diffusion") as interface:
        
        # Header
        gr.HTML("""
        <div class="main-header">
            <h1>🎨 AI Image Generator</h1>
            <p>Chuyển đổi ảnh với Stable Diffusion và AI Prompt Engineering</p>
        </div>
        """)
        
        # Info box
        gr.HTML("""
        <div class="info-box">
            <h3>📋 Hướng dẫn sử dụng:</h3>
            <ul>
                <li>Upload ảnh đầu vào bạn muốn chuyển đổi</li>
                <li>Nhập mô tả yêu cầu bằng tiếng Việt (VD: "Chuyển thành phong cách anime", "Thêm hiệu ứng neon")</li>
                <li>Điều chỉnh các thông số nếu cần (để trống để dùng AI tự động)</li>
                <li>Nhấn "Tạo Ảnh" và chờ kết quả</li>
            </ul>
            <p><strong>💡 Tối ưu:</strong> Models đã được load sẵn để tăng tốc độ xử lý!</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                # Input section
                gr.Markdown("### 📤 Input")
                
                input_image = gr.Image(
                    label="Ảnh đầu vào",
                    type="pil",
                    height=300
                )
                
                user_request = gr.Textbox(
                    label="Yêu cầu của bạn",
                    placeholder="VD: Chuyển thành phong cách anime, thêm hiệu ứng neon, tạo phiên bản cyberpunk...",
                    lines=3
                )
                
                generate_btn = gr.Button(
                    "🎨 Tạo Ảnh",
                    variant="primary",
                    size="lg"
                )
                
                # Status
                status_text = gr.Textbox(
                    label="Trạng thái",
                    value="🔄 Đang khởi tạo models...",
                    interactive=False
                )
            
            with gr.Column(scale=1):
                # Output section
                gr.Markdown("### 📤 Kết quả")
                
                output_image = gr.Image(
                    label="Ảnh kết quả",
                    height=300
                )
                
                output_info = gr.Markdown(
                    label="Thông tin kết quả",
                    value="Kết quả sẽ hiển thị ở đây..."
                )
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; margin-top: 30px; color: #7f8c8d;">
            <p>Powered by Stable Diffusion + Gemini AI | Made with ❤️</p>
        </div>
        """)
        
        # Event handlers
        generate_btn.click(
            fn=process_image_generation,
            inputs=[input_image, user_request],
            outputs=[output_image, output_info]
        )
        
        # Auto-initialize generators khi app khởi động
        interface.load(initialize_generators, outputs=[status_text])
    
    return interface

# Tạo interface
app = create_interface()

# Launch cho Hugging Face Spaces
if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    ) 