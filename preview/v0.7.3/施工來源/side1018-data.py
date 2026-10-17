from pathlib import Path
import re,json
P=Path(__file__).resolve().parent
data={}
for key in ['015','016']:
 s=(P/('side'+key+'-original.txt')).read_text('utf8')
 s=s[s.index('第一階段：'):s.index('第五階段：任務完成' if key=='015' else '第六階段：任務完成')]
 rows=[]
 for line in s.splitlines():
  t=line.strip()
  if not t or re.match(r'^第.+階段：',t):continue
  m=re.fullmatch(r'([^：]+)：「(.*)」',t)
  rows.append({'speaker':m[1] if m else '旁白','text':m[2] if m else t,'important':any(w in t for w in ['父親還','父親，或許','危險區開放','身世','猜測','沒有證據'])})
 data[key]=rows
(P/'side1018-data.js').write_text('window.JZ073_SIDE1018='+json.dumps(data,ensure_ascii=False,indent=1)+';','utf8')
(P/'side1018-dialogues.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),'utf8')
print({k:len(v) for k,v in data.items()})
