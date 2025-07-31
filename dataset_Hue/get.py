import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin, urlparse
import re
from PIL import Image
import hashlib

class HueTourismImageCrawler:
    def __init__(self, output_dir="hue_tourism_data"):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.output_dir = output_dir
        self.images_dir = os.path.join(output_dir, "images")
        self.data = []
        
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(self.images_dir, exist_ok=True)
    
    def download_image(self, img_url, filename):
        """Tải xuống hình ảnh"""
        try:
            response = self.session.get(img_url, timeout=15)
            response.raise_for_status()
            
            # Kiểm tra kích thước ảnh (chỉ tải ảnh lớn hơn 10KB)
            if len(response.content) < 10240:
                return None
                
            filepath = os.path.join(self.images_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return filepath
        except Exception as e:
            print(f"Lỗi tải ảnh {img_url}: {e}")
            return None
    
    def extract_image_info(self, soup, base_url):
        """Trích xuất thông tin hình ảnh và mô tả"""
        image_data = []
        
        # Tìm tất cả hình ảnh
        images = soup.find_all('img')
        
        for idx, img in enumerate(images):
            try:
                # Lấy URL ảnh
                img_src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                if not img_src:
                    continue
                
                # Chuyển thành URL đầy đủ
                img_url = urljoin(base_url, img_src)
                
                # Bỏ qua ảnh quá nhỏ hoặc icon
                if any(keyword in img_url.lower() for keyword in ['icon', 'logo', 'avatar', 'thumb']):
                    continue
                
                # Lấy thông tin mô tả ảnh
                alt_text = img.get('alt', '')
                title_text = img.get('title', '')
                
                # Tìm caption hoặc mô tả gần ảnh
                caption = self.find_image_caption(img)
                
                # Lấy context xung quanh ảnh
                context = self.get_image_context(img)
                
                # Tạo tên file duy nhất
                img_hash = hashlib.md5(img_url.encode()).hexdigest()[:8]
                file_extension = os.path.splitext(urlparse(img_url).path)[1] or '.jpg'
                filename = f"hue_{idx}_{img_hash}{file_extension}"
                
                # Tải ảnh
                local_path = self.download_image(img_url, filename)
                
                if local_path:
                    image_info = {
                        'filename': filename,
                        'local_path': local_path,
                        'original_url': img_url,
                        'alt_text': alt_text,
                        'title': title_text,
                        'caption': caption,
                        'context': context,
                        'source_url': base_url
                    }
                    image_data.append(image_info)
                    print(f"Đã tải: {filename}")
                
                time.sleep(1)  # Delay giữa các lần tải ảnh
                
            except Exception as e:
                print(f"Lỗi xử lý ảnh {idx}: {e}")
                continue
        
        return image_data
    
    def find_image_caption(self, img_tag):
        """Tìm caption của ảnh"""
        caption = ""
        
        # Tìm trong các thẻ figure/figcaption
        figure = img_tag.find_parent('figure')
        if figure:
            figcaption = figure.find('figcaption')
            if figcaption:
                caption = figcaption.get_text(strip=True)
        
        # Tìm trong div parent có class caption
        parent = img_tag.find_parent(['div', 'span'], class_=re.compile('caption|desc'))
        if parent and not caption:
            caption = parent.get_text(strip=True)
        
        # Tìm trong sibling elements
        if not caption:
            next_sibling = img_tag.find_next_sibling(['p', 'div', 'span'])
            if next_sibling and len(next_sibling.get_text(strip=True)) < 200:
                caption = next_sibling.get_text(strip=True)
        
        return caption
    
    def get_image_context(self, img_tag):
        """Lấy context xung quanh ảnh"""
        context = ""
        
        # Tìm đoạn văn trước và sau ảnh
        prev_p = img_tag.find_previous('p')
        next_p = img_tag.find_next('p')
        
        if prev_p:
            prev_text = prev_p.get_text(strip=True)
            if len(prev_text) < 300:
                context += prev_text + " "
        
        if next_p:
            next_text = next_p.get_text(strip=True)
            if len(next_text) < 300:
                context += next_text
        
        return context.strip()
    
    def crawl_hue_tourism_sites(self):
        """Crawl các trang du lịch về Huế"""
        sites = [
            "https://www.istockphoto.com/vi/b%E1%BB%A9c-%E1%BA%A3nh/hu%E1%BA%BF"
        ]
        
        all_images = []
        
        for site in sites:
            try:
                print(f"\n=== Đang crawl: {site} ===")
                response = self.session.get(site, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Trích xuất thông tin ảnh
                site_images = self.extract_image_info(soup, site)
                all_images.extend(site_images)
                
                print(f"Đã tìm thấy {len(site_images)} ảnh từ {site}")
                
                time.sleep(3)  # Delay giữa các site
                
            except Exception as e:
                print(f"Lỗi khi crawl {site}: {e}")
        
        return all_images
    
    def crawl_google_images(self, keywords):
        """Tìm ảnh từ Google Images (cẩn thận với Terms of Service)"""
        # Lưu ý: Cần tuân thủ Terms of Service của Google
        search_urls = []
        for keyword in keywords:
            url = f"https://www.google.com/search?q={keyword}&tbm=isch"
            search_urls.append(url)
        
        # Thực hiện tìm kiếm thận trọng
        # (Code này chỉ mang tính minh họa)
        pass
    
    def save_metadata(self, images_data):
        """Lưu metadata của tất cả ảnh"""
        metadata_file = os.path.join(self.output_dir, "images_metadata.json")
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(images_data, f, ensure_ascii=False, indent=2)
        
        print(f"Đã lưu metadata vào {metadata_file}")
    
    def create_summary_report(self, images_data):
        """Tạo báo cáo tổng kết"""
        report = {
            'total_images': len(images_data),
            'sources': list(set([img['source_url'] for img in images_data])),
            'images_with_captions': len([img for img in images_data if img['caption']]),
            'images_with_context': len([img for img in images_data if img['context']]),
            'summary': []
        }
        
        # Tạo tóm tắt cho từng ảnh
        for img in images_data:
            summary = {
                'filename': img['filename'],
                'description': img['alt_text'] or img['caption'] or 'Không có mô tả',
                'has_detailed_info': bool(img['caption'] and img['context'])
            }
            report['summary'].append(summary)
        
        # Lưu báo cáo
        report_file = os.path.join(self.output_dir, "crawl_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report
    
    def run(self):
        """Chạy toàn bộ quá trình crawl"""
        print("🚀 Bắt đầu crawl dữ liệu hình ảnh về du lịch Huế...")
        
        # Crawl từ các trang web
        images_data = self.crawl_hue_tourism_sites()
        
        # Lưu metadata
        self.save_metadata(images_data)
        
        # Tạo báo cáo
        report = self.create_summary_report(images_data)
        
        print(f"\n✅ Hoàn thành!")
        print(f"📊 Tổng cộng: {report['total_images']} ảnh")
        print(f"📝 Ảnh có mô tả: {report['images_with_captions']}")
        print(f"📋 Ảnh có context: {report['images_with_context']}")
        print(f"📁 Dữ liệu được lưu tại: {self.output_dir}")

# Sử dụng
if __name__ == "__main__":
    crawler = HueTourismImageCrawler()
    crawler.run()
    
    # # Các keywords để tìm kiếm thêm (nếu cần)
    # hue_keywords = [
    #     "Huế cung đình", "chùa Thiên Mụ", "đại nội Huế", 
    #     "lăng Khải Định", "lăng Tự Đức", "sông Hương",
    #     "chợ Đông Ba", "cầu Trường Tiền"
    # ]