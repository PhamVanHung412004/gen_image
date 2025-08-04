import os
import sys
import json
import uuid
import base64
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from gen.gen_cpu import Img2ImgGenerator
from gen.gen_prompt import Answer_Question_From_Documents

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'temp_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create temp_images directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the generator
try:
    generator = Img2ImgGenerator()
    print("✅ Img2ImgGenerator initialized successfully")
except Exception as e:
    print(f"❌ Error initializing Img2ImgGenerator: {e}")
    generator = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files from frontend directory"""
    return send_from_directory('frontend', filename)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'generator_ready': generator is not None
    })

@app.route('/api/generate', methods=['POST'])
def generate_image():
    """API endpoint để tạo ảnh"""
    if generator is None:
        return jsonify({'error': 'Generator not initialized'}), 500
    
    try:
        user_request = request.form.get('userRequest')
        
        if 'imageFile' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['imageFile']
        if file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        temp_filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        temp_path = os.path.join(UPLOAD_FOLDER, temp_filename)
        file.save(temp_path)
        
        try:
            # Generate prompt using AI
            prompt_data = Answer_Question_From_Documents(user_request).run
            prompt_data = prompt_data.replace("```json", "").replace("```", "")
            prompt_data = json.loads(prompt_data)
            
            # Use AI-generated parameters
            strength = 0.8
            steps = prompt_data["parameters"]["steps"]
            guidance = prompt_data["parameters"]["cfg_scale"]
            prompt = prompt_data["prompt"]
            
            output_filename = f"generated_{uuid.uuid4()}.png"
            output_path = os.path.join(UPLOAD_FOLDER, output_filename)
            
            # Generate image
            image = generator.generate(
                input_image_path=temp_path,
                prompt=prompt,
                output_path=output_path,
                strength=strength,
                steps=steps,
                guidance=guidance
            )
            
            # Read and encode the generated image
            with open(output_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            
            # Clean up temporary files
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=True)
