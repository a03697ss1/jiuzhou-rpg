from pathlib import Path
P=Path(__file__).resolve().parent
out='V0.7.3_新三寵補完_2026-10-18'
for name in ['core1018.cjs','extended1018.cjs','a1018.cjs','b1018.cjs','meta1018.cjs']:
 s=(P/name).read_text('utf8').replace('V0.7.3_部分項目補完_2026-10-18',out)
 if name=='core1018.cjs':
  s=s.replace('25種神秘蛋選單；新種資料不足不扣蛋','25種神秘蛋選單；補齊新種八核後正常建立孵化蛋')
  s=s.replace("x.species===25&&!x.no&&x.before===x.after&&x.body.includes('不消耗')","x.species===25&&x.no&&x.before-x.after===1")
 (P/('pet-complete-'+name)).write_text(s,'utf8')
