#!/bin/bash

echo "🎯 Khởi động AI Image Generator với serveo tunnel..."
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

# Khởi động serveo tunnel
echo "🌐 Khởi động serveo tunnel..."
echo "📝 Lưu ý: serveo sẽ hiển thị URL trong terminal"
echo "⏳ Đang kết nối..."

# Sử dụng ssh để tạo tunnel với serveo
ssh -R 80:localhost:5000 serveo.net &
SERVEO_PID=$!

echo "✅ Serveo tunnel đã khởi động!"
echo "🔍 Kiểm tra terminal để lấy URL"
echo "💡 URL sẽ có dạng: https://your-subdomain.serveo.net"
echo "=================================================="
echo "📝 Cập nhật frontend/script.js với URL mới:"
echo "   const API_BASE_URL = 'https://your-subdomain.serveo.net/api';"
echo "=================================================="

echo "🎉 Ứng dụng đã sẵn sàng!"
echo "💡 Nhấn Ctrl+C để dừng"

# Dừng các process khi nhận Ctrl+C
trap 'echo -e "\n🛑 Đang dừng ứng dụng..."; kill $FLASK_PID $SERVEO_PID 2>/dev/null; exit' INT

# Giữ script chạy
wait 