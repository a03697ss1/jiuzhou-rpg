from pathlib import Path
p=Path(__file__).with_name('review18-fixes.js');s=p.read_text('utf8')
extra=""" const pack={'［特殊］節能粉':5,'［特殊］良護藥劑':5,'［特殊］桂淞粉':5,'［特殊］成良粉':5,'［初階］百靈藥水':50,'［特殊］自選二階素材箱':8,'［特殊］自選二階妖物素材箱':8,'［初階］靈根丹':3,'［特殊］隨機功法書':1};if(pack[exact])add('禮包','東州大禮包','使用［特殊］東州大禮包取得×'+pack[exact]+'。');
 if(exact==='［特殊］滿貫丹'||exact==='［特殊］隨機功法書')add('地區','黑潮禁岸','A路線取得黑潮禁岸線索後，第'+(exact==='［特殊］滿貫丹'?'1':'2')+'次挖掘取得。');
 const routeRewards={'［初階］氣血藥水':['青陽山',20],'［初階］靈力藥水':['青陽山',20],'［初階］百靈藥水':['落星谷',15],'［初階］靈根丹':['雷鳴沼',1],'功法殘卷':['雷鳴沼',1]};if(routeRewards[exact]){const [area,qty]=routeRewards[exact],d=N.def('030');add('任務',d.id,'［主線］'+d.title+'：選擇調查'+area+'並完成回報時取得×'+qty+'。');}
"""
if "const pack={'［特殊］節能粉'" not in s:s=s.replace(" if(exact==='［特殊］長右之心')",extra+" if(exact==='［特殊］長右之心')")
s=s.replace("const pstats=JZ072.partnerStats;JZ072.partnerStats=function(p){const f=pstats.apply(this,arguments);if(f&&N.npcRoots18[p?.name]){f.rootValues={...N.npcRoots18[p.name]};", "const pstats=JZ072.partnerStats;JZ072.partnerStats=function(p){const f=pstats.apply(this,arguments),v=N.npcRoots18[p?.name]||N.npcRoots18[N.npcRootAliases18[p?.name]];if(f&&v){f.rootValues={...v};")
p.write_text(s,'utf8')
