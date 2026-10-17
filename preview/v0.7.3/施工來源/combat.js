(function(){'use strict';const N=JZ073,C=JZ360,P=JZP,W=JZW,V=JZV2,R=JZR;
N.stateDefs={灼熱:{icon:'🔥',status:'灼燒',cancel:'水'},潮濕:{icon:'💧',element:'雷',status:'冰凍'},纏身:{icon:'🌿',element:'火',status:'中毒'},泥身:{icon:'🟤',status:'遲緩'},風蝕:{icon:'🍃',status:'迷茫'},電能:{icon:'⚡',status:'麻痺'},光明:{icon:'☀️',element:'暗',status:'失明'},黑暗:{icon:'🌑',element:'光',status:'恐懼'}};
N.applyState=(b,a,t,name)=>{if(!N.stateDefs[name]||t.hp<=0)return false;(t.jz073States??={})[name]={source:a?.name};C.log(b,t.name+'獲得狀態「'+name+'」。');return true;};
N.consumeState=(b,t,name)=>{if(!t.jz073States?.[name])return false;delete t.jz073States[name];if(b)C.log(b,t.name+'的「'+name+'」已觸發並消失。');return true;};
N.preventStatus=(b,a,t,op)=>{if(t.jz073Boss&&['暈眩','麻痺','冰凍','睡眠','特殊睡眠','束縛','混亂','恐懼','魅惑'].includes(op.name)){C.log(b,'長右「災獸之體」免疫'+op.name+'。');return true;}return false;};
N.statusChance=(b,a,t,op,p)=>{if(N.preventStatus(b,a,t,op)||p===0)return 0;for(const [name,d] of Object.entries(N.stateDefs))if(t.jz073States?.[name]&&d.status===op.name){N.consumeState(b,t,name);return Math.min(1,p+.03);}return p;};
const adjust=W.damageAdjust;W.damageAdjust=function(a,t,n,kind,r,ctx,els=[]){n=adjust.apply(this,arguments)??n;for(const [name,d] of Object.entries(N.stateDefs)){if(!t.jz073States?.[name])continue;if(d.cancel&&els.includes(d.cancel))N.consumeState(battle,t,name);else if(d.element&&els.includes(d.element)){n*=1.03;N.consumeState(battle,t,name);}}return n;};
const create=(id,name,cost,cd,target,op,effect,learn)=>{const r=JZ072.rule(id,name,cost,cd,target,[{op}],effect,'一般新增');r.raw.learn=learn;r.jz073=true;JZMON_SKILLS.push(r);return r;};
const data=[
 ['M07301','洪水',25,3,'enemyAll','flood','全敵120%水屬性道術傷害；必定潮濕。','長右；高危種水屬性可學'],
 ['M07302','巨海渦流',28,5,'enemyAll','vortex','全敵每回合60%水道術，3回合；每次75%遲緩1回合。','長右專屬'],
 ['M07303','浪潮',32,4,'enemyAll','waves','全敵五段各30%水屬性道術傷害。','長右；高危種水屬性可學'],
 ['M07304','轟雷',26,3,'enemy3','thunder','隨機3個不重複目標各110%雷道術，75%麻痺1回合。','雷屬性高危種可學；長右第二階段'],
 ['M07305','潮閃引雷',0,4,'enemy1','wetThunder','180%雷道術，70%麻痺1回合；潮濕目標必中麻痺2回合，優先潮濕。','僅長右專屬'],
 ['M07306','災獸之體',0,0,'self','bossPassive','被動免疫任何硬控制。','僅長右專屬'],
 ['M07307','靈幣打擊',0,0,'enemy1','coinStrike','150%物理；每次施放扣怨靈100靈幣。','財寶怨靈專屬'],
 ['M07308','深淵爪',1,3,'enemy1','abyss','10%物理暗傷；必中沉默、恐懼1回合。','財寶怨靈專屬'],
 ['M07309','烈爪',9,2,'enemy1','fireClaw','100%物理火傷。','狼／狐／龍／熊／鳥／雀／鷹／雕／猴／猿／猩／虎／豹／獾／貓種；火屬限定'],
 ['M07310','餘火',12,4,'enemy1','ember','80%基礎灼燒2回合。','火屬性；需要特殊種'],
 ['M07311','夾擊',8,3,'enemy1','clamp','80%物理；75%束縛1回合。','甲蟲／蜈蚣／蠍／蟹／蝦種'],
 ['M07312','固態甲殼',18,4,'self','shell','自身守勢2回合；守勢失去後下一次傷害降低50%。','甲蟲／蜈蚣／蠍／龜／蟹／蝦／蟲種；需要特殊種'],
 ['M07313','破夢',19,3,'enemy1','dreamBreak','先判睡眠：睡眠130%道術並必中混亂1回合；否則30%。','全種族；需要特殊種'],
 ['M07314','蛇之舞',20,4,'self','snakeDance','迅捷2回合；免疫下一次任何傷害，一次消失。','蛇／蛟種；需要特殊種'],
 ['M07315','沉默粉',18,4,'enemy1','silencePowder','必中沉默2回合。','蝶／蟲種；需要特殊種'],
 ['M07316','玩泥巴',25,4,'self','mudPlay','清除自身全部增減益，再守勢、療癒2回合。','鯰魚／豬種；土屬性；需要特殊種'],
 ['M07317','毒襲',16,3,'enemy1','toxicStrike','110%物理；中毒目標傷害額外40%，優先中毒目標。','全種族；需要特殊種']
];
N.skillRows=data;for(const row of data)create(...row);
N.hit=(b,a,t,ratio,kind='magic',elements=[],extra={})=>{if(t.hp<=0)return 0;if(Math.random()>=C.hitChance(a,t,{element:elements})){C.event(b,{type:'miss',actor:a.name,target:t.name});return 0;}b.jz072DamageKind=kind;b.jzwCurrentElements=elements;const r={element:elements},critical=Math.random()<C.critChance(a,t),n=C.damageValue(a,t,{ratio,kind,...extra},r,{crit:critical});return C.hurt(b,a,t,n);};
N.bad=(b,a,t,name,turns,chance=1,sure=false)=>{const op={name,turns,hostile:true,chance,sure};const p=N.statusChance(b,a,t,op,C.effectChance(b,a,t,op));if(Math.random()>=p)return false;return C.add(b,a,t,{...op,jz073ChanceDone:true});};
N.buff=(b,a,t,name,turns,extra={})=>C.add(b,a,t,{name,turns,...extra});
const resolve=P.resolveOp;P.resolveOp=function(b,a,r,o,targets,ctx){if(!r.jz073)return resolve.apply(this,arguments);const op=o.op;
 for(const t of targets){if(t.hp<=0)continue;switch(op){
 case 'flood':N.hit(b,a,t,1.2,'magic',['水']);N.applyState(b,a,t,'潮濕');break;
 case 'vortex':(b.jz073Vortices??=[]).push({source:a,target:t,left:3,start:b.round||1});break;
 case 'waves':for(let i=0;i<5&&t.hp>0;i++)N.hit(b,a,t,.3,'magic',['水']);break;
 case 'thunder':N.hit(b,a,t,1.1,'magic',['雷']);N.bad(b,a,t,'麻痺',1,.75);break;
 case 'wetThunder':{const wet=!!t.jz073States?.潮濕;N.hit(b,a,t,1.8,'magic',['雷']);N.bad(b,a,t,'麻痺',wet?2:1,wet?1:.7,wet);break;}
 case 'bossPassive':break;
 case 'coinStrike':N.hit(b,a,t,1.5,'physical');break;
 case 'abyss':N.hit(b,a,t,.1,'physical',['暗']);N.bad(b,a,t,'沉默',1,1,true);N.bad(b,a,t,'恐懼',1,1,true);break;
 case 'fireClaw':N.hit(b,a,t,1,'physical',['火']);break;
 case 'ember':N.bad(b,a,t,'灼燒',2,.8);break;
 case 'clamp':N.hit(b,a,t,.8,'physical');N.bad(b,a,t,'束縛',1,.75);break;
 case 'shell':N.buff(b,a,a,'守勢',2);a.jz073Shell={active:true,guard:true};break;
 case 'dreamBreak':{const asleep=!!(C.has(t,'睡眠')||C.has(t,'特殊睡眠'));N.hit(b,a,t,asleep?1.3:.3);if(asleep)N.bad(b,a,t,'混亂',1,1,true);break;}
 case 'snakeDance':N.buff(b,a,a,'迅捷',2);a.jz073SnakeDodge=true;break;
 case 'silencePowder':N.bad(b,a,t,'沉默',2,1,true);break;
 case 'mudPlay':for(const st of C.allStates(a))C.remove(a,st.name);N.buff(b,a,a,'守勢',2);N.buff(b,a,a,'療癒',2);break;
 case 'toxicStrike':N.hit(b,a,t,C.has(t,'中毒')?1.54:1.1,'physical');break;
 default:if(N.petOp?.(b,a,r,o,targets,ctx))return true;return resolve.apply(this,arguments);
 }}return true;};
const beforeResolve=W.beforeResolve;W.beforeResolve=function(b,a,r){const out=beforeResolve.apply(this,arguments);if(r.name==='靈幣打擊'&&N.canonical(a.name)==='財寶怨靈')a.jz073Purse=Math.max(0,(a.jz073Purse??3000)-100);if(a.jz073Boss&&a.jz073Phase===2&&(r.name==='轟雷'||r.name==='洪水'))a.jz073PhaseActions=(a.jz073PhaseActions||0)+1;return out;};
const before=P.beforeDamage;P.beforeDamage=function(b,a,t,n,direct){n=before.apply(this,arguments)??n;if(t.jz073SnakeDodge&&n>0){delete t.jz073SnakeDodge;return 0;}if(t.jz073Shell?.active&&!C.has(t,'守勢')&&n>0){delete t.jz073Shell;n*=.5;}
 if(t.jz073Boss&&t.jz073Phase===1&&t.hp-n<(t.maxhp/2)){const absorb=C.has(t,'護盾')?.shield||0;n=Math.min(n,Math.max(0,t.hp-t.maxhp/2)+absorb);t.jz073Transition=true;}
 return N.petBeforeDamage?.(b,a,t,n,direct)??n;};
const event=P.damageEvent;P.damageEvent=function(b,a,t,old,direct){const out=event.apply(this,arguments);if(t.jz073Boss&&t.jz073Transition&&t.hp<=t.maxhp/2){delete t.jz073Transition;t.hp=t.maxhp/2;t.mp=t.maxmp;t.jz073Phase=2;t.element=t.attr='水／雷';t.jz073PhaseActions=0;t.skills=['洪水','巨海渦流','浪潮','轟雷','潮閃引雷','災獸之體'];C.init(t).cd={};C.log(b,'長右進入第二階段：暴雨雷電；靈力回滿，災獸仍維持同一條氣血。');b.jz073Storm=true;}
 N.petDamage?.(b,a,t,old,direct);return out;};
const rounds=W.roundEffects;W.roundEffects=function(b){const out=rounds.apply(this,arguments);for(const v of b.jz073Vortices||[])if(v.left>0&&v.target.hp>0){b.jz072DamageKind='magic';b.jzwCurrentElements=['水'];C.hurt(b,v.source,v.target,C.damageValue(v.source,v.target,{ratio:.6,kind:'magic',element:['水']},{element:['水']},{}),false);N.bad(b,v.source,v.target,'遲緩',1,.75);v.left--;}return out;};
const choose=JZ072.chooseRule;JZ072.chooseRule=function(b,f,choices,pref=[]){if(f.jz073Boss){const legal=choices.filter(r=>r.name!=='災獸之體');let name=f.jz073Phase===2?((f.jz073PhaseActions||0)===0?'轟雷':f.jz073PhaseActions===1?'洪水':b.playerTeam.some(t=>t.hp>0&&t.jz073States?.潮濕)?'潮閃引雷':null):null;const forced=legal.find(r=>r.name===name);return forced||legal[Math.floor(Math.random()*legal.length)]||C.basic;}return choose.apply(this,arguments);};
const auto=JZ072.autoTargets;JZ072.autoTargets=function(b,f,r){const pool=C.pool(b,f,r);if(r.name==='潮閃引雷'){const wet=pool.filter(t=>t.jz073States?.潮濕);return N.randomTargets(b,f,r,wet.length?wet:pool,1);}if(r.name==='毒襲'){const poisoned=pool.filter(t=>C.has(t,'中毒'));return N.randomTargets(b,f,r,poisoned.length?poisoned:pool,1);}if(r.target==='enemy3')return N.randomTargets(b,f,r,pool,Math.min(3,pool.length));return auto.apply(this,arguments);};
const restriction=V.skillRestriction;V.skillRestriction=function(f,r){const species=f.petRef?R.petData(f.petRef).species:N.canonical(f.name);if(['巨海渦流','潮閃引雷','災獸之體'].includes(r?.name)&&!f.jz073Boss)return '長右專屬技能';if(r?.name==='災獸之體')return '被動技能';return restriction.apply(this,arguments);};
const death=V.onDeath;V.onDeath=function(b){if(b.jz073PlotLoss)return;return death.apply(this,arguments);};
N.note('L16','已實裝','50%鎖血、同一敵人、回滿MP、第二階段前兩動、潮濕優先與硬控免疫。');N.note('L18','部分實裝','八種獨立狀態與消耗；洪水明確附加潮濕，其餘施加來源未定。');
})();

