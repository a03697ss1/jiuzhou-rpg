(function(){'use strict';if(!window.JZ073_OFFICIAL)return;const N=JZ073,R=JZR,E=N.esc,ROOT='https://a03697ss1.github.io/jiuzhou-rpg/';
N.phase=JZ072.phase='正式版';N.masterPromoted=JZ072.masterPromoted=JZR.masterPromoted=JZW.masterPromoted=JZV2.promoted=true;N.acceptedAt='2026-10-19';
N.version=JZ072.version=JZV2.version=R.version=JZW.version='0.7.3';
for(const [ob,key] of [[R,'ensure'],[JZ071,'ensure'],[N,'ensure']]){const old=ob[key];ob[key]=function(){const out=old.apply(this,arguments);if(S)S.version='V0.7.3';return out;};}
const initial=initialState;initialState=function(){const s=initial.apply(this,arguments);s.version='V0.7.3';return s;};
N.releaseHistory073={version:'0.7.3',date:'2026-10-19',新增:[
 '雷鳴沼地下深窟、黑潮禁岸、新妖物與災獸長右雙階段BOSS戰；長右專屬血條及水／水雷立繪。',
 '東州A／B主線分支、兩條後續支線與新增委託；兩條分支各自保留經歷、道具與隱藏紀錄。',
 '燐火狼、硬黑蠍、靈珠蝶加入寵物養成；神秘妖物蛋25種選擇、6遊戲小時孵化。',
 '完整圖片圖鑑、地區／類型／階級篩選、搜尋、取得來源與技能說明；裝備與物品圖片。',
 '問道檯跨境界對手生成，依境界、品質、流派、靈根與合法裝備功法生成。',
 '背包容量、固定格與每次增加3格的背包擴充格；功法、煉金爐、鑄造檯固定格。',
 '郵箱、7遊戲日信件期限、重要道具保管與既有角色先驅者感謝信；抽獎卷、改名卡與靈幣圖片。'],
 改動:[
 '戰鬥修為與靈幣採新表；依各出戰單位自身境界計算。高出敵方11層以上不獲修為。',
 '歷練表面100、額外保留20；投入整10點提高突破／破境成功率。任務、委託、戰鬥、探索、採集、品茗、好感與升星分別累積。',
 '每種紀念品首次取得歷練＋1，月玉珮首次＋5；目前持有與已領取紀錄可確認的紀念品補發一次。',
 '問道裝備、五種戰中丹藥、寵物材料與道具說明更新；特殊物品及自選箱禁止出售。',
 '玩家與永久夥伴裝備介面顯示圖片及數值；突破顯示提升前後與差額；可結婚夥伴使用各自背景。',
 '0.7.0、0.7.1、0.7.2另存歷史入口，各自使用存檔副本，保留原版本與規則。'],
 BUG修復:[
 '修正主線三隻青臭蟲、後續主線與一般戰鬥敵方倒地後無法結束的問題。',
 '修正BOSS勝利時玩家倒地後仍為0氣血；勝利退出後至少1氣血，可至醫館治療。',
 '修正長右第二階段立繪、血條與屬性切換；護盾值會隨承傷更新。',
 '修正圖鑑中文搜尋、切換條目捲動回頂、幫助清單回彈與日誌遮擋。',
 '修正月玉珮合成漏查紀念品欄；品茗歷練上限誤用角色總歷練；多敵歷練漏算。',
 '修正寵物丹藥配方、特殊功法分類、NPC位置、任務入口、裝備來源與物品敘述。',
 '修正未開箱道具進入戰鬥背包、浮點百分比文字及突破數值預覽；築基圓滿停止突破至尚未開放的金丹。']};
N.versions073=()=>showModal('歷史版本','<p>目前正式版：0.7.3。舊版各自保留，使用各自存檔副本，避免舊版本覆寫新版進度。</p>'+['0.7.0','0.7.1','0.7.2'].map(v=>'<p><a href="'+ROOT+'versions/'+v+'/" target="_blank" rel="noopener">開啟 '+v+' 保留版</a></p>').join(''));
JZ072.versionHistory=()=>showModal('版本更新・0.7.3','<h2>V0.7.3 · 2026-10-19</h2>'+['新增','改動','BUG修復'].map(k=>'<section class="card" data-release-kind="'+k+'"><h3>'+k+'</h3><ul>'+N.releaseHistory073[k].map(t=>'<li>'+E(t)+'</li>').join('')+'</ul></section>').join('')+'<p>抽獎功能與金丹修行尚未開放；抽獎卷請先保留。音樂暫不實裝。</p><button onclick="JZ073.versions073()">0.7.0／0.7.1／0.7.2 保留版</button>');
N.paintOfficial073=()=>{document.title='九州修仙錄 0.7.3';for(const e of document.querySelectorAll('.brand'))e.textContent='九州修仙錄 V0.7.3';const stamp=document.getElementById('jz073-start-version');if(stamp)stamp.textContent='V0.7.3 正式版';for(const e of document.querySelectorAll('#start .muted.small'))if(/0\.7\.[23]/.test(e.textContent))e.textContent='正式版 0.7.3';for(const banner of document.querySelectorAll('.jz073-banner')){if(banner.firstChild?.nodeType===3)banner.firstChild.nodeValue='V0.7.3 正式版 ';banner.querySelectorAll('.jz18-build').forEach(e=>e.remove());if(!banner.querySelector('[data-release-history]'))banner.insertAdjacentHTML('beforeend','<button data-release-history onclick="JZ072.versionHistory()">更新內容</button><button data-release-history onclick="JZ073.versions073()">歷史版本</button>');}};
const decorate=N.decorate;N.decorate=function(){const out=decorate.apply(this,arguments);N.paintOfficial073();return out;};
// Continue the existing 0.7.3 namespace. Only copy the old automatic save if
// that namespace is empty; never overwrite a test save or an old manual slot.
const auto=r4SaveKey('auto');if(!localStorage.getItem(auto)){const raw=window.JZ073_ORIGINAL_STORAGE?.read(auto);if(raw){try{N.saveRecovery.parse(raw);N.saveRecovery.keep(raw,'升級0.7.3前的原版自動存檔','official-upgrade');localStorage.setItem(auto,raw);}catch{}}}
if(localStorage.getItem(auto)){const button=document.getElementById('continueBtn');if(button)button.style.display='inline-block';}
const recovery=N.saveRecovery.view;N.saveRecovery.view=function(){return recovery.apply(this,arguments).replace('測試版與原版分開存檔。','0.7.3會延續先前測試進度；原版紀錄仍保留。').replaceAll('測試版自動存檔','0.7.3自動存檔');};
N.paintOfficial073();
})();
