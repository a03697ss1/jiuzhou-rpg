from pathlib import Path
P=Path(__file__).resolve().parent
p=P/'review18-art.js';s=p.read_text('utf8')
s=s.replace('<p>戰鬥戰位與血量同步、可重複的長右測試入口、主線行動所在地檢查、NPC靈根與同行位置、柳清妍任務入口、藥品正確階級與來源、獨立物品圖片、布告欄與交談視窗調整。</p>', '<h3>新增</h3><p>裝備、各階藥品與特殊物品的獨立圖片；補齊NPC靈根資質。</p><h3>改動</h3><p>狐毛、狐尾與獸角歸妖物素材；藥品使用你提供的數值；取得來源依完整階級與當前商店核對；布告箱移到放大的布告欄下方；交談只保留暫時離開。</p><h3>BUG修復</h3><p>戰鬥血量與戰位同步、測試999重複挑戰長右、主線行動所在地限制、蘇璃同行位置、柳清妍任務入口、功法階級顯示，以及必敗戰的手動1倍與繼續提示。</p>')
p.write_text(s,'utf8')
p=P/'review18-qa.cjs';s=p.read_text('utf8')
s=s.replace('root:JZW.itemDescription(\'［初階］靈根丹\')','root:JZW.itemDescription(\'［初階］靈根丹\'),actualStore:JZV2.askRows.map(([name,price])=>({name,price,sources:JZ073.itemSources1018(name)})),retiredStore:JZ073.itemSources1018(\'［特殊］問心劍\')')
s=s.replace("assert(x.high.every(r=>r.sources.length===0)","assert(x.actualStore.every(r=>r.sources.some(s=>s.name==='問道檯'&&s.text.includes(r.price+'問道點數')))&&!x.retiredStore.some(s=>s.name==='問道檯')&&x.high.every(r=>r.sources.length===0)")
s=s.replace('speed:battle.jz18Speed,zero:',"speed:battle.jz18Speed,speedUI:document.querySelector('.jz-speed select')?.value,speedDisabled:document.querySelector('.jz-speed select')?.disabled,zero:")
s=s.replace('assert(!before.auto&&before.speed===1&&before.zero',"assert(!before.auto&&before.speed===1&&before.speedUI==='1'&&before.speedDisabled&&before.zero")
p.write_text(s,'utf8')
p=P/'review18-package.py';s=p.read_text('utf8').replace('href="新增獨立圖片提示詞.json"','href="完整獨立圖片提示詞.json"')
p.write_text(s,'utf8')
