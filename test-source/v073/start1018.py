from pathlib import Path
import json,hashlib,shutil,zipfile,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent; R=P.parents[1]; O=R/'V0.7.3_部分項目補完_2026-10-18';O.mkdir(exist_ok=True)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
files=[R/'九州修仙錄_正式母檔_0.7.2.html',R/'最新定案母檔_0.7.2.json',R/'github-release/index.html',R/'github-release/定案規則_0.7.2.json',R/'V0.7.3_獨立測試_2026-10-17/GitHub測試發布/preview/v0.7.3/index.html']
target=O/'施工前保護檔案雜湊.json'
if not target.exists():target.write_text(json.dumps({str(p.relative_to(R)):sha(p) for p in files},ensure_ascii=False,indent=2),'utf8')
snapshot=O/'施工前0.7.3來源';snapshot.mkdir(exist_ok=True)
for p in P.glob('*.js'):
 if not (snapshot/p.name).exists():shutil.copy2(p,snapshot/p.name)
source=Path('C:/Users/User/.codex/attachments/867e8f79-1c1a-431f-9143-485255a26794/貼上的文字.txt')
shutil.copy2(source,P/'side016-original.txt')
art=R/'素材美術_2026-10-18';art.mkdir(exist_ok=True)
shutil.copy2(Path('C:/Users/User/.codex/generated_images/01a0fe64-95aa-7260-ba13-9d565c3bee39/exec-351e9bfd-d86d-48fb-8c1e-d1ce282164d5.png'),art/'靈草.png')
# Search all Word XML parts, including text in tables, notes and comments.
found=[]
for p in [R/'九州修仙錄_下一輪更新施工規格.docx',Path('C:/Users/User/OneDrive/桌面/九州修仙錄_V0.7.2_下一批大更新_完整施工工作檔_2026-10-17.docx')]:
 with zipfile.ZipFile(p) as z:
  for name in z.namelist():
   if name.startswith('word/') and name.endswith('.xml'):
    t='\n'.join(ET.fromstring(z.read(name)).itertext())
    hits=[s for s in t.splitlines() if any(n in s for n in ['燐火狼','硬黑蠍','靈珠蝶'])]
    if hits:found.append({'file':str(p),'part':name,'hits':hits})
(O/'新寵物原稿交叉查核.json').write_text(json.dumps(found,ensure_ascii=False,indent=2),'utf8')
print('Local supplement folder, source snapshot and protected hashes saved; Word sections searched:',len(found))
