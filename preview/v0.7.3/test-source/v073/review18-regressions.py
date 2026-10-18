from pathlib import Path
P=Path(__file__).resolve().parent
for name in ['core','a','b']:
 s=(P/('revision-regression-'+name+'1018.cjs')).read_text('utf8').replace('V0.7.3_逐項修正_2026-10-18','V0.7.3_18項修正_2026-10-18')
 for branch in ['A','B']:
  a="await p.waitForFunction(()=>!battle&&JZ073.quest('034"+branch+"').progress.phase==='post'"
  b="await p.waitForFunction(()=>battle?.jz18AwaitPlot,{timeout:30000});await p.locator('[onclick=\"JZ073.continuePlot18()\"]').click();"+a
  s=s.replace(a,b)
 (P/('review18-regression-'+name+'.cjs')).write_text(s,'utf8')
p=P/'review18-visual.cjs';s=p.read_text('utf8').replace("JZ073.debugScenario('world');closeModal();JZ071.openBoard();","JZ073.debugScenario('world');S.quests.push({id:'confirmCult',claimed:true,done:true,progress:{}});closeModal();JZ071.openBoard();");p.write_text(s,'utf8')
