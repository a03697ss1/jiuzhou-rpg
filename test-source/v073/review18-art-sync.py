from pathlib import Path
import json,shutil,re
R=Path(__file__).resolve().parents[2];D=R/'物品獨立美術_2026-10-18'
ok=[];bad=[]
for f in (D/'生成紀錄').glob('*.json'):
 try:
  x=json.loads(f.read_text('utf-8-sig'));source=x['source'].replace('\\','/');source=source[source.rfind('C:/'):];p=Path(source)
  if not p.exists():raise ValueError(source)
  target=D/(x['name']+'.png')
  if not target.exists():shutil.copy2(p,target)
  x.update(source=source,file=str(target),method='built-in imagegen');f.write_text(json.dumps(x,ensure_ascii=False,indent=2),'utf8');ok.append(x)
 except Exception as e:bad.append({'file':str(f),'error':str(e)})
(R/'V0.7.3_18項修正_2026-10-18/新增獨立圖片來源.json').write_text(json.dumps(ok,ensure_ascii=False,indent=2),'utf8')
print(json.dumps({'copied':len(ok),'totalPNG':len(list(D.glob('*.png'))),'bad':bad},ensure_ascii=False))
