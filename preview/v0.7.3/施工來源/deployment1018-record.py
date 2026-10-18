from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]; O=ROOT/'V0.7.3_部分項目補完_2026-10-18'
r=json.loads((O/'GitHub獨立測試部署紀錄.json').read_text('utf8'))
p=O/'本輪交付清單.json';d=json.loads(p.read_text('utf8'))
d.update(published=True,formalUpdated=False,url=r['url'],deploymentCommit=r['deploymentCommit'],publicationScope='preview/v0.7.3 only')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf8')
for name in ['閱讀我_先看這裡.html','完整測試及驗收報告.html','素材圖片清單與預覽.html']:
 p=O/name;h=p.read_text('utf8')
 h=h.replace('正式母檔、正式版本及GitHub內容未更新','正式母檔與正式入口維持0.7.2；本輪成果已發布至GitHub 0.7.3獨立測試頁')
 h=h.replace('本輪未執行推送或發布','本輪已發布preview/v0.7.3獨立測試頁，正式入口未改')
 h=h.replace('未發布GitHub','已提供GitHub獨立測試頁')
 if name=='閱讀我_先看這裡.html' and 'GitHub最新0.7.3獨立測試版' not in h:
  h=h.replace('<h2>開啟遊戲</h2>','<h2>開啟遊戲</h2><p><a href="'+r['url']+'?build='+r['build']+'">GitHub最新0.7.3獨立測試版</a></p>')
 p.write_text(h,'utf8')
print(json.dumps({'recorded':True,'url':r['url'],'commit':r['deploymentCommit']}))
