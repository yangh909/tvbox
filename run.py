import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor

os.makedirs("dist", exist_ok=True)

# ===================== 你的直播源 =====================
live_sources = [
    {
        "name": "📺 自用直播源",
        "url": "https://ghfast.top/https://raw.githubusercontent.com/yangh909/iptv-api/master/output/result.txt"
    }
]

# ===================== 读取仓库列表 =====================
fetch_urls = []
try:
    with open("source_list.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("http"):
                fetch_urls.append(line)
except:
    pass

# ===================== 抓取仓库 =====================
all_items = []
url_set = set()
headers = {"User-Agent": "Mozilla/5.0"}

for url in fetch_urls:
    try:
        data = requests.get(url, headers=headers, timeout=10).json()
        items = data.get("urls") or data.get("stores") or data.get("lives") or data
        for item in items:
            name = item.get("name", "").strip()
            u = item.get("url", "").strip()
            if name and u and u not in url_set:
                url_set.add(u)
                all_items.append({"name": name, "url": u})
    except:
        continue

# ===================== 验证仓库 =====================
def check(item):
    try:
        if requests.get(item["url"], timeout=5, headers=headers).status_code == 200:
            return item
    except:
        return None

valid = []
with ThreadPoolExecutor(5) as executor:
    for res in executor.map(check, all_items):
        if res:
            valid.append(res)

# ===================== 生成 2 个文件 =====================
# 1. 仓库文件（点播+直播）
with open("dist/db.json", "w", encoding="utf-8") as f:
    json.dump({"urls": valid, "lives": live_sources}, f, ensure_ascii=False, indent=2)

# 2. 纯直播文件（能显示在直播列表里）
with open("dist/live.json", "w", encoding="utf-8") as f:
    json.dump(live_sources, f, ensure_ascii=False, indent=2)

print(f"✅ 完成！仓库：{len(valid)} 直播：{len(live_sources)}")
