(function(){'use strict';const N=JZ073,W=JZW,R=JZR;
// Apply entry preference only after a real arena battle was created.
for(const key of ['startRandom','startFloor']){const start=W[key];W[key]=function(){const before=battle,out=start.apply(this,arguments),b=battle;if(b&&b!==before&&b.jzWendao&&!!b.auto!==!!JZ1007.config().enterAuto)toggleAutoBattle();return out;};}
const finish=W.endChallenge;W.endChallenge=function(b,win){if(b?.jzWendao?.mode!=='cross')return finish.apply(this,arguments);if(b.jzwPaid)return;b.jzwPaid=true;const x=S.eastWord.wendao,r=b.jzWendao;if(win){x.streak++;const q=64+Math.min(x.streak,5);x.points=(Number(S.special['［特殊］問道點數'])||x.points||0)+q;S.special['［特殊］問道點數']=x.points;log('問道挑戰勝利，點數＋'+q+'，連勝 '+x.streak+'。');}else{x.streak=0;log('問道挑戰失敗，可再次挑戰。');}S.hp=r.saved.hp;S.mp=r.saved.mp;battle=null;closeModal();R.save();render();setTimeout(()=>W.openWendao(),0);};
const open=W.openWendao;W.openWendao=function(){const out=open.apply(this,arguments);for(const el of document.querySelectorAll('#modalBody button,#modalBody p')){if(el.textContent.includes('跨境界戰'))el.textContent=el.textContent.replace('32點','64點').replace('32積分','64積分');}return out;};
const help=R511_CODEX.問道檯;if(help)R511_CODEX.問道檯=JSON.parse(JSON.stringify(help).replaceAll('跨境界戰為32積分','跨境界戰為64積分'));
const guide=R.beginWendaoGuide;R.beginWendaoGuide=function(){const before=battle,out=guide.apply(this,arguments),b=battle;if(b&&b!==before&&b.jzWendao&&!!b.auto!==!!JZ1007.config().enterAuto)toggleAutoBattle();return out;};
if(N.releaseHistory073){N.releaseHistory073.改動.push('問道檯跨境界戰勝利基礎獎勵提高為64問道點數，沿用原有連勝加成。');N.releaseHistory073.BUG修復.push('問道檯逐步挑戰、境界相符戰及跨境界戰遵守進場自動戰鬥設定。');}
})();
