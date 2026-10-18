from pathlib import Path
import json,re,base64,hashlib,sys
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_部分項目補完_2026-10-18'
if '--output-dir' in sys.argv:O=R/sys.argv[sys.argv.index('--output-dir')+1];O.mkdir(parents=True,exist_ok=True)
baseline=json.loads((P/'baseline.json').read_text('utf8'))
assets=R/'新增美術_2026-10-16'
art={k:assets/v for k,v in {'長右':'災獸長右_完整透明立繪.png','財寶怨靈':'財寶怨靈_完整透明立繪.png','燐火狼':'燐火狼_完整透明立繪.png','硬黑蠍':'硬黑蠍_完整透明立繪.png','靈珠蝶':'靈珠蝶_完整透明立繪.png','陸刑舟':'陸刑舟_完整透明立繪.png','陸景和':'陸景和_完整透明立繪.png','黑衣人01':'黑衣人01_完整透明立繪.png','黑衣人02':'黑衣人02_完整透明立繪.png','黑衣人03':'黑衣人03_完整透明立繪.png','黑潮禁岸':'黑潮禁岸_地圖場景.png','深窟':'雷鳴沼地下深窟_地圖場景.png','黑潮戰鬥':'黑潮禁岸_戰鬥背景.png','深窟戰鬥':'雷鳴沼地下深窟_戰鬥背景.png'}.items()}
hooks=[
 ("function speed(){return S?.settings?.battleSpeed===1.5?1.5:1;}","function speed(){return battle?.jz073PlotLoss||battle?.jz18Speed===1?1:S?.settings?.battleSpeed===1.5?1.5:1;}"),
 ("function startQueue(b){b.jzQueue=[...b.playerTeam,...b.enemyTeam].filter(f=>f.hp>0).sort((a,c)=>engine.stat(c,'agi')-engine.stat(a,'agi'));b.jzIndex=0;}","function startQueue(b){b.jzQueue=[...b.playerTeam,...b.enemyTeam].filter(f=>f.hp>0).sort((a,c)=>engine.stat(c,'agi')-engine.stat(a,'agi'));if(b.jz073PlotB||b.jz073PlotA)b.jzQueue.sort((a,c)=>Number(!!(c.jz073PlotB||c.jz073PlotA))-Number(!!(a.jz073PlotB||a.jz073PlotA)));b.jzIndex=0;}"),
 ("const a=selected?.length?(r.repeatTargets?selected:[...new Set(selected)]).filter(x=>p.includes(x)):p.slice(0,cap);", "const a=selected?.length?(r.repeatTargets?selected:[...new Set(selected)]).filter(x=>p.includes(x)):(globalThis.JZ073?.randomTargets(b,f,r,p,cap)??p.slice(0,cap));"),
 ("function add(b,a,t,op){if(!alive(t))return false;", "function add(b,a,t,op){if(!alive(t)||globalThis.JZ073?.preventStatus(b,a,t,op))return false;"),
 ("if(!r)return '找不到功法資料';if(r.pending)", "if(!r)return '找不到功法資料';if(b?.jz073PlotLoss&&b.enemyTeam.includes(f)&&r.id===b.jz073PlotSkill)return '';if(r.pending)"),
 ("const p=effectChance(b,a,t,op);if(rng()>=p)", "const p=globalThis.JZ073?.statusChance(b,a,t,op,effectChance(b,a,t,op))??effectChance(b,a,t,op);if(rng()>=p)"),
 ("function finish(b){if(!ended(b))return false;", "function finish(b){if(!ended(b))return false;if(globalThis.JZ073?.finishStoryBattle(b,!b.enemyTeam.some(f=>f.hp>0)))return true;"),
 ("const cost=20*(1-(aux?.energyBonus||0)/100);if(x.aura<cost)","const cost=0;if(x.aura<cost)"),
]
isolation='''<script id="jz073-save-isolation">(()=>{const p='jz073-independent-20261017:',g=Storage.prototype.getItem,s=Storage.prototype.setItem,r=Storage.prototype.removeItem;window.JZ073_ORIGINAL_STORAGE=Object.freeze({read:key=>g.call(localStorage,key)});Storage.prototype.getItem=function(k){return g.call(this,p+k)};Storage.prototype.setItem=function(k,v){return s.call(this,p+k,v)};Storage.prototype.removeItem=function(k){return r.call(this,p+k)};window.JZ073_SAVE_PREFIX=p;})();</script>'''
def apply(text,standalone):
 def branch_version(m):
  return m[0].replace("phase='正式'","phase='獨立測試・待玩家驗收'").replace('masterPromoted=true','masterPromoted=false').replace('V0.7.2','V0.7.3 獨立測試').replace('九州修仙錄 0.7.2','九州修仙錄 0.7.3 獨立測試')
 text,n=re.subn(r'<script id="jz072-official">.*?</script>',branch_version,text,flags=re.S)
 assert n==1
 text=text.replace('<h1>V0.7.2</h1>','<h1>V0.7.3</h1>').replace('>正式版 0.7.2</div>','>獨立測試版 0.7.3・待玩家驗收</div>')
 for a,b in hooks:
  count=text.count(a)
  if count!=1:raise ValueError(f'Hook count {count}: {a}')
  text=text.replace(a,b)
 text=text.replace('<head>','<head>'+isolation,1)
 code='\n<style id="jz073-style">'+(P/'style.css').read_text('utf8')+'</style>\n'
 images={k:('data:image/png;base64,'+base64.b64encode(v.read_bytes()).decode() if standalone else '/新增美術_2026-10-16/'+v.name) for k,v in art.items()}
 code+='<script id="jz073-assets">window.JZ073_ART='+json.dumps(images,ensure_ascii=False).replace('</','<\\/')+';</script>\n'
 materials={v.stem:('data:image/png;base64,'+base64.b64encode(v.read_bytes()).decode() if standalone else '/素材美術_2026-10-18/'+v.name) for v in (R/'素材美術_2026-10-18').glob('*.png')}
 code+='<script id="jz073-material-assets">window.JZ073_MATERIAL_ART='+json.dumps(materials,ensure_ascii=False).replace('</','<\\/')+';</script>\n'
 for folder,key in [('物品美術_2026-10-18','JZ073_ITEM_ART'),('人物全身_2026-10-18','JZ073_FULLBODY_ART'),('物品獨立美術_2026-10-18','JZ073_ITEM_UNIQUE_ART')]:
  pictures={v.stem:('data:image/png;base64,'+base64.b64encode(v.read_bytes()).decode() if standalone else '/'+folder+'/'+v.name) for v in (R/folder).glob('*.png')}
  code+='<script>window.'+key+'='+json.dumps(pictures,ensure_ascii=False).replace('</','<\\/')+';</script>\n'
 for name in ['core','economy','monsters','combat','story-data','humans','quests','world','commissions','pets','codex','ui','completion','clarifications','b-data','b-story','a-data','a-story','npc-generation','test-entry','side1018-data','side1018','material1018','pet-cores1018','pet1018','status1018','release1018','save-recovery1018','revision-world1018','revision-items1018','revision-codex1018','revision-help1018','revision-boss1018','revision-finish1018','review18-fixes','review18-art','hidden-steal1019','items1019','boss1019','battle1019','equipment1019','boss-bar1019']:
  f=P/(name+'.js')
  if f.exists():code+='<script id="jz073-'+name+'">'+f.read_text('utf8')+'</script>\n'
 return text+code
small=apply((P/'baseline-preview.html').read_text('utf8'),False);(P/'preview.html').write_text(small,'utf8')
import sys
if '--full' in sys.argv:
 source=R/'九州修仙錄_測試分支.html'
 assert hashlib.sha256(source.read_bytes()).hexdigest()==baseline['protected'][source.name]['sha256']
 (O/'九州修仙錄_V0.7.3_獨立測試版.html').write_text(apply(source.read_text('utf8'),True),'utf8')
print('Built preview'+(' and standalone' if '--full' in sys.argv else ''))
