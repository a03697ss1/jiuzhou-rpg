from pathlib import Path
p=Path(__file__).with_name('save-recovery1018-qa.cjs');s=p.read_text('utf8')
s=s.replace("for(const s of ['auto','1','2','3'])r4WriteSave(s,{silent:true});return Object.fromEntries", "for(const s of ['auto','1','2','3'])r4WriteSave(s,{silent:true});clearTimeout(r4AutoTimer);return Object.fromEntries",1)
needle="const found=await p.evaluate(()=>JZ073.saveRecovery.original().map"
s=s.replace(needle,"original=await p.evaluate(()=>Object.fromEntries(['auto','1','2','3'].map(s=>[s,JZ073_ORIGINAL_STORAGE.read(r4SaveKey(s))])));const found=await p.evaluate(()=>JZ073.saveRecovery.original().map",1)
p.write_text(s,'utf8')
