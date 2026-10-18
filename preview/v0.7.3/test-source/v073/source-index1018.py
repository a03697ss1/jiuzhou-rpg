from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_部分項目補完_2026-10-18';names=['燐火狼','硬黑蠍','靈珠蝶']
rows=[]
for p in [R/('最新定案母檔_'+v+'.json') for v in ['0.7.0','0.7.1','0.7.2']]+[Path('C:/Users/User/OneDrive/桌面/九州修仙錄_設定母檔_V0.3.md')]:
 s=p.read_text('utf8');rows.append({'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'speciesMentions':{n:s.count(n) for n in names}})
data={'searchedHistoricalSources':rows,'wordEvidence':'新寵物原稿交叉查核.json','currentSpeciesTable':'release-tools/v073/monsters.js','knownCoreRows':11,'missingQiAndFoundationRows':49,'existingFormalRules':[{'file':'baseline-scripts/88-jz360-integration.js','found':'妖物通用練氣／築基八核基準；不是新三寵個體偏科表。'},{'file':'baseline-scripts/101-jzp-20261005.js','found':'金丹～大乘既有寵物成長公式與0★直接乘星倍率。'},{'file':'baseline-scripts/115-jz-round26.js','found':'升星成本3／5／7／15／20獸魂晶。'}],'conclusion':'未找到新三寵完整練氣／築基個體八核或可直接引用的個體倍率。未將野外片段數值倒推為正式定案。'}
(O/'新寵物資料來源查核索引.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),'utf8')
f=O/'BUG修復與待補清單.html';s=f.read_text('utf8').replace('</main>','<p><a href="新寵物資料來源查核索引.json">新寵物資料來源查核索引</a></p></main>');f.write_text(s,'utf8')
for name in ['art1018-gallery.py','finalize1018.py','source-index1018.py']:shutil.copy2(P/name,O/'施工來源'/name)
print('Historical source index saved; formal files were only read.')
