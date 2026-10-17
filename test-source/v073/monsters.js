(function(){'use strict';const N=JZ073,M=JZMON,U=JZ071,W=JZW,R=JZR;
N.monsters=[
 {name:'燐火狼',area:'黑潮禁岸',weight:33.3,special:60,element:'火',core:'氣血',bands:[['z',5,5,40],['z',6,8,40],['z',10,10,20]],skills:['揮擊','烈爪'],specialSkills:['餘火'],pet:true,drops:[['火尾毛',35],['硬獸骨',20],['獸牙',5],['利爪',30],['濃縮妖血',5],['妖丹',4],['妖魂碎片',1]]},
 {name:'硬黑蠍',area:'黑潮禁岸',weight:33.3,special:60,element:'土',core:'防／道防',bands:[['z',5,5,25],['z',7,7,25],['z',9,9,25],['z',10,10,25]],skills:['毒針','夾擊'],specialSkills:['固態甲殼'],pet:true,drops:[['黑蠍甲',90],['濃縮妖血',5],['妖丹',4],['妖魂碎片',1]]},
 {name:'靈珠蝶',area:'黑潮禁岸',weight:33.4,special:100,element:'木／風',core:'道',bands:[['z',5,5,50],['z',10,10,50]],skills:['飛速一擊','撲粉','破夢'],specialSkills:[],pet:true,drops:[['靈粉',25],['濃縮妖血',25],['妖丹',25],['妖魂碎片',25]]},
 {name:'財寶怨靈',area:'雷鳴沼地下深窟',weight:100,special:100,element:'暗',core:'氣血',bands:[['z',10,10,100]],skills:['靈幣打擊','深淵爪'],specialSkills:[],pet:false,drops:[]},
 {name:'長右',area:'雷鳴沼地下深窟',weight:0,special:100,element:'水',core:'道',bands:[['z',10,10,100]],skills:['洪水','巨海渦流','浪潮'],specialSkills:[],pet:false,questOnly:true,drops:[]}
];
N.monsterCores={
 燐火狼:{5:[585,159,47,38,33,31,39,38],6:[644,174,50,41,35,33,41,42],7:[702,189,55,44,38,36,44,45],8:[760,204,59,48,41,39,47,48],10:[878,234,67,54,47,45,54,54]},
 硬黑蠍:{5:[485,159,38,36,44,44,28,33],7:[582,189,44,42,51,51,32,39],9:[680,219,50,48,59,59,37,44],10:[728,234,54,51,63,63,39,47]},
 靈珠蝶:{5:[476,276,41,75,34,41,51,51],10:[715,406,59,106,49,59,71,71]},財寶怨靈:{10:[2600,390,75,79,69,69,56,69]},長右:{10:[4500,1200,115,180,80,90,48,70]}};
const stats=M.stats;M.stats=function(name,major,layer,tier='一般種'){const d=N.monsters.find(x=>x.name===N.canonical(name));if(!d)return stats.apply(this,arguments);name=d.name;const base=N.monsterCores[name][layer];if(!base)throw Error(name+'未定案境界：'+layer);if(['靈珠蝶','財寶怨靈'].includes(name)&&tier!=='特殊種')throw Error(name+'僅特殊種');if(name==='長右')tier='災獸種';const f={name,type:'monster',realm:JZ072.realm('築基',layer),tier,element:d.element,attr:d.element,status:[],jzCanonical:true,jz073New:true,skills:[...d.skills,...(tier==='特殊種'?d.specialSkills:[])],...(tier==='災獸種'?{}:M.hidden('築基',tier,d.element.match(/[火水木土風雷光暗]/g)||[]))};const mult=['靈珠蝶','財寶怨靈','長右'].includes(name)?1:tier==='特殊種'?1.25:1;N.keys.forEach((k,i)=>f[k]=Math.round(base[i]*mult));f.hp=f.maxhp;f.mp=f.maxmp;f.combatPower=name==='長右'?1957:M.power(f);if(name==='財寶怨靈')f.jz073Purse=3000;if(name==='長右'){f.jz073Boss=true;f.jz073Phase=1;f.jz073Kind='災獸種';f.skills.push('災獸之體');}return f;};
for(const d of N.monsters){d.jz073New=true;M.defs.push(d);M.byName[d.name]=d;if(d.name!=='長右')MONSTER_FOUR_LAYER_ART_8[d.name]=N.art[d.name];}
M.areas.黑潮禁岸=[500,950,Infinity];M.areas.雷鳴沼地下深窟=[1050,1400,Infinity];
N.generate=(name,rng=Math.random,options={})=>{const d=M.byName[name];if(!N.monsters.includes(d))return M.generate(name,rng,{ignoreCap:true,...options});const band=N.choose(d.bands,rng),layer=band[1]+Math.min(band[2]-band[1],Math.floor(rng()*(band[2]-band[1]+1))),tier=options.tier||((rng()*100<d.special)?'特殊種':'一般種');return M.stats(name,'z',layer,tier);};
const gen=M.generate;M.generate=function(name,rng=Math.random,opts={}){return N.monsters.some(x=>x.name===name)?N.generate(name,rng,opts):gen.apply(this,arguments);};
const enc=M.encounter;M.encounter=function(area){if(area==='黑潮禁岸')return N.generate(N.choose(N.monsters.filter(d=>d.area===area),Math.random).name);if(area==='雷鳴沼地下深窟')return N.generate('財寶怨靈');return enc.apply(this,arguments);};
const drops=W.rollDrops;W.rollDrops=function(f,rng=Math.random,budget=1+Math.floor(rng()*2)){const d=N.monsters.find(d=>d.name===N.canonical(f.name));if(!d)return drops.apply(this,arguments);if(!d.drops.length)return [];const out=[];for(let i=0;i<budget;i++){const short=N.choose(d.drops,rng,x=>x[1])[0],name=U.materialCatalog.find(n=>U.short(n)===short);if(!name){N.state().reports.push({kind:'掉落缺正式素材',name:short});continue;}const row=out.find(x=>x.name===name);if(row)row.qty++;else out.push({name,qty:1});}return out;};
JZ072.mysteryEggSpecies=[...new Set([...JZ072.mysteryEggSpecies,'燐火狼','硬黑蠍','靈珠蝶'])];
JZV2.family.燐火狼='狼';JZV2.family.硬黑蠍='蠍';JZV2.family.靈珠蝶='蝶';
for(const d of N.monsters.filter(d=>d.pet)){if(!R.petSpecies.includes(d.name))R.petSpecies.push(d.name);R.petCore[d.name]=d.name==='燐火狼'?'maxhp':d.name==='硬黑蠍'?'dualdef':'dao';}
const egg=U.eggTier;U.eggTier=function(species,rng=Math.random){if(species==='靈珠蝶')return '特殊種';if(['燐火狼','硬黑蠍'].includes(species))return rng()*85<50?'一般種':'特殊種';return egg.apply(this,arguments);};
N.note('L15','已實裝','五隻新妖物、候選八核、合法種級與境界、立繪；須玩家驗收平衡。');N.note('L29','已實裝','財寶怨靈每次靈幣打擊才減100，最低0。');N.note('L34','已實裝','神秘蛋新增三種；新種級受合法範圍限制。');
})();



