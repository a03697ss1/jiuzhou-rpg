(function(){'use strict';const N=JZ073;
// Main-quest settlement already advanced the quest, but left its battle modal open.
// Only remove the obsolete battle screen after settlement has detached that battle.
// Preserve any replacement dialogue, result window, and the plot-defeat Continue step.
const finish=N.finishStoryBattle;N.finishStoryBattle=function(b){const out=finish.apply(this,arguments);if(b?.jz073Story&&battle!==b&&document.querySelector('#modalBody .bmv1-canvas'))closeModal();if(b?.jz073Story&&battle!==b){document.getElementById('modalBack')?.classList.remove('bmv1-active','battle-locked');}return out;};
})();
