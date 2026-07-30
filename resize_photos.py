import json
import os
from PIL import Image

JSON_PATH = r"C:\Users\a2189\Dropbox\obsidian\40_manuscript\2026ORS\domon.json"
PHOTO_DIR = r"G:\マイドライブ\2026ORS写真"
# 現在のディレクトリ内に resized_photos フォルダを作成します
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "resized_photos")

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

def resize_image(input_path, output_path, max_size=800):
    with Image.open(input_path) as img:
        img.thumbnail((max_size, max_size))
        img.save(output_path, "JPEG", quality=85)

print(f"JSONから写真を検索し、リサイズを開始します...")

# JSONからすべての写真を抽出してリサイズ
processed_count = 0
for day in data.get("schedule", []):
    for photo in day.get("photos", []):
        filename = photo.get("filename")
        if filename:
            orig_path = os.path.join(PHOTO_DIR, filename)
            resized_path = os.path.join(OUTPUT_DIR, filename)
            if os.path.exists(orig_path):
                print(f"-> リサイズ中: {filename}")
                resize_image(orig_path, resized_path)
                processed_count += 1
            else:
                print(f"-> 警告: 元の画像が見つかりません {orig_path}")

print(f"\n合計 {processed_count} 枚の写真をリサイズし、以下に保存しました:")
print(OUTPUT_DIR)
