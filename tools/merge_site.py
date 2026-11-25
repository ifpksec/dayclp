import glob
import json
import os
import shutil
import sys

mine, pub, tag = sys.argv[1], sys.argv[2], sys.argv[3]


def copy(rel):
    src = os.path.join(mine, rel)
    if not os.path.exists(src):
        return
    dst = os.path.join(pub, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


for path in glob.glob(os.path.join(mine, "videos", "*")):
    copy(os.path.relpath(path, mine))
for rel in ("index.html", "favicon.svg", ".nojekyll", "data/progress-%s.json" % tag):
    copy(rel)

for old in glob.glob(os.path.join(pub, "live", "%s-*" % tag)):
    os.remove(old)
for path in glob.glob(os.path.join(mine, "live", "%s-*" % tag)):
    copy(os.path.relpath(path, mine))


def load(path):
    try:
        with open(path, encoding="utf8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return []


items = {x["id"]: x for x in load(os.path.join(pub, "data", "videos.json"))}
for x in load(os.path.join(mine, "data", "videos.json")):
    items.setdefault(x["id"], x)
merged = sorted(items.values(), key=lambda x: x.get("ts", ""), reverse=True)
os.makedirs(os.path.join(pub, "data"), exist_ok=True)
with open(os.path.join(pub, "data", "videos.json"), "w", encoding="utf8") as fh:
    json.dump(merged, fh, ensure_ascii=False, indent=1)
print("merged %d videos" % len(merged))
