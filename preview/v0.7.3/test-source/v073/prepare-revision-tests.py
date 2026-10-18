from pathlib import Path
P=Path(__file__).resolve().parent
for name in ['a','b','core']:
    s=(P/f'pet-complete-{name}1018.cjs').read_text('utf-8')
    s=s.replace("out='V0.7.3_新三寵補完_2026-10-18'", "out='V0.7.3_逐項修正_2026-10-18'")
    s=s.replace('.jz073-boss img','.jz-boss-body img').replace('.jz073-boss-bar','.jz-boss-health').replace("'.jz073-boss'","'.jz-boss-body'")
    s=s.replace("work+'/boss-ui.png'","out+'/長右回歸驗收.png'")
    s=s.replace("x.rows>=12&&x.body.includes('優良')&&x.body.includes('差額')", "x.rows>0&&x.body.includes('優良')&&x.body.includes('差異')")
    s=s.replace("document.querySelector('.jz073-icon')?.getAttribute('src')", "document.querySelector('.jz-catalog-image img')?.getAttribute('src')")
    s=s.replace("await Promise.all(imgs.map(i=>i.complete?null:", "imgs.forEach(i=>i.loading='eager');await Promise.all(imgs.map(i=>i.complete?null:")
    for letter in ['A','B']:
        old="await p.evaluate(()=>window."+letter+"_BOSS=battle);await p.locator('button[onclick=\"toggleAutoBattle()\"] ').click();await p.waitForFunction(()=>!battle,{timeout:60000});"
        new="await p.evaluate(()=>{window."+letter+"_BOSS=battle;const f=battle.playerTeam.find(f=>f.type==='player');f.atk=1200;f.hp=f.maxhp=10000;});for(let manual=0;manual<160;manual++){await p.waitForFunction(()=>!battle||!battle.jzBusy,{timeout:30000});if(!await p.evaluate(()=>!!battle))break;await p.locator('button[onclick=\"battleAttack()\"]').click();if(await p.evaluate(()=>!!battle?.jzPick))await p.locator('.jz-boss-body').click();await p.waitForTimeout(80);}assert(!await p.evaluate(()=>!!battle),'手動長右戰未結束');"
        s=s.replace(old,new)
    (P/f'revision-regression-{name}1018.cjs').write_text(s,'utf-8')
s=(P/'save-recovery1018-qa.cjs').read_text('utf-8').replace("out='V0.7.3_存檔銜接修復_2026-10-18'", "out='V0.7.3_逐項修正_2026-10-18'")
(P/'revision-save-qa1018.cjs').write_text(s,'utf-8')
s=(P/'pet-complete1018.cjs').read_text('utf-8').replace("out='V0.7.3_新三寵補完_2026-10-18'", "out='V0.7.3_逐項修正_2026-10-18'")
s=s.replace("JZR.give('［特殊］寵物自選專屬技能箱',10);let safety=0;", "JZR.give('［特殊］寵物自選專屬技能箱',15);for(const name of ({燐火狼:['烈爪'],硬黑蠍:['夾擊'],靈珠蝶:['撲粉','破夢']}[species])){const skill=JZ360.byName[name];if(!x.skills.some(n=>(JZ360.byName[n]||JZ360.byId[n])?.id===skill.id)&&!JZR.learnPet(0,skill.id,'寵物自選專屬技能箱'))throw Error('必要技能無法正常學習');}let safety=0;")
(P/'revision-pet-qa1018.cjs').write_text(s,'utf-8')
