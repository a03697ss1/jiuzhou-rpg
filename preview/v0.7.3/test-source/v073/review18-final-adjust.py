from pathlib import Path
p=Path(__file__).with_name('review18-fixes.js');s=p.read_text('utf8')
s=s.replace("const itemUse=W.useItem;W.useItem=function(n){if(n===N.deletedItem18)","const itemUse=W.useItem;W.useItem=function(n){if(battle?.jzWendao&&battle.jzWendao.mode!=='tower')return itemUse.apply(this,arguments);if(n===N.deletedItem18)")
s=s.replace("if(N.potions18[n].resist||battle?.tutorialCase)","if(N.potions18[n].resist||N.potions18[n].clear||battle?.tutorialCase)")
p.write_text(s,'utf8')
