// Configuration
const API_BASE_URL = 'https://43132cc82716.ngrok-free.app/api';
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
let selectedFile = null;
let isProcessing = false;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    checkServerStatus();
});

function setupEventListeners() {
    // Form submission
    document.getElementById('imageForm').addEventListener('submit', handleFormSubmit);
    
    // File input events
    document.getElementById('imageFile').addEventListener('change', handleFileSelect);
    
    // Drag and drop events
    document.getElementById('uploadArea').addEventListener('dragover', handleDragOver);
    document.getElementById('uploadArea').addEventListener('dragleave', handleDragLeave);
    document.getElementById('uploadArea').addEventListener('drop', handleDrop);
    document.getElementById('uploadArea').addEventListener('click', () => document.getElementById('imageFile').click());
    
    // Remove image button
    document.getElementById('removeImage').addEventListener('click', removeSelectedImage);
}

// Server Status Check
async function checkServerStatus() {
    const statusElement = document.getElementById('serverStatus');
    
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            statusElement.className = 'server-status connected';
            statusElement.innerHTML = '✅ Kết nối server thành công';
        } else {
            throw new Error('Server error');
        }
    } catch (error) {
        statusElement.className = 'server-status disconnected';
        statusElement.innerHTML = '❌ Không thể kết nối server. Vui lòng khởi động backend trước.';
    }
}

// File Handling
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        processSelectedFile(file);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    document.getElementById('uploadArea').classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    document.getElementById('uploadArea').classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    document.getElementById('uploadArea').classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        processSelectedFile(files[0]);
    }
}

function processSelectedFile(file) {
    if (!validateFile(file)) {
        return;
    }
    
    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('imagePreview').src = e.target.result;
        document.getElementById('previewContainer').style.display = 'block';
        document.getElementById('uploadArea').style.display = 'none';
    };
    reader.readAsDataURL(file);
}

function validateFile(file) {
    if (!file.type.startsWith('image/')) {
        showError('Vui lòng chọn file ảnh hợp lệ (JPG, PNG, GIF)');
        return false;
    }
    
    if (file.size > MAX_FILE_SIZE) {
        showError('File quá lớn. Vui lòng chọn file nhỏ hơn 10MB');
        return false;
    }
    
    return true;
}

function removeSelectedImage() {
    selectedFile = null;
    document.getElementById('imageFile').value = '';
    document.getElementById('previewContainer').style.display = 'none';
    document.getElementById('uploadArea').style.display = 'flex';
    document.getElementById('imagePreview').src = '';
}

// Form Validation
function isFormValid() {
    if (!document.getElementById('userRequest').value.trim()) {
        showError('Vui lòng nhập mô tả yêu cầu');
        return false;
    }
    
    if (!selectedFile) {
        showError('Vui lòng chọn file ảnh');
        return false;
    }
    
    return true;
}

// Form Submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    if (isProcessing) return;
    
    if (!isFormValid()) {
        return;
    }
    
    isProcessing = true;
    updateGenerateButton(true);
    showLoading();
    
    try {
        const formData = new FormData();
        formData.append('userRequest', document.getElementById('userRequest').value.trim());
        formData.append('imageFile', selectedFile);
        formData.append('useAutoParams', 'true');
        
        const response = await fetch(`${API_BASE_URL}/generate`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showSuccessResult(data);
        } else {
            showError(data.message || 'Có lỗi xảy ra khi tạo ảnh');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError('Không thể kết nối đến server. Vui lòng kiểm tra backend có đang chạy không.');
    } finally {
        isProcessing = false;
        updateGenerateButton(false);
    }
}

// UI Updates
function updateGenerateButton(disabled) {
    const btn = document.getElementById('generateBtn');
    btn.disabled = disabled;
    if (disabled) {
        btn.innerHTML = '<div class="spinner" style="width: 20px; height: 20px; margin: 0;"></div><span>Đang xử lý...</span>';
    } else {
        btn.innerHTML = '🚀 Tạo Ảnh';
    }
}

function showLoading() {
    const result = document.getElementById('result');
    result.style.display = 'block';
    result.className = 'result';
    result.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Đang tạo ảnh, vui lòng chờ...</p>
            <small>Quá trình này có thể mất vài phút</small>
        </div>
    `;
}

function showSuccessResult(data) {
    const result = document.getElementById('result');
    result.style.display = 'block';
    result.className = 'result success';
    result.innerHTML = `
        <h4>✅ Tạo ảnh thành công!</h4>
        <p><strong>Prompt được tạo:</strong> ${data.prompt}</p>
        <p><strong>Thông số:</strong> Steps: ${data.parameters.steps}, Guidance: ${data.parameters.cfg_scale}</p>
        <img src="data:image/png;base64,${data.image}" alt="Generated Image">
        <br>
        <a href="data:image/png;base64,${data.image}" download="generated_image.png" class="download-btn">
            💾 Tải xuống ảnh
        </a>
    `;
    
    // Scroll to results
    result.scrollIntoView({ behavior: 'smooth' });
}

function showError(message) {
    const result = document.getElementById('result');
    result.style.display = 'block';
    result.className = 'result error';
    result.innerHTML = `
        <h4>❌ Lỗi</h4>
        <p>${message}</p>
    `;
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (!isProcessing && isFormValid()) {
            document.getElementById('imageForm').dispatchEvent(new Event('submit'));
        }
    }
}); 