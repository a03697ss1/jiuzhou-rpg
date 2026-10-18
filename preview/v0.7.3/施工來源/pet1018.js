(function(){'use strict';const N=JZ073,R=JZR,P=JZP,V=JZV2,C=JZ360;
const names=N.newPetSpecies,majors=['練氣','築基','金丹','元嬰','化神','煉虛','合體','大乘'],growth=[1.45,1.55,1.65,1.75,1.85,2],layers=[1,1.04,1.08,1.12,1.16,1.20,1.24,1.28,1.32,1.38];
N.petTierLegal=(species,tier)=>species==='靈珠蝶'?tier==='特殊種':names.includes(species)?['一般種','特殊種'].includes(tier):true;
const petError=R.petError;R.petError=function(p){const x=R.petData(p);if(!N.petTierLegal(x.species,x.tier))return '此物種未定案此種級';return petError.apply(this,arguments);};
const petStats=R.petStats;R.petStats=function(p){const f=petStats.apply(this,arguments);if(names.includes(R.petData(p).species))f.combatPower=JZMON.power(f);return f;};
Object.assign(V.spec.base.pet_system.special_breakthrough.core_map,{燐火狼:'氣血',硬黑蠍:'防＋道防',靈珠蝶:'道'});
const fixedLegal=V.isLegalSkill;V.isLegalSkill=function(p,n){const x=R.petData(p),r=C.byId[n]||C.byName[n],d=JZMON.byName[x.species];if(names.includes(x.species)&&r&&(d.skills.includes(r.name)||x.tier!=='一般種'&&d.specialSkills.includes(r.name)))return r.monster===true;return fixedLegal.apply(this,arguments);};
// Preserve formal recorded wild cores. Higher realms use the already adopted pet growth path.
const monster=P.monsterStats;P.monsterStats=function(name,major,layer,tier,raw=false){if(!names.includes(name))return monster.apply(this,arguments);major=major==='q'?'練氣':major==='z'?'築基':major;const rank=majors.indexOf(major);if(rank<0||!Number.isInteger(layer)||layer<1||layer>10)throw Error('未核定寵物境界');if(!N.petTierLegal(name,tier))throw Error('此物種未定案此種級');const f=JZMON.stats(name,'z',10,tier);if(rank<2){const base=N.petCores[name][major][layer],mult=name==='靈珠蝶'||tier==='一般種'?1:1.25;N.keys.forEach((k,i)=>f[k]=Math.round(base[i]*mult));}else{let scale=1;for(let i=2;i<=rank;i++)scale*=growth[i-2]*(i<rank?1.38:1);scale*=layers[layer-1];for(const k of N.keys)f[k]=raw?f[k]*scale:Math.round(f[k]*scale);}Object.assign(f,JZMON.hidden(major,tier,f.element.match(/[水火木土風雷光暗]/g)||[]));f.realm=JZ072.realm(major,layer);f.hp=f.maxhp;f.mp=f.maxmp;f.combatPower=JZMON.power(f);return f;};
// The official family and element restrictions apply to new species too, without the old closure's 19-species whitelist.
const skills=R.legalPetSkills;R.legalPetSkills=function(p){if(!names.includes(R.petData(p).species))return skills.apply(this,arguments);return [...new Map(Object.values(C.byId).filter(r=>r.monster&&V.isLegalSkill(p,r.id)).map(r=>[r.id,r])).values()];};
const allowed=JZ072.newSkillAllowed;JZ072.newSkillAllowed=function(p,r){const species=R.petData(p).species;if(species==='硬黑蠍'&&['反彈','鐵甲','護盾反擊'].includes(r.name))return r.name!=='護盾反擊'||R.petData(p).tier!=='一般種';return allowed.apply(this,arguments);};
const chooseAB=R.chooseAB;R.chooseAB=function(i){const pet=S.pets[i],x=pet&&R.petData(pet);if(!names.includes(x?.species))return chooseAB.apply(this,arguments);if(battle||!x.specialBreak||x.choice||V.dead(pet))return false;const options=R.newPetSkills.filter(r=>r.group==='五星二選一'&&r.species.includes(x.species));showModal('五星突破技能・二選一',options.map(d=>{const r=C.byId[d.id];return '<div class="card"><b>'+d.choice+' '+N.esc(d.name)+'</b><p>'+N.esc(d.effect)+'</p><p>MP'+r.cost+'／CD'+r.cd+'；占1格編招槽</p><button onclick="JZ072.choosePetAB('+i+',\''+d.id+'\')">選擇此技能</button></div>';}).join(''));return true;};
N.newPetGrowthAudit=()=>names.map(species=>({species,core:R.petCore[species],stars:[...R.starMultipliers],wildBase:N.monsterCores[species],petBase:N.petCores[species],missing:[],higherRealmFormula:'沿用101-jzp-20261005.js的築基圓滿基準、境界成長與層位倍率。'}));
N.pending=N.pending.filter(row=>row.id!=='新寵物全境界八核');
const describe=JZW.itemDescription;JZW.itemDescription=function(n){return n==='［特殊］神秘妖物蛋'?'神秘的蛋，能孵出心中所想的妖物。25種妖物自選1，必定孵出所選物種；孵化6遊戲小時，僅抽取該物種合法種級。':describe.apply(this,arguments);};
N.note('L19','已實裝','已接入使用者補齊49列八核；保留11列野外值，沿用升星、突破與五星核心公式。');
N.note('L20','已實裝','保留已定三條10心任務、計數與技能；由正常孵化取得的新三寵可接取。');
N.note('L34','已實裝','25種神秘蛋選單全部開放；新三寵6遊戲小時孵化與合法種級。');
})();
