from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_18項修正_2026-10-18'
d=json.loads((O/'可用寶箱與特殊資源核對.json').read_text('utf8'))
names=d['boxOptions']['list']
p=P/'review18-fixes.js';s=p.read_text('utf8')
line='N.verifiedBoxPills18='+json.dumps(names,ensure_ascii=False)+';\n'
if 'N.verifiedBoxPills18=' not in s:s=s.replace('N.wendaoSourceRows1018=',line+'N.wendaoSourceRows1018=').replace('...N.verifiedSpecialItems18])','...N.verifiedSpecialItems18,...N.verifiedBoxPills18])')
if "add('開箱','自選護體丹箱'" not in s:s=s.replace(" const tech=JZ360.byName", " if(N.verifiedBoxPills18.includes(exact))add('開箱','自選護體丹箱','使用［特殊］自選護體丹箱，選擇對應屬性護體丹。');\n const tech=JZ360.byName")
p.write_text(s,'utf8')
p=P/'revision-codex1018.js';s=p.read_text('utf8').replace('/藥水|丹$/','/藥水|丹(?:－[火水木風雷土光暗])?$/');p.write_text(s,'utf8')
p=O/'新增獨立圖片提示詞.json';jobs=json.loads(p.read_text('utf8'));existing={j['name'] for j in jobs}
themes={'火':'red cinnabar with subtle flame marbling, bronze dish','水':'deep blue with wave marbling, silver shell dish','木':'green jade with leaf marbling, carved wooden leaf dish','風':'pale cyan with spiral marbling, thin crescent dish','雷':'violet with branching silver marbling, angular metal dish','土':'ochre with mineral grain, earthenware square dish','光':'ivory with soft golden shimmer, small sunburst dish','暗':'near-black indigo with cloudy silver patches, crescent onyx dish'}
for n in names+['功法殘卷','獸魂晶','寵物飼料','寵物餅乾']:
 if n in existing:continue
 if n in names:detail='One medicinal pill, '+themes[n[-1]]+'. Modest initial-tier craftsmanship, not a bottle. Element motifs are decorative only.'
 else:detail={'功法殘卷':'One weathered fragment of an ancient martial manuscript scroll, worn jade-green silk, rolled edges, abstract faded ink marks with no readable writing.','獸魂晶':'One irregular amber-violet crystal with a subtle beast-like light silhouette inside, rough natural facets on tiny stone base.','寵物飼料':'One open small wooden feeding bowl holding coarse golden herb pellets, a few green leaves.','寵物餅乾':'One distinct crunchy golden pet biscuit shaped like a stylized paw, embossed surface, small rice-paper wrapper beneath.'}[n]
 jobs.append({'name':n,'file':n+'.png','prompt':'Use case: stylized-concept. One independent inventory icon for Chinese xianxia RPG 九州修仙錄. Hand-painted semi-realistic fantasy item illustration, rich physical texture, clear readable silhouette. Whole single object centered, transparent background. No letters, text, watermark, frame, scenery, people, collage. Item '+n+'. '+detail})
p.write_text(json.dumps(jobs,ensure_ascii=False,indent=2),'utf8')
(O/'追加核對圖片.json').write_text(json.dumps([j for j in jobs if j['name'] in names+['功法殘卷','獸魂晶','寵物飼料','寵物餅乾']],ensure_ascii=False,indent=2),'utf8')
print('Added verified existing box pills and 12 image jobs; total images',len(jobs)+1)
