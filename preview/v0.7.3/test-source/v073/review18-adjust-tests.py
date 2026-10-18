from pathlib import Path
p=Path(__file__).with_name('review18-qa.cjs');s=p.read_text('utf8')
for a,b in [('S.rootValues?.火','S.roots?.火'),('S.rootValues.火','S.roots.火'),('JZNEXT.npcs[n]?.rootValues',"JZNEXT.npcs[n==='萬乾坤'?'萬錢坤':n]?.rootValues"),("JZ073.offer('033A');QA18.finish();S.place='青陽山';","S.place='青陽山';JZ073.offer('033A');QA18.finish();")]:s=s.replace(a,b)
p.write_text(s,'utf8')
