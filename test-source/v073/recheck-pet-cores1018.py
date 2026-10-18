from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import json, hashlib, re

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'新三寵八核複查_2026-10-18';OUT.mkdir(exist_ok=True)
NAMES=['燐火狼','硬黑蠍','靈珠蝶']
SOURCE=Path('C:/Users/User/OneDrive/桌面/九州修仙錄_V0.7.2_下一批大更新_完整施工工作檔_2026-10-17.docx')
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def text(e):return ''.join(t.text or '' for t in e.findall('.//w:t',NS))
def read_docx(path):
 out=[];tables=[]
 with ZipFile(path) as z:
  for part in z.namelist():
   if not part.startswith('word/') or not part.endswith('.xml'):continue
   root=ET.fromstring(z.read(part))
   if part=='word/document.xml':
    body=root.find('w:body',NS)
    for i,b in enumerate(body):
     if b.tag.endswith('}tbl'):
      rows=[[text(c) for c in row.findall('w:tc',NS)] for row in b.findall('w:tr',NS)]
      tables.append({'block':i,'rows':rows});out.append({'block':i,'kind':'table','rows':rows,'text':'\n'.join(' | '.join(r) for r in rows)})
     else:out.append({'block':i,'kind':'paragraph','text':text(b)})
   else:
    hits=[text(p) for p in root.findall('.//w:p',NS) if any(n in text(p) for n in NAMES)]
    if hits:out.append({'part':part,'text':'\n'.join(hits)})
 return out,tables

blocks,tables=read_docx(SOURCE)
indexes=set()
for i,b in enumerate(blocks):
 if any(n in b['text'] for n in NAMES):indexes.update(range(max(0,i-2),min(len(blocks),i+4)))
evidence=[blocks[i] for i in sorted(indexes)]
(OUT/'最新工作檔相關原文.txt').write_text('\n\n'.join(f"區塊 {b.get('block',b.get('part'))}\n{b['text']}" for b in evidence),'utf8')
core_rows=[]
for t in tables:
 for r in t['rows']:
  if len(r)>=4 and r[0] in NAMES and re.fullmatch(r'\d+(?:/\d+){7}',r[3]):
   core_rows.append({'species':r[0],'realm':r[1],'tier':r[2],'values':list(map(int,r[3].split('/'))),'power':r[4] if len(r)>4 else None,'wordBlock':t['block']})
old=json.loads((ROOT/'V0.7.3_部分項目補完_2026-10-18/新三寵已知八核與49項缺列.json').read_text('utf8'))
audit=old['audit']
def layer_name(n):return '圓滿' if n==10 else '一二三四五六七八九'[n-1]+'層'
comparison=[]
for pet in audit:
 for layer,values in pet['wildBase'].items():
  row=next(x for x in core_rows if x['species']==pet['species'] and x['realm']=='築基'+('圓滿' if layer=='10' else '一二三四五六七八九'[int(layer)-1]) and x['tier']==('特殊' if pet['species']=='靈珠蝶' else '一般'))
  comparison.append({'species':pet['species'],'layer':int(layer),'values':values,'wordValues':row['values'],'matches':values==row['values'],'wordBlock':row['wordBlock']})
assert len(core_rows)==20 and len(comparison)==11 and all(r['matches'] for r in comparison)
checked=[]
paths=[SOURCE,ROOT/'九州修仙錄_下一輪更新施工規格.docx',ROOT/'release-tools/v071/施工工作表.docx']
paths+=list(Path('C:/Users/User/.codex/attachments').rglob('*.docx'))
for p in dict.fromkeys(paths):
 if not p.is_file():continue
 bs,ts=read_docx(p);alltext='\n'.join(b['text'] for b in bs)
 checked.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mentions':{n:alltext.count(n) for n in NAMES}})
 for b in bs:
  if any(n in b['text'] for n in NAMES) and p!=SOURCE:
   (OUT/('其他工作檔_'+p.stem+'.txt')).write_text('\n\n'.join(x['text'] for x in bs if any(n in x['text'] for n in NAMES)),'utf8');break
missing=[{'species':p['species'],'realm':x['major']+layer_name(x['layer']),'fields':['氣血','靈力','攻','道','防','道防','身','命'],'tierBasis':'特殊種最終0星裸值' if p['species']=='靈珠蝶' else '一般種0星裸值'} for p in audit for x in p['missing']]
result={'source':str(SOURCE),'sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'wordRows':core_rows,'sourceComparison':comparison,'missingRows':missing,'counts':{'wordRowsIncludingSpecialVariants':20,'independentKnownRealmRows':11,'missingRealmRows':len(missing),'missingScalarFields':len(missing)*8},'checkedDocuments':checked}
codeChecks=[]
for path in [ROOT/'release-tools/v073/monsters.js',ROOT/'V0.7.3_獨立測試_2026-10-17/Git測試分支/test-source/v073/monsters.js',ROOT/'V0.7.3_獨立測試_2026-10-17/GitHub測試發布/preview/v0.7.3/施工來源/monsters.js']:
 code=path.read_text('utf8');table={}
 for n in NAMES:
  section=re.search(re.escape(n)+r':\{([^}]+)\}',code).group(1)
  table[n]={k:list(map(int,v.split(','))) for k,v in re.findall(r'(\d+):\[([^\]]+)\]',section)}
 assert all(table[p['species']]==p['wildBase'] for p in audit)
 codeChecks.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'matchesOriginalWord':True,'knownRows':sum(len(v) for v in table.values())})
result['currentCodeChecks']=codeChecks
(OUT/'八核複查證據.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf8')
summary=[
 '九州修仙錄 新三寵八核缺值核對與補完清單',
 '核對日期：2026-10-18。這輪只查核與匯出，未修改遊戲程式、正式母檔或GitHub。',
 '結論：最新工作檔提供新三寵20列野外八核（包含一般／特殊版本），合計涵蓋11個獨立境界列。正常練氣一層孵化與練氣～築基連續成長，尚缺49個境界列，每列8欄，共392個未列欄位。這是缺列統計，不代表必須手寫392個數字；也可提供完整且正式定案的生成公式。',
 '\n一 核對來源',str(SOURCE),'工作檔C2「五隻新妖物設定與八核」、E「新增三寵物五星二選一與10心專屬」、K3「神秘妖物蛋」。',
 '已逐列對照目前0.7.3來源、獨立測試分支來源及GitHub發布來源的monsters.js；三處11個已知境界列均與Word一致。',
 '較早的下一輪施工規格、V0.7.1工作表沒有這三個物種；歷次0.7.0／0.7.1／0.7.2定案JSON也未列入新三寵。',
 '\n二 仍缺哪些境界',
 '燐火狼：練氣一～九層、練氣圓滿；築基一、二、三、四、九層。共15列／120欄。',
 '硬黑蠍：練氣一～九層、練氣圓滿；築基一、二、三、四、六、八層。共16列／128欄。',
 '靈珠蝶：練氣一～九層、練氣圓滿；築基一、二、三、四、六、七、八、九層。共18列／144欄。',
 '每列八核順序固定：氣血／靈力／攻／道／防／道防／身／命。九層與圓滿是兩個不同層位。',
 '\n三 已有數值 不需要重新補',
 '以下為0★、未穿裝備、未套好感／五星特殊突破的來源八核。燐火狼與硬黑蠍列一般種；靈珠蝶列特殊種。',
 '物種 | 境界 | 種級 | 氣血／靈力／攻／道／防／道防／身／命']
for p in audit:
 for layer,vals in p['wildBase'].items():summary.append(p['species']+' | 築基'+layer_name(int(layer))+' | '+('特殊種' if p['species']=='靈珠蝶' else '一般種')+' | '+'／'.join(map(str,vals)))
summary += [
 '\n四 種級與計算基準',
 '燐火狼、硬黑蠍：正式合法種級只有一般種、特殊種；現有一般種列×1.25並四捨五入，可重現工作檔全部9列特殊種八核。補表可給一般種0★裸值，再沿用特殊種×1.25。',
 '靈珠蝶：合法種級只有特殊種。上面476／276及715／406開頭的兩列已是特殊種實際八核，不能再乘1.25。補表若直接給特殊種0★裸值，請沿用此標示；若改給種級乘算前數值，須明確定義，避免重複乘算。',
 '三隻均未定案高危種，不需另補高危種表。',
 'Word只寫「配合本輪個體核心偏科」，列了氣血／雙防／道的定位，沒有列出三隻各八項的個體偏科倍率。通用妖物基準雖已存在，不能在欠缺倍率時直接替代個體八核，也不能把已取整的野外列倒推成正式倍率。',
 '來源Word將這批八核及戰力標為「試算待玩家驗收」；本清單完整保留原值，沒有把試算改成已驗收。',
 '\n五 已有規則 不需要再設計',
 '0★～5★倍率：1.00／1.05／1.12／1.22／1.37／1.57；全部直接由對應境界的0★計算。',
 '五星特殊突破：全八核×1.15；燐火狼氣血另×1.10；硬黑蠍防、道防各另×1.07；靈珠蝶道另×1.10。',
 '金丹～大乘：現行寵物系統已有從築基圓滿延伸的境界及層位成長公式，0.7.3已接入。這部分不算新增缺表。',
 '孵化6遊戲小時、25種選單、合法種級、五星二選一技能與MP／CD、10心任務與技能均有既有來源；本次缺口是0★八核與可連續計算的個體公式，不是上述技能或星倍率缺失。',
 '\n六 補完方式',
 '方式A：填下方49列八核，沿用11列既有值及現有種級、星級、成長規則。',
 '方式B：提供三隻各8項正式個體倍率，或另一套完整正式生成公式；明定練氣／築基適用基準、個體與種級乘算次序、取整時機，並說明如何保留現有11列（若有衝突，以你明確定案的處理方式為準）。只提供三列練氣一層起始值，仍不足以定義其他缺失層位。',
 '請不要把野外「只出現築基五／七／九／圓滿」的境界池當成寵物成長限制；寵物仍須經過練氣與中間各層。',
 '\n七 可直接補填的49列',
 '請填：氣血／靈力／攻／道／防／道防／身／命。以0★裸值為準，排除裝備、好感、五星突破與戰鬥增減益。']
for r in missing:summary.append(r['species']+' | '+r['realm']+' | '+r['tierBasis']+' | 待補／待補／待補／待補／待補／待補／待補／待補')
summary+=['\n附錄 最新Word完整20列（含一般與特殊版本）']
for r in core_rows:summary.append(' | '.join([r['species'],r['realm'],r['tier'],'／'.join(map(str,r['values']))]))
(OUT/'新三寵八核缺值與補填清單.txt').write_text('\n'.join(summary),'utf8')
print(json.dumps({'counts':result['counts'],'documents':checked,'wordBlocks':sorted(set(r['wordBlock'] for r in core_rows))},ensure_ascii=False))
