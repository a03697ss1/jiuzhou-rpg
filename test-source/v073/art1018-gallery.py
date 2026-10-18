from pathlib import Path
import json,html,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_部分項目補完_2026-10-18';A=R/'素材美術_2026-10-18'
materials=json.loads((P/'inventory1018.json').read_text('utf8'))['materials']
rows=[]
for name in materials:
 short=name.split('］',1)[1];f=A/(short+'.png');row={'name':name,'path':str(f),'exists':f.exists(),'source':'built-in image_gen','sharedKey':short}
 if f.exists():
  with Image.open(f) as im:
   alpha=im.getchannel('A') if 'A' in im.getbands() else None
   row.update(width=im.width,height=im.height,mode=im.mode,alpha=alpha.getextrema() if alpha else None,bbox=alpha.getbbox() if alpha else None,bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest())
 rows.append(row)
(O/'素材圖片檔案驗收.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),'utf8')
(O/'素材缺圖清單.json').write_text(json.dumps([r['name'] for r in rows if not r['exists']],ensure_ascii=False,indent=2),'utf8')
e=html.escape
css='body{background:#0b1720;color:#e4e7e4;font:16px Microsoft JhengHei;margin:20px}a{color:#abd4f1}.grid{display:grid;grid-template-columns:repeat(6,1fr);gap:12px}.tile{background:#172a34;border:1px solid #64756a;border-radius:10px;min-width:0;padding:12px;text-align:center}.tile img{height:128px;width:100%;object-fit:contain}.tile span{display:block;min-height:40px}h1{color:#e6cc86}p{line-height:1.6}.meta{font-size:12px;overflow-wrap:anywhere;color:#a2bbc2}'
body='<h1>V0.7.3 素材圖片清單與共用圖源</h1><p>68項原目錄＋正式合成產物［一階］龜甲片，共69項。每項使用一張獨立PNG；圖鑑、背包、工坊、商店與委託共用。此為本地測試交付，未發布GitHub。</p><p>全部以內建image_gen工具製作，原圖已保存到工作區。<a href="素材圖片生成提示詞與路徑.json">完整提示詞、生成來源及保存路徑</a> · <a href="素材缺圖清單.json">素材缺圖清單</a> · <a href="素材圖片實際顯示驗收.json">實際顯示結果</a></p>'
for start in range(0,len(rows),24):
 body+='<section id="batch'+str(start//24+1)+'"><h2>第'+str(start+1)+'～'+str(min(start+24,len(rows)))+'項</h2><div class="grid">'
 for row in rows[start:start+24]:
  short=row['sharedKey'];body+='<div class="tile"><a href="../素材美術_2026-10-18/'+e(short)+'.png">'+('<img src="../素材美術_2026-10-18/'+e(short)+'.png" alt="'+e(row['name'])+'">' if row['exists'] else '<p>圖片製作中</p>')+'</a><span>'+e(row['name'])+'</span><div class="meta">'+(str(row['width'])+'×'+str(row['height'])+'・'+row['mode'] if row['exists'] else '待補')+'</div></div>'
 body+='</div></section>'
(O/'素材圖片清單與預覽.html').write_text('<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>素材圖片清單</title><style>'+css+'</style>'+body+'</html>','utf8')
print('Material images',sum(r['exists'] for r in rows),'/',len(rows))
