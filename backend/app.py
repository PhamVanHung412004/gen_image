from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gen import Img2ImgGenerator, Answer_Question_From_Documents
import json
import os
import base64
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Khởi tạo generator
generator = Img2ImgGenerator()

# Tạo thư mục để lưu ảnh tạm thời
UPLOAD_FOLDER = '../temp_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/api/generate', methods=['POST'])
def generate_image():
    """API endpoint để tạo ảnh"""
    try:
        # Lấy dữ liệu từ request
        user_request = request.form.get('userRequest')
        use_auto_params = request.form.get('useAutoParams', 'true').lower() == 'true'
        
        # Lấy file ảnh
        if 'imageFile' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['imageFile']
        if file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        # Lưu file tạm thời
        temp_filename = f"{uuid.uuid4()}_{file.filename}"
        temp_path = os.path.join(UPLOAD_FOLDER, temp_filename)
        file.save(temp_path)
        
        try:
            # Tạo prompt từ yêu cầu người dùng
            prompt_data = Answer_Question_From_Documents(user_request).run
            prompt_data = prompt_data.replace("```json", "").replace("```", "")
            prompt_data = json.loads(prompt_data)
            
            # Sử dụng thông số từ AI
            strength = 0.8
            steps = prompt_data["parameters"]["steps"]
            guidance = prompt_data["parameters"]["cfg_scale"]
            prompt = prompt_data["prompt"]
            
            # Tạo ảnh
            output_filename = f"generated_{uuid.uuid4()}.png"
            output_path = os.path.join(UPLOAD_FOLDER, output_filename)
            
            image = generator.generate(
                input_image_path=temp_path,
                prompt=prompt,
                output_path=output_path,
                strength=strength,
                steps=steps,
                guidance=guidance
            )
            
            # Chuyển ảnh thành base64 để trả về
            with open(output_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            
            # Xóa file tạm thời
            os.remove(temp_path)
            os.remove(output_path)
            
            return jsonify({
                'success': True,
                'prompt': prompt,
                'parameters': {
                    'steps': steps,
                    'cfg_scale': guidance,
                    'strength': strength
                },
                'image': img_data
            })
            
        except Exception as e:
            # Xóa file tạm thời nếu có lỗi
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
            
    except json.JSONDecodeError as e:
        return jsonify({
            'error': 'Invalid JSON response from AI',
            'message': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'Generation failed',
            'message': str(e)
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'AI Image Generator API'
    })

@app.route('/api/test')
def test_endpoint():
    """Test endpoint"""
    return jsonify({
        'message': 'Backend API is working!',
        'endpoints': {
            'generate': '/api/generate',
            'health': '/api/health',
            'test': '/api/test'
        }
    })

if __name__ == '__main__':
    print("🚀 Khởi động AI Image Generator Backend API...")
    print("📡 API Base URL: http://localhost:5000/api")
    print("🔧 Health Check: http://localhost:5000/api/health")
    print("🧪 Test Endpoint: http://localhost:5000/api/test")
    app.run(host='0.0.0.0', port=5000, debug=True) 