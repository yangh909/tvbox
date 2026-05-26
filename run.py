import requests
import json
import os
import time

# 创建输出目录
os.makedirs("dist", exist_ok=True)

# ==============================================
# 固定直播源（你自己的）
# ==============================================
live = [
    {"name": "📺 自用直播源", "url": "https://ghfast.top/https://raw.githubusercontent.com/yangh909/iptv-api/master/output/result.txt"}
]

# ==============================================
# 要爬取的远程仓库合集（自动抓取里面的所有仓）
# ==============================================
fetch_urls = [
    "https://iptvindex.com/db.json",
    "https://jihulab.com/z-blog/xh2/-/raw/main/t3.json",
    "https://jihulab.com/duomv/apps/-/raw/main/duo.json",
    "https://jihulab.com/ygbh1/box/-/raw/main/dcang/dc2.json"
]

# ==============================================
# 开始爬取 + 合并 + 去重
# ==============================================
all_items = []
url_set = set()
headers = {"User-Agent": "Mozilla/5.0"}

# 加入直播源
for item in live:
    u = item["url"]
    if u not in url_set:
        url_set.add(u)
        all_items.append(item)

# 爬取所有远程仓库
for fetch_url in fetch_urls:
    try:
        print(f"正在抓取：{fetch_url}")
        resp = requests.get(fetch_url, timeout=10, headers=headers)
        data = resp.json()

        # 自动识别 urls / stores / lives 三种常见格式
        items = []
        if "urls" in data:
            items = data["urls"]
        elif "stores" in data:
            items = data["stores"]
        elif "lives" in data:
            items = data["lives"]

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
# 生成影视仓标准格式
# ==============================================
result = {"urls": valid_list}

with open("dist/db.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n✅ 生成完成！有效仓库总数：{len(valid_list)}")
