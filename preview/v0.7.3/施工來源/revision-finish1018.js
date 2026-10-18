(function(){'use strict';const N=JZ073,E=N.esc;
N.itemArtAudit1018=()=>N.allItemNames1018().map(name=>({name,family:N.itemArtFamily1018(name),image:N.itemIcon(name),missing:!/^data:image\/png|\.png(?:$|\?)/.test(N.itemIcon(name))}));
N.remainingCodexImages1018=()=>N.itemArtAudit1018().filter(r=>r.missing);
N.note('L33','已實裝','沿用69張素材圖，新增71類共用物品PNG與8張全身人物PNG；個別物品映射與圖片用途逐項列於本輪圖片清單。');
N.pending=N.pending.filter(r=>!['圖鑑缺少原始來源欄位','素材原生來源'].includes(r.id));
const decorate=N.decorate;N.decorate=function(){const out=decorate.apply(this,arguments);for(const banner of document.querySelectorAll('.jz073-banner'))if(banner.firstChild?.nodeType===3)banner.firstChild.nodeValue='V0.7.3・10/18 逐項修正測試版・待玩家驗收 ';return out;};
const stamp=document.getElementById('jz073-start-version');if(stamp)stamp.textContent='V0.7.3 獨立測試版・10/18 逐項修正';
const previous=JZ072.versionHistory;JZ072.versionHistory=()=>showModal('版本更新','<h2>V0.7.3・10/18 逐項修正</h2><h3>新增</h3><p>圖鑑搜尋、分類與階級組合篩選；全區／東州分頁；飾品、藥水與丹藥分類；妖物技能詳情；物品成品圖片與主線戰鬥全身人物。</p><h3>改動</h3><p>地下深窟移到雷鳴沼旁；野外境界表放入東州地圖；圖鑑與幫助視窗加大，內容分格；幫助重新說明玩法並補問道檯；八種特殊狀態整合到幫助。</p><p>精晶礦靈與臂巨礦使用此次確認的掉落比例。素材來源顯示四捨五入後的實際單項機率。夥伴最多出戰3名，寵物最多2隻，全隊仍為4個戰位。</p><p>長右血條移至上方，數字放在血條內；第二階段顯示全畫面提示與水／雷屬性，替換風雨雷光效果。長右戰改為手動操作。</p><h3>BUG修復</h3><p>返回圖鑑保留捲動位置；幫助可捲到底；配方顯示成品而非材料圖片；修正淬體丹百分比小數誤差；新寵物初始技能改從合法技能庫隨機取得；修正A路線測試入口的舊任務追蹤衝突。</p><p>保留舊版存檔副本讀取與備份。正式入口與正式母檔仍維持原版，等待玩家驗收。</p><button onclick="JZ073.previousRevisionHistory1018()">查看先前更新</button>');N.previousRevisionHistory1018=previous;
})();
