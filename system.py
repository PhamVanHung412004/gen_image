# import torch
# import numpy as np
# from transformers import CLIPProcessor, CLIPModel
# from PIL import Image
# import json
# from sklearn.metrics.pairwise import cosine_similarity

# class SwordSearchSystem:
#     def __init__(self):
#         # Load CLIP model
#         self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
#         self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
#         # Database lưu thông tin các thanh kiếm
#         self.swords_db = []
#         self.embeddings = []
        
#     def add_sword_to_db(self, sword_id, image_path, name, description, features=""):
#         """Thêm thanh kiếm vào database"""
#         sword_info = {
#             "id": sword_id,
#             "image_path": image_path,
#             "name": name,
#             "description": description,
#             "features": features
#         }
        
#         # Tạo embedding cho sản phẩm này
#         embedding = self._create_sword_embedding(image_path, name, description, features)
        
#         self.swords_db.append(sword_info)
#         self.embeddings.append(embedding)
        
#     def _create_sword_embedding(self, image_path, name, description, features):
#         """Tạo embedding kết hợp ảnh + text cho 1 thanh kiếm"""
#         # Load và process ảnh
#         image = Image.open(image_path)
#         image_inputs = self.processor(images=image, return_tensors="pt")
        
#         # Tạo text mô tả đầy đủ
#         full_text = f"{name}. {description}. {features}"
#         text_inputs = self.processor(text=[full_text], return_tensors="pt", padding=True)
        
#         # Lấy embeddings
#         with torch.no_grad():
#             image_embedding = self.model.get_image_features(**image_inputs)
#             text_embedding = self.model.get_text_features(**text_inputs)
        
#         # Kết hợp embedding (có thể điều chỉnh trọng số)
#         image_weight = 0.7  # Ưu tiên hình ảnh hơn
#         text_weight = 0.3
        
#         combined_embedding = (image_weight * image_embedding + 
#                             text_weight * text_embedding)
        
#         # Normalize
#         combined_embedding = combined_embedding / combined_embedding.norm(dim=-1, keepdim=True)
        
#         return combined_embedding.numpy()
    
#     def search_similar_swords(self, query_image_path, query_text, top_k=5):
#         """Tìm kiếm thanh kiếm tương tự dựa trên ảnh + text input"""
        
#         # Tạo embedding cho query
#         query_embedding = self._create_sword_embedding(
#             query_image_path, 
#             "", 
#             query_text, 
#             ""
#         )
        
#         # Tính similarity với tất cả sản phẩm trong DB
#         if not self.embeddings:
#             return []
            
#         db_embeddings = np.vstack(self.embeddings)
#         similarities = cosine_similarity(query_embedding, db_embeddings)[0]
        
#         # Lấy top-k kết quả
#         top_indices = np.argsort(similarities)[::-1][:top_k]
        
#         results = []
#         for idx in top_indices:
#             sword = self.swords_db[idx]
#             similarity_score = similarities[idx]
            
#             results.append({
#                 "sword": sword,
#                 "similarity": float(similarity_score),
#                 "confidence": f"{similarity_score*100:.1f}%"
#             })
            
#         return results
    
#     def save_database(self, file_path):
#         """Lưu database ra file"""
#         data = {
#             "swords": self.swords_db,
#             "embeddings": [emb.tolist() for emb in self.embeddings]
#         }
#         with open(file_path, 'w', encoding='utf-8') as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)
    
#     def load_database(self, file_path):
#         """Load database từ file"""
#         with open(file_path, 'r', encoding='utf-8') as f:
#             data = json.load(f)
        
#         self.swords_db = data["swords"]
#         self.embeddings = [np.array(emb) for emb in data["embeddings"]]

# # Ví dụ sử dụng
# if __name__ == "__main__":
#     # Khởi tạo hệ thống
#     sword_search = SwordSearchSystem()
    
#     # Thêm các thanh kiếm vào database
#     sword_search.add_sword_to_db(
#         sword_id="katana_01",
#         image_path="katana_1.jpg",
#         name="Katana Samurai",
#         description="Thanh kiếm Nhật truyền thống",
#         features="Lưỡi cong, cán dài, thép cao cấp"
#     )
    
#     sword_search.add_sword_to_db(
#         sword_id="broadsword_01", 
#         image_path="broadsword_1.jpg",
#         name="Broad Sword",
#         description="Kiếm rộng phong cách châu Âu",
#         features="Lưỡi rộng, hai lưỡi cắt, cán ngắn"
#     )
    
#     # Tìm kiếm
#     results = sword_search.search_similar_swords(
#         query_image_path="user_sword_image.jpg",
#         query_text="Tôi muốn đổi sang thanh kiếm Nhật Bản, kiểu cong, dài",
#         top_k=3
#     )
    
#     # Hiển thị kết quả
#     print("🗡️ Gợi ý thanh kiếm phù hợp:")
#     for i, result in enumerate(results, 1):
#         sword = result["sword"]
#         print(f"\n{i}. {sword['name']}")
#         print(f"   📝 {sword['description']}")
#         print(f"   ⚔️ {sword['features']}")
#         print(f"   🎯 Độ phù hợp: {result['confidence']}")
#         print(f"   🔗 ID: {sword['id']}")