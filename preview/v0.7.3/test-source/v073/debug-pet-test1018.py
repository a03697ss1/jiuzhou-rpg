from pathlib import Path
p=Path(__file__).with_name('pet-complete1018.cjs')
s=p.read_text('utf8').replace("throw Error('讀檔遺失');","throw Error('讀檔檢查 '+JSON.stringify({species,x,prereq:JZP.heartPrereq(pet),learned:x.skills.map(n=>(JZ360.byName[n]||JZ360.byId[n])?.name)}));")
p.write_text(s,'utf8')
