import requests
import json
import os
import time

# 创建输出目录
os.makedirs("dist", exist_ok=True)

# ==============================================
# 固定直播源（放最后）
# ==============================================
live = [
    {"name": "📺 自用直播源", "url": "https://ghfast.top/https://raw.githubusercontent.com/yangh909/iptv-api/master/output/result.txt"}
]

# ==============================================
# 从文件读取要爬的地址（自动读，不用改代码）
# ==============================================
fetch_urls = []
try:
    with open("source_list.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and line.startswith("http"):
                fetch_urls.append(line)
except:
    print("读取 source_list.txt 失败")

# ==============================================
# 开始爬取 + 合并 + 去重
# ==============================================
all_items = []
url_set = set()
headers = {"User-Agent": "Mozilla/5.0"}

# 爬取所有远程仓库
for fetch_url in fetch_urls:
    try:
        print(f"正在抓取：{fetch_url}")
        resp = requests.get(fetch_url, timeout=10, headers=headers)
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
            if name and url and url.startswith("http"):
                if url not in url_set:
                    url_set.add(url)
                    all_items.append({"name": name, "url": url})
    except Exception as e:
        print(f"抓取失败：{fetch_url}")

# ==============================================
# 验证地址是否可用
# ==============================================
valid_list = []
timeout = 8

print("\n开始验证地址可用性...")
for item in all_items:
    name = item["name"]
    url = item["url"]
    try:
        res = requests.get(url, timeout=timeout, headers=headers)
        if res.status_code == 200:
            valid_list.append(item)
            print(f"✅ 有效：{name}")
        else:
            print(f"❌ 失效：{name}")
    except:
        print(f"❌ 失效：{name}")
    time.sleep(0.2)

# ==============================================
# 直播源放在最后
# ==============================================
# for item in live:
#     valid_list.append(item)

# ==============================================
# 生成最终影视仓文件
# ==============================================
result = {"urls": valid_list}

with open("dist/db.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n✅ 生成完成！有效仓库总数：{len(valid_list)}")
