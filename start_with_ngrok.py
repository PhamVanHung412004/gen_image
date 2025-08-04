#!/usr/bin/env python3
"""
Script để chạy Flask app với ngrok tunnel
"""

import subprocess
import time
import requests
import json
import os
import signal
import sys
from threading import Thread

def run_flask_app():
    """Chạy Flask app"""
    print("🚀 Khởi động Flask app...")
    subprocess.run([sys.executable, "app.py"])

def get_ngrok_url():
    """Lấy URL ngrok từ API"""
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
        data = response.json()
        for tunnel in data['tunnels']:
            if tunnel['proto'] == 'https':
                return tunnel['public_url']
    except:
        pass
    return None

def main():
    print("🎯 Khởi động AI Image Generator với ngrok tunnel...")
    print("=" * 50)
    
    # Khởi động Flask app trong background
    flask_process = subprocess.Popen([sys.executable, "app.py"])
    
    # Đợi Flask app khởi động
    print("⏳ Đợi Flask app khởi động...")
    time.sleep(3)
    
    # Khởi động ngrok tunnel
    print("🌐 Khởi động ngrok tunnel...")
    ngrok_process = subprocess.Popen([
        "ngrok", "http", "5000",
        "--log=stdout"
    ])
    
    # Đợi ngrok khởi động
    print("⏳ Đợi ngrok tunnel khởi động...")
    time.sleep(5)
    
    # Lấy URL ngrok
    ngrok_url = None
    for i in range(10):
        ngrok_url = get_ngrok_url()
        if ngrok_url:
            break
        time.sleep(2)
    
    if ngrok_url:
        print("✅ Ngrok tunnel đã sẵn sàng!")
        print(f"🌐 HTTPS URL: {ngrok_url}")
        print(f"🔗 API Base URL: {ngrok_url}/api")
        print(f"🔍 Ngrok Dashboard: http://localhost:4040")
        print("=" * 50)
        print("📝 Cập nhật frontend/script.js với URL mới:")
        print(f"   const API_BASE_URL = '{ngrok_url}/api';")
        print("=" * 50)
        
        # Cập nhật frontend script.js
        update_frontend_url(ngrok_url)
        
        print("🎉 Ứng dụng đã sẵn sàng!")
        print("💡 Nhấn Ctrl+C để dừng")
        
        try:
            # Giữ script chạy
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Đang dừng ứng dụng...")
    else:
        print("❌ Không thể lấy URL ngrok")
    
    # Dừng các process
    flask_process.terminate()
    ngrok_process.terminate()
    print("✅ Đã dừng tất cả services")

def update_frontend_url(ngrok_url):
    """Cập nhật URL trong frontend script.js"""
    try:
        script_path = "frontend/script.js"
        if os.path.exists(script_path):
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Thay thế API_BASE_URL
            new_content = content.replace(
                "const API_BASE_URL = 'http://localhost:5000/api';",
                f"const API_BASE_URL = '{ngrok_url}/api';"
            )
            
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Đã cập nhật frontend/script.js")
    except Exception as e:
        print(f"⚠️ Không thể cập nhật frontend: {e}")

if __name__ == "__main__":
    main() 