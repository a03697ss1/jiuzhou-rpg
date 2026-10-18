from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[2];O=R/'V0.7.3_18項修正_2026-10-18';D=R/'物品獨立美術_2026-10-18';D.mkdir(exist_ok=True)
x=json.loads((O/'施工前資料核對.json').read_text('utf8'))
previous={r['name']:r for r in json.loads((O/'新增獨立圖片提示詞.json').read_text('utf8'))} if (O/'新增獨立圖片提示詞.json').exists() else {}
gear=x['equipment'];names=[r['name'] for r in gear]+[r['name'] for r in x['medicines'] if '凝靈妖丹' not in r['name']]
names += [n for n in x['specials'] if n not in names]
names += x.get('additionalAuthoritativeSpecialItems',[])
names += ['［特殊］長右之心','［特殊］山河護身令']
names += ['［特殊］潮汐秘境通行證','［特殊］小型煉金爐','［特殊］鑄造台']
slots={r['name']:r['slot'] for r in gear}
base='Use case: stylized-concept. One finished independent inventory illustration for Chinese xianxia RPG 九州修仙錄. Hand-painted semi-realistic fantasy equipment art, rich physical material texture, clean silhouette, whole single object centered and fully visible, transparent background. No letters, numbers, text, watermark, frame, scenery, people, collage, or multiple options. Square composition, readable thumbnail. '
jobs=[]
for i,n in enumerate(dict.fromkeys(names)):
 if n=='［特殊］小型煉金爐':continue
 tier=re.match(r'［([^］]+)］',n).group(1) if n.startswith('［') else '初階'
 level={'無階':0,'初階':1,'中階':2,'高階':3,'仙階':4,'天階':5,'特殊':4}.get(tier,1)
 luxury=['plain practical unadorned wood and iron','modest bronze or silver fittings, only subtle engraving','refined jade inlay, fine patterned metalwork and silk tassel','luxurious gold filigree, gemstone settings, intricate relief carvings','magnificent ethereal jade and platinum, luminous crystals, elaborate cloud motifs','supremely majestic divine gold and crystal, layered ornate crown-like fittings, restrained radiant aura'][level]
 detail='Item name and design theme: '+n+'. '
 if n in slots:detail+='Type: '+slots[n]+'. Design actual object matching this name and material/element/animal/cloud theme. Each item has its own distinctive silhouette and ornament. '
 elif '藥水' in n:
  kind='red healing liquid' if '氣血' in n else 'blue spiritual liquid' if '靈力' in n else 'violet dual-tone restorative liquid' if '綜合' in n else 'herbal medicinal liquid'
  detail+='A single Chinese elixir bottle with '+kind+', '+['simple small round clay vial','simple small glazed ceramic flask','faceted jade flask with carved stopper','elegant precious crystal vessel with gold collar','exquisite floating-cloud crystal flask with elaborate silver lotus stopper','majestic divine crystal vessel with golden crown stopper and luminous suspended medicine'][level]+'. '
 elif '丹' in n:detail+='A single medicinal pill on its own small open carved container, jade/porcelain pill presentation; visibly differentiated pill color, surface pattern and container matching the named medicine, not a potion flask. '
 elif '小型煉金爐' in n:detail+='Small portable three-legged bronze alchemy furnace with gentle amber fire. '
 elif '鑄造台' in n:detail+='Miniature compact blacksmith workbench with steel anvil, small hammer and organized tools, a single integrated portable crafting station. '
 elif '通行證' in n:detail+='An ornate wave-pattern jade travel permit on a short blue silk cord, clear token silhouette, no written symbols. '
 elif '箱' in n:detail+='One distinctive small treasure chest, its surface motif clearly represents the named contents. '
 elif '蛋' in n:detail+='One magical creature egg, ivory shell with distinct natural glowing vein patterns. '
 elif '粉' in n:detail+='One open small shallow porcelain jar with magical powder appropriate to item name. '
 elif '玉' in n or '石' in n or '魂' in n:detail+='One carved jade/stone/crystal talisman matching its theme, distinctive silhouette. '
 else:detail+='Depict the named object literally, identifiable and distinctive, never substitute a generic bag unless the item actually is a bag. '
 detail+='Craftsmanship tier: '+tier+', '+luxury+'. Distinguishing artistic variation: '+['lotus contours','angular mountain motifs','flowing cloud engravings','feather-like detailing','coiling vine patterns','subtle crescent moon profile','wave-like ridges','star shaped settings'][i%8]+', '+['muted blue and antique silver','deep teal and warm bronze','burgundy and pale gold','ivory and cool jade','charcoal and copper','indigo and platinum'][i%6]+'. Ornamental motifs are visual decoration only, do not imply extra gameplay abilities.'
 jobs.append(previous.get(n) or {'name':n,'file':n+'.png','prompt':base+detail})
(O/'新增獨立圖片提示詞.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),'utf8')
print(json.dumps({'jobs':len(jobs),'gear':len(gear)},ensure_ascii=False))
