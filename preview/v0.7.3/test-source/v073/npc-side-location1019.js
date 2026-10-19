(function(){'use strict';const N=JZ073,U=JZ071;
// User-confirmed correction: Lin returns to Qingyang Town after the first seal.
const side=N.def('SQ-DZ-015');side.place='青陽鎮';R56_QUESTS[side.id].place='青陽鎮';for(const row of JZ073_SIDE1018['015'])if(row.speaker==='旁白'&&row.text==='玩家在朝御城遇見林夏于。')row.text='玩家在青陽鎮遇見林夏于。';
const tuples=new Map();for(const data of Object.values(EAST_CONTENT))for(const row of data.npcs||[])if(!tuples.has(row[0]))tuples.set(row[0],[...row]);
const sync=N.syncWorld;N.syncWorld=function(){if(S&&N.done('038')){const places=N.state().story.npcPlaces??={};places.林夏于='青陽鎮';}const out=sync.apply(this,arguments);if(!S)return out;const places={...N.state().story.npcPlaces};for(const p of S.partners||[])if(p.story073)places[p.name]='同行中';for(const [name,place] of Object.entries(places)){const expected=EAST_CONTENT[place],hits=Object.entries(EAST_CONTENT).flatMap(([area,data])=>(data.npcs||[]).filter(row=>row[0]===name).map(()=>area));if(hits.length===(expected?1:0)&&(!expected||hits[0]===place))continue;const row=tuples.get(name)||[name,JZNEXT.npcs[name]?.identity||JZNEXT.npcs[name]?.role||'',''];for(const data of Object.values(EAST_CONTENT))if(data.npcs)data.npcs=data.npcs.filter(row=>row[0]!==name);if(expected)(expected.npcs??=[]).push([...row]);}return out;};
const people=renderPeople;renderPeople=function(){U.updateNpcLocations();N.syncWorld();return people.apply(this,arguments);};
const rows=N.catalogRows1018;N.catalogRows1018=function(tab){if(tab==='NPC'){U.updateNpcLocations();N.syncWorld();}return rows.apply(this,arguments);};
if(N.releaseHistory073)N.releaseHistory073.BUG修復.push('第一封印後林夏于在青陽鎮，圖鑑、人物列表與任務引導同步；危險區改在青陽鎮接取，保留兩日等待、完整對話與一次性獎勵。修復其他主線NPC人物列表仍使用舊固定位置的問題。');
})();
