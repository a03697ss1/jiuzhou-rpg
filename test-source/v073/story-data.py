from pathlib import Path
import re,json
p=Path(__file__).parent
lines={int(x[:4]):x[5:] for x in (p/'spec.txt').read_text('utf8').splitlines()}
def dialog(a,b):
 out=[];speaker='旁白'
 for i in range(a,b+1):
  t=lines[i]
  if t.endswith('：') and '：' not in t[:-1]:speaker=t[:-1];continue
  m=re.match(r'^([^：]{1,16})[：](.*)',t)
  if m and ('「' in m[2] or m[1] in ['邱山河','玩家','林夏于','沈玄川','柳清妍','黃蕭','黑衣人']):speaker=m[1];t=m[2]
  if t.startswith('「') and t.endswith('」'):t=t[1:-1]
  elif not m:speaker='旁白'
  out.append({'speaker':speaker,'text':t,'important':bool(re.search('龍胤|轉靈|封印|命符|線索|黑潮|姓名|災獸之主|真相|首次|前往|獲得',t))})
 return out
d={
 '029-offer':dialog(600,629),'029-report':dialog(649,677),
 '030-offer':dialog(688,699),'030-report':dialog(708,722),
 '031-offer':dialog(758,833),'032-offer':dialog(872,921),'032-A':dialog(925,938),'032-B':dialog(948,961),
 '033A-0':dialog(1006,1025),'033A-1':dialog(1054,1079),'033A-2':dialog(1089,1151),
 '037-offer':dialog(228,252),'038-report':dialog(259,277),
 '038-NE':dialog(280,281),'038-SE':dialog(282,283)
}
(p/'story-data.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf8')
(p/'story-data.js').write_text('window.JZ073_STORY='+json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+';','utf8')
print({k:len(v) for k,v in d.items()})
