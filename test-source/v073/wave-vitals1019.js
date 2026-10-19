(function(){'use strict';const N=JZ073,R=JZR,P=JZP;
const petFor=s=>{const p=S.pets[s.index];return p&&p.name===s.name?p:null;};
N.waveVitals1019=(run,fromPet)=>{if(!run)return;for(const s of run.states||[]){const p=petFor(s);if(!p)continue;const f=R.petStats(p);s.maxhp=f.maxhp;s.maxmp=f.maxmp;if(fromPet){s.hp=f.hp;s.mp=f.mp;}else{p.hp=Math.max(0,Math.min(f.maxhp,s.hp));p.mp=Math.max(0,Math.min(f.maxmp,s.mp));}}};
const save=R.saveRun;R.saveRun=function(){if(!battle)N.waveVitals1019(R.beast().run,false);return save.apply(this,arguments);};
const start=P.startWave;P.startWave=function(){if(!battle){const run=R.beast().run;if(run?.saved)N.waveVitals1019(run,true);}return start.apply(this,arguments);};
const open=R.openRun;R.openRun=function(){if(!battle){const run=R.beast().run;if(run?.saved)N.waveVitals1019(run,true);}return open.apply(this,arguments);};
const recover=R.runRecover;R.runRecover=function(size){if(battle)return recover.apply(this,arguments);const run=R.beast().run,key=size===30?'recovery30':size===50?'recovery50':'';if(run&&key&&run.completed&&run[key]>0){if(run.saved)N.waveVitals1019(run,true);run.saved=false;}const out=recover.apply(this,arguments);if(out){N.waveVitals1019(run,false);R.save();}return out;};
const finish=R.finishPetBattle;R.finishPetBattle=function(b,win){const fresh=b?.jzPetMode?.mode==='wave'&&!b.jzrSettled,out=finish.apply(this,arguments);if(fresh){N.waveVitals1019(R.beast().run,false);R.save();}return out;};
const settle=R.settleRun;R.settleRun=function(){if(battle)return settle.apply(this,arguments);const run=R.beast().run;if(!run)return settle.apply(this,arguments);const pets=(run.states||[]).map(petFor).filter(Boolean),out=settle.apply(this,arguments);if(!R.beast().run){for(const p of pets){const f=R.petStats(p);p.hp=f.maxhp;p.mp=f.maxmp;}R.save();renderPlayer();log('萬妖陣已結算，參戰寵物氣血與靈力已全部恢復。');}return out;};
if(N.releaseHistory073){N.releaseHistory073.BUG修復.push('萬妖陣儲存退出同步寵物氣血靈力；醫館治療後重新進場採用治療後數值，不再被舊波次數值覆蓋。');N.releaseHistory073.改動.push('萬妖陣退出結算後，參戰寵物自動恢復滿氣血與滿靈力。');}
})();
