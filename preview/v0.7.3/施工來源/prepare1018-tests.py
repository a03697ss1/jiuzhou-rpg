from pathlib import Path
P=Path(__file__).resolve().parent
old='V0.7.3_獨立測試_2026-10-17';new='V0.7.3_部分項目補完_2026-10-18'
base=(P/'accept.cjs').read_text('utf8')
header=base[:base.index("await test('L38'")]
tail=base[base.index('const meta=await p.evaluate'):]
extended=header+(P/'extended-tests.js').read_text('utf8')+'\n'+tail.replace('施工測試結果.json','擴充流程測試結果.json')
for name,s in [('core1018',base),('extended1018',extended),('a1018',(P/'a-accept.cjs').read_text('utf8')),('b1018',(P/'b-accept.cjs').read_text('utf8'))]:
 (P/(name+'.cjs')).write_text(s.replace(old,new),'utf8')
print('Four supplement-only test runners prepared; previous reports preserved.')
