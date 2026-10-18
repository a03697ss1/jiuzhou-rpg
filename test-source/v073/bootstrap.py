from pathlib import Path
import re,json,hashlib,base64
ROOT=Path(__file__).resolve().parents[2]
WORK=Path(__file__).resolve().parent
OUT=ROOT/'V0.7.3_獨立測試_2026-10-17'
OUT.mkdir(exist_ok=True)
source=ROOT/'九州修仙錄_測試分支.html'
protected=[source,ROOT/'九州修仙錄_正式母檔_0.7.2.html',ROOT/'最新定案母檔_0.7.2.json',ROOT/'github-release/index.html',ROOT/'github-release/定案規則_0.7.2.json']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
fingerprint={str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in protected}
assert fingerprint[source.name]['sha256']=='58ce74be8922d4d0bc5e702fde0ebc8823649f560f00d12c8d843a5954a3ca50','底稿已變更，需重新核對'
(WORK/'baseline.json').write_text(json.dumps({'version':'0.7.2','testVersion':'0.7.3','commit':'a420a7772dcbb75de52b87c6e2628fa87937495a','protected':fingerprint},ensure_ascii=False,indent=2),'utf8')
text=source.read_text('utf8')
assets=WORK/'assets';assets.mkdir(exist_ok=True)
def externalize(m):
 mime,encoded=m.groups();data=base64.b64decode(encoded);h=hashlib.sha256(data).hexdigest();ext={'jpeg':'jpg','svg+xml':'svg'}.get(mime,mime)
 name='jz070_'+h[:24]+'.'+ext
 if (ROOT/'github-release/assets'/name).exists():return '/github-release/assets/'+name
 path=assets/(h[:24]+'.'+ext)
 if not path.exists():path.write_bytes(data)
 return '/release-tools/v073/assets/'+path.name
small=re.sub(r'data:image/([A-Za-z0-9.+-]+);base64,([A-Za-z0-9+/=]+)',externalize,text)
old="if(!uri)return null;const [head,b64]=uri.split(',')"
new="if(!uri)return null;if(!uri.startsWith('data:'))return Q.portraits[n]=new URL(uri,document.baseURI).href;const [head,b64]=uri.split(',')"
assert small.count(old)==1
small=small.replace(old,new)
(WORK/'baseline-preview.html').write_text(small,'utf8')
scripts=WORK/'baseline-scripts';scripts.mkdir(exist_ok=True)
index=[]
for i,m in enumerate(re.finditer(r'<script\b([^>]*)>(.*?)</script>',small,re.S|re.I)):
 attrs,code=m.groups();idmatch=re.search(r'\bid=[\"\x27]([^\"\x27]+)',attrs);id=idmatch.group(1) if idmatch else str(i)
 name=f'{i:02d}-{id}.js';(scripts/name).write_text(code,'utf8');index.append({'file':name,'chars':len(code),'attrs':attrs})
(WORK/'script-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),'utf8')
print(json.dumps({'sourceHash':fingerprint[source.name]['sha256'],'previewBytes':len(small.encode()),'scripts':len(index),'output':str(OUT)},ensure_ascii=False))
