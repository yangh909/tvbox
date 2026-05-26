import requests
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

# 创建输出目录
os.makedirs("dist", exist_ok=True)

# ===================== 【直播源】 =====================
live_sources = [
    {
        "name": "📺 自用直播源",
        "url": "https://ghfast.top/https://raw.githubusercontent.com/yangh909/iptv-api/master/output/result.txt"
    }
]

# ===================== 从文件读取【点播仓库】 =====================
fetch_urls = []
try:
    with open("source_list.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and line.startswith("http"):
                fetch_urls.append(line)
except:
    print("⚠️ 读取 source_list.txt 失败")

# ===================== 配置 =====================
headers = {"User-Agent": "Mozilla/5.0"}
timeout = 10
max_workers = 5
url_set = set()
all_items = []

# ===================== 抓取点播仓库 =====================
for fetch_url in fetch_urls:
    try:
        resp = requests.get(fetch_url, headers=headers, timeout=timeout)
        data = resp.json()

        items = []
        if "urls" in data:
            items = data["urls"]
        elif "stores" in data:
            items = data["stores"]
        elif "lives" in data:
            items = data["lives"]
        elif isinstance(data, list):
            items = data

        for item in items:
            name = item.get("name", "").strip()
            url = item.get("url", "").strip()
            if name and url and url.startswith("http") and url not in url_set:
                url_set.add(url)
                all_items.append({"name": name, "url": url})

        print(f"✅ 抓取成功: {fetch_url}")
    except Exception as e:
        print(f"❌ 抓取失败: {fetch_url}")

# ===================== 验证仓库可用性 =====================
def check(item):
    try:
        res = requests.get(item["url"], headers=headers, timeout=5)
        if res.status_code == 200:
            return item
    except:
        pass
    return None

valid_list = []
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    results = executor.map(check, all_items)
    for res in results:
        if res:
            valid_list.append(res)

# ===================== ✅ 关键：生成 点播+直播 标准格式 =====================
result = {
    "urls": valid_list,    # 👈 点播仓库
    "lives": live_sources  # 👈 直播源
}

# 输出文件
with open("dist/db.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n🎉 生成完成！有效仓库：{len(valid_list)} 个，直播源：{len(live_sources)} 个")
