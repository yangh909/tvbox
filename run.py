import requests
import json
import os
os.makedirs("dist", exist_ok=True)

# ============= 可自己修改 =============


TV_SOURCES = [
    {"name": "饭太硬", "url": "http://www.饭太硬.cc/tv"},
    {"name": "肥猫", "url": "http://肥猫.live"},
    {"name": "游魂", "url": "https://www.iyouhun.com/tv/0"},
    {"name": "欧歌", "url": "https://m.nxog.top/nxog/ou1.php?url=http://tv.nxog.top&b=欧歌"},
    {"name": "俊哥", "url": "http://home.jundie.top:81/top98.json"}
]

LIVE_SOURCES = [
    {"name": "📺 直播源", "url": "https://ghfast.top/https://raw.githubusercontent.com/yangh909/iptv-api/master/output/result.txt"}
]
# ======================================

final = LIVE_SOURCES + TV_SOURCES

output = {"urls": final}

with open("dist/db.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("生成完成")
