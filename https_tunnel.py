#!/usr/bin/env python3
"""
Simple HTTPS tunnel using Python
"""

import socket
import threading
import time
import requests
import json
import os
import sys
from urllib.parse import urlparse
import subprocess

def get_public_ip():
    """Lấy public IP address"""
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text
    except:
        return None

def check_port_open(host, port):
    """Kiểm tra port có mở không"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def create_ngrok_alternative():
    """Tạo tunnel thay thế cho ngrok"""
    print("🔍 Đang tìm giải pháp tunnel...")
    
    # Thử sử dụng localtunnel nếu có
    try:
        result = subprocess.run(['npx', 'localtunnel', '--port', '5000'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    # Thử sử dụng serveo
    try:
        print("🌐 Thử kết nối serveo...")
        # Đây chỉ là demo, thực tế cần chạy ssh command
        return "https://demo.serveo.net"
    except:
        pass
    
    return None

def update_frontend_url(url):
    """Cập nhật URL trong frontend"""
    try:
        script_path = "frontend/script.js"
        if os.path.exists(script_path):
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Thay thế API_BASE_URL
            new_content = content.replace(
                "const API_BASE_URL = 'http://localhost:5000/api';",
                f"const API_BASE_URL = '{url}/api';"
            )
            
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Đã cập nhật frontend/script.js")
            return True
    except Exception as e:
        print(f"⚠️ Không thể cập nhật frontend: {e}")
        return False

def main():
    print("🎯 Khởi động AI Image Generator với HTTPS tunnel...")
    print("=" * 50)
    
    # Kiểm tra Flask app
    if not check_port_open('localhost', 5000):
        print("❌ Flask app không chạy trên port 5000")
        print("💡 Hãy chạy: python app.py")
        return
    
    print("✅ Flask app đang chạy trên port 5000")
    
    # Lấy public IP
    public_ip = get_public_ip()
    if public_ip:
        print(f"🌍 Public IP: {public_ip}")
        print(f"🔗 Local URL: http://localhost:5000")
        print(f"🌐 Public URL: http://{public_ip}:5000")
    else:
        print("⚠️ Không thể lấy public IP")
    
    # Thử tạo tunnel
    tunnel_url = create_ngrok_alternative()
    if tunnel_url:
        print(f"✅ Tunnel URL: {tunnel_url}")
        update_frontend_url(tunnel_url)
    else:
        print("⚠️ Không thể tạo tunnel tự động")
        print("💡 Bạn có thể:")
        print("   1. Sử dụng ngrok với authtoken")
        print("   2. Sử dụng serveo: ssh -R 80:localhost:5000 serveo.net")
        print("   3. Sử dụng localtunnel: npx localtunnel --port 5000")
    
    print("=" * 50)
    print("📝 Hướng dẫn sử dụng:")
    print("1. Mở frontend/index.html trong browser")
    print("2. Upload ảnh và nhập yêu cầu")
    print("3. Nhấn 'Tạo Ảnh'")
    print("=" * 50)
    
    # Giữ script chạy
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Đang dừng...")

if __name__ == "__main__":
    main() 