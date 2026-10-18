from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_部分項目補完_2026-10-18'
read=lambda p:json.loads(p.read_text('utf-8-sig'))
commit=read(O/'本地測試分支保存紀錄.json');data=read(O/'本輪交付清單.json');data['localTestCommit']=commit
(O/'本輪交付清單.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),'utf8')
f=O/'完整測試及驗收報告.html';s=f.read_text('utf8');needle='<h2>本地測試分支保存</h2>'
if needle not in s:s=s.replace('</main>',needle+'<p>已保存至獨立測試分支，未推送GitHub。</p><p><a href="本地測試分支保存紀錄.json">本地保存紀錄</a> · <a href="測試分支本地驗收.json">測試分支實際載入驗收</a></p></main>');f.write_text(s,'utf8')
for row in read(O/'正式與已發布檔案保護驗證.json'):
 h=hashlib.sha256()
 with (R/row['path']).open('rb') as stream:
  for chunk in iter(lambda:stream.read(8*1024*1024),b''):h.update(chunk)
 assert h.hexdigest()==row['before'],row['path']
manifest=read(O/'素材圖片生成提示詞與路徑.json')
assert len(manifest)==69 and len({r['name'] for r in manifest})==69
assert not read(O/'素材缺圖清單.json')
print(json.dumps({'localCommit':commit['commit'],'pushed':commit['pushed'],'tests':data['passedChecks'],'materials':data['materials'],'sourceRows':data['sourceRows'],'standaloneBytes':(O/'九州修仙錄_V0.7.3_獨立測試版.html').stat().st_size,'protectedFilesUnchanged':5},ensure_ascii=False))
