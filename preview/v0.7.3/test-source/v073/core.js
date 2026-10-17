(function(){'use strict';
const N=window.JZ073={version:'0.7.3',baseline:'0.7.2',phase:'獨立測試・待玩家驗收',coverage:{},pending:[],art:JZ073_ART},U=JZ071,R=JZR;
N.state=()=>S?(S.v073??={schema:1,branch:null,known:[],dig:{count:0,nextAt:0},story:{},reports:[],treasure:{charges:2,lastDay:null}}):null;
N.now=()=>U.now();N.short=n=>U.short(n);N.esc=R.esc;N.clone=x=>structuredClone(x);N.keys=['maxhp','maxmp','atk','dao','def','daoDef','agi','hit'];
N.canonical=n=>String(n||'').replace(/^【[^】]+】/,'').replace(/^災獸/,'');
N.realmIndex=r=>JZ072.rank(r)*10+JZ072.level(r);N.realmFrom=i=>JZ072.realm(['練氣','築基','金丹','元嬰','化神','煉虛','合體','大乘'][Math.floor((i-1)/10)],(i-1)%10+1);
N.choose=(rows,rng=Math.random,weight=r=>r.weight??r[3]??1)=>{const total=rows.reduce((v,r)=>v+weight(r),0);let x=rng()*total;for(const row of rows){x-=weight(row);if(x<0)return row;}return rows.at(-1);};
N.note=(id,state,reason='')=>N.coverage[id]={state,reason};
N.notice=(title,text)=>showModal(title,'<p>'+N.esc(text)+'</p><button onclick="closeModal()">關閉</button>');
N.pending.push({id:'修為非一般種差10級',reason:'工作檔H2明列其他種級特殊結算待補；遇到此情況暫存該角色待結算紀錄，不以未定數值發放。'},
 {id:'部分主線逐字原稿',reason:'033B、034～036缺完整逐字對話；保留已提供事件骨架與測試入口，不宣稱逐字劇情完成。'},
 {id:'問道兩項抽選機率',reason:'主根分段55/30/12/3及武器偏好70/30待核。跨境生成器可做機制驗收；正式抽選入口保持待定鎖。'},
 {id:'素材提交分類',reason:'保留0.7.2現有合法提交集合；未擅自將原未分類素材加入泛用提交池。'},
 {id:'長右與新妖物數值',reason:'依工作檔候選八核與地圖門檻在測試版試算，須玩家實戰驗收；不寫入正式母檔。'});
N.ensure=()=>{if(!S)return;const s=N.state();S.version='V0.7.3 獨立測試';s.schema=1;};
const ensure=R.ensure;R.ensure=function(){const out=ensure.apply(this,arguments);N.ensure();return out;};
const initial=initialState;initialState=function(){const s=initial.apply(this,arguments);s.version='V0.7.3 獨立測試';return s;};
JZ072.phase=N.phase;JZ072.versionHistory=()=>showModal('版本更新','<h3>V0.7.3 獨立測試</h3><p>基於最新V0.7.2增量施工；等待玩家明確驗收，尚未更新正式母檔與GitHub。</p><h4>新增</h4><p>新地區、新妖物與技能、長右雙階段測試、新委託、圖片圖鑑及來源反查。</p><h4>改動</h4><p>修為V2.1、靈幣V1、任務引導與跳過、裝備比較、素材箱分類。</p><h4>BUG修復</h4><p>合成不扣能量、平民愛心、護盾反擊、前後排隨機選敵與品質顯示。</p><h4>待補與驗收</h4>'+N.pending.map(x=>'<p>'+N.esc(x.id)+'：'+N.esc(x.reason)+'</p>').join(''));
document.title='九州修仙錄 0.7.3 獨立測試';
N.randomTargets=(b,f,r,p,cap,rng=Math.random)=>{if(!r?.target?.startsWith('enemy')||!p.length)return p.slice(0,cap);const remain=[...p],out=[];for(let i=0;i<cap&&remain.length;i++){let q=remain;const taunt=JZ360.has(f,'嘲諷');if(!(taunt&&remain.includes(taunt.source))){const front=remain.filter(x=>String(x.slot||Object.entries(b.enemyFormation||{}).find(([,v])=>v===x)?.[0]||Object.entries(b.playerFormation||{}).find(([,v])=>v===x)?.[0]||'front1').startsWith('front')),back=remain.filter(x=>!front.includes(x));q=front.length&&back.length?(rng()<.6?front:back):remain;}const t=q[Math.floor(rng()*q.length)];out.push(t);remain.splice(remain.indexOf(t),1);}return out;};
N.note('L38','已實裝','獨立目錄、存檔前綴與受保護檔案雜湊；正式GitHub不動。');
})();
