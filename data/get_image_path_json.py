import json
from pathlib import Path

# (.dataset) zzou@pnikitn:~$ python ~/COMFORT/data/get_image_path_json.py

root = Path("./COMFORT/data/comfort_human_car")

# 只搜索两级子目录下的 .png 文件
# for p in root.glob("*/*/*.png"):
#     if "horse" not in str(p).lower():
#         image_paths.append(str(p))
image_paths = [
    str(p) for p in root.glob("*/*/*.png") if "horse" not in str(p).lower()
]

image_paths.sort()
print(f"Found {len(image_paths)} images")

with open("comfort_image_paths.json", "w", encoding="utf-8") as f:
    json.dump(image_paths, f, indent=2, ensure_ascii=False)

print("Saved: comfort_image_paths.json") # save to ./comfort_image_paths.json