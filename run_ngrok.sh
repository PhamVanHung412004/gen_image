#!/bin/bash

echo "🎯 Khởi động AI Image Generator với ngrok tunnel..."
echo "=================================================="

# Kiểm tra xem Flask app có đang chạy không
if ! pgrep -f "python.*app.py" > /dev/null; then
    echo "🚀 Khởi động Flask app..."
    python app.py &
    FLASK_PID=$!
    sleep 3
else
    echo "✅ Flask app đã đang chạy"
fi

# Khởi động ngrok
echo "🌐 Khởi động ngrok tunnel..."
ngrok http 5000 --log=stdout &
NGROK_PID=$!

# Đợi ngrok khởi động
echo "⏳ Đợi ngrok tunnel khởi động..."
sleep 5

# Lấy URL ngrok
echo "🔍 Lấy URL ngrok..."
for i in {1..10}; do
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | head -1 | cut -d'"' -f4)
    if [ ! -z "$NGROK_URL" ]; then
        break
    fi
    sleep 2
done

if [ ! -z "$NGROK_URL" ]; then
    echo "✅ Ngrok tunnel đã sẵn sàng!"
    echo "🌐 HTTPS URL: $NGROK_URL"
    echo "🔗 API Base URL: $NGROK_URL/api"
    echo "🔍 Ngrok Dashboard: http://localhost:4040"
    echo "=================================================="
    echo "📝 Cập nhật frontend/script.js với URL mới:"
    echo "   const API_BASE_URL = '$NGROK_URL/api';"
    echo "=================================================="
    
    # Cập nhật frontend script.js
    if [ -f "frontend/script.js" ]; then
        sed -i "s|const API_BASE_URL = 'http://localhost:5000/api';|const API_BASE_URL = '$NGROK_URL/api';|g" frontend/script.js
        echo "✅ Đã cập nhật frontend/script.js"
    fi
    
    echo "🎉 Ứng dụng đã sẵn sàng!"
    echo "💡 Nhấn Ctrl+C để dừng"
    
    # Giữ script chạy
    wait
else
    echo "❌ Không thể lấy URL ngrok"
fi

# Dừng các process khi nhận Ctrl+C
trap 'echo -e "\n🛑 Đang dừng ứng dụng..."; kill $FLASK_PID $NGROK_PID 2>/dev/null; exit' INT 