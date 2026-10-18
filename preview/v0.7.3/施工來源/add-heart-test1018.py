from pathlib import Path
p=Path(__file__).with_name('pet-complete1018.cjs');s=p.read_text('utf8')
mark="console.log(JSON.stringify({passed:rows.filter(r=>r.pass).length,total:rows.length,errors}));"
extra="""await test('正常孵化三寵的10心任務由正式技能事件累計、解鎖及防重領',async()=>{await p.addScriptTag({path:path.resolve('release-tools/v073/pet-heart-events1018.js')});return await p.evaluate(()=>runNewPetHeartAcceptance());});
"""
if extra not in s:s=s.replace(mark,extra+mark)
p.write_text(s,'utf8')
