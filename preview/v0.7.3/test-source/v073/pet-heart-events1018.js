/* Acceptance fixture: pets come from the real six-hour hatch above. Controlled formal-monster combat events; no task counters are assigned. */
window.runNewPetHeartAcceptance=function(){const N=JZ073,R=JZR,C=JZ360,P=JZP,results=[],old=Math.random;Math.random=()=>0;try{
 const makeBattle=(pet,enemies)=>{const f=R.petStats(pet),b={round:1,auto:false,playerTeam:[f],enemyTeam:enemies,logs:[],v071Place:'青陽山',jzLab:false};[f,...enemies].forEach((u,i)=>{u.jzId='pet-accept-'+i;C.init(u);});C.restore(b,f,f,C.stat(f,'maxmp'),true);if(pet.species!=='燐火狼')C.restore(b,f,f,C.stat(f,'maxhp'));return b;};
 const cast=(b,a,skill,t)=>{b.round+=6;b.jzwCurrentRule=C.byId[skill]||C.byName[skill]||skill;const out=C.cast(b,a,skill,[t]);if(!out.ok)throw Error((skill.name||skill)+' '+out.reason);return out;};
 const foe=(layer=1)=>JZMON.stats('青木狼','q',layer,'特殊種');
 for(const species of N.newPetSpecies){battle=null;S.pets=[structuredClone(S.v073PetAcceptance[species])];const pet=S.pets[0],x=R.petData(pet),before=[...x.heartTask.counts];
 if(species==='燐火狼')for(let j=0;j<5;j++){const b=makeBattle(pet,[foe(),foe(),foe()]),a=b.playerTeam[0];for(const e of b.enemyTeam)cast(b,a,'烈爪',e);P.finishBattle(b,true);}
 if(species==='硬黑蠍'){const enemies=Array.from({length:3},()=>JZMON.stats('青木狼','z',10,'特殊種')),b=makeBattle(pet,enemies),a=b.playerTeam[0];for(let j=0;j<15;j++){const e=enemies[j%3];C.remove(e,'束縛');cast(b,a,'夾擊',e);}for(let j=0;j<5;j++)cast(b,enemies[0],C.basic,a);for(const e of enemies)while(e.hp>0)cast(b,a,C.basic,e);P.finishBattle(b,true);}
 if(species==='靈珠蝶'){const enemies=Array.from({length:3},()=>JZMON.stats('青木狼','z',10,'特殊種')),b=makeBattle(pet,enemies),a=b.playerTeam[0];for(let j=0;j<20;j++){const e=enemies[j%3];cast(b,a,'撲粉',e);}for(const e of enemies){C.remove(e,'睡眠');cast(b,a,'撲粉',e);if(!C.has(e,'睡眠'))throw Error('撲粉未施加睡眠');cast(b,a,'破夢',e);}P.finishBattle(b,true);}
 battle=null;const ready=P.heartReady(pet),counts=[...x.heartTask.counts];if(!ready)throw Error(species+'任務未完成 '+JSON.stringify({counts,skills:x.skills,prereq:P.heartPrereq(pet)}));if(!P.claimHeart(0)||P.claimHeart(0))throw Error('領獎不正確');const id=x.heartTask.id;if(!JZV2.isLegalSkill(pet,id))throw Error('專屬技能未解鎖');S.v073PetAcceptance[species]=structuredClone(pet);results.push({species,before,counts,ready,claimed:x.heartTask.claimed,skill:id,petOrigin:'正常神秘蛋選擇、等待360遊戲分鐘並開啟；本測試不寫入任務計數'});
 }
 r4WriteSave('3',{silent:true});return results;
 }finally{Math.random=old;battle=null;}};
