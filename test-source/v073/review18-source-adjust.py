from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;O=P.parents[1]/'V0.7.3_18項修正_2026-10-18';d=json.loads((O/'施工前資料核對.json').read_text('utf8'))
p=P/'review18-fixes.js';s=p.read_text('utf8')
line='N.verifiedSpecialItems18='+json.dumps(d['additionalAuthoritativeSpecialItems']+['［特殊］潮汐秘境通行證','［特殊］小型煉金爐','［特殊］鑄造台','［特殊］長右之心','［特殊］山河護身令'],ensure_ascii=False)+';\n'
if 'N.verifiedSpecialItems18=' not in s:s=s.replace('// Match fully qualified items:',line+"N.wendaoSourceRows1018=(JZV2.askRows||[]).map(([name,price])=>[name,price]);\n// Match fully qualified items:")
else:s=re.sub(r'N\.verifiedSpecialItems18=\[.*?\];\n',lambda m:line,s,count=1)
s=s.replace("const allItems=N.allItemNames1018;N.allItemNames1018=()=>allItems().filter(n=>n!==N.deletedItem18);","const allItems=N.allItemNames1018;N.allItemNames1018=()=>[...new Set([...allItems(),...N.verifiedSpecialItems18])].filter(n=>n!==N.deletedItem18);")
s=s.replace("add('兌換','問道檯','問道檯商店・'+price+'問道積分')","add('兌換','問道檯','問道檯商店・'+price+'問道點數')")
s=s.replace("for(const [heart,n,qty=1] of gifts)if(same(n))", "for(const [heart,n,qty=1] of gifts)if(!(npc==='邱山河'&&heart>=10)&&same(n))")
s=s.replace(" const g=R546_GEAR_FULL[exact];if(g?.source&&!['任務','任務取得','配方','鍛造','裝備商人'].includes(g.source))add('物品',exact,g.source);", " if(['［特殊］滿貫丹','［特殊］隨機功法書','［特殊］山河護身令'].includes(exact))add('NPC贈禮','邱山河','B路線完成［支線］與山河聊聊，解鎖邱山河10心收取禮物。');")
if "if(exact==='［特殊］長右之心')" not in s:s=s.replace(" if(exact==='［任務］命符')", " if(exact==='［特殊］長右之心')add('任務','038','擊敗長右後，於［主線］第一封印。長右的後續交談取得，僅一次。');\n if(exact==='［任務］命符')")
p.write_text(s,'utf8')
p=P/'review18-art.js';s=p.read_text('utf8').replace("window.JZ073_ITEM_UNIQUE_ART?.[base]||icon.apply", "window.JZ073_ITEM_UNIQUE_ART?.[base]||(!base.startsWith('［')&&(window.JZ073_ITEM_UNIQUE_ART?.['［初階］'+base]||window.JZ073_ITEM_UNIQUE_ART?.['［特殊］'+base]))||icon.apply");p.write_text(s,'utf8')
