from pathlib import Path
p=Path(__file__).with_name('live-pet-entry1018.cjs');s=p.read_text('utf8')
s=s.replace('const pet=S.pets[0],x=JZR.petData(pet),f=JZR.petStats(pet);','const pet=S.pets.at(-1),x=JZR.petData(pet),f=JZR.petStats(pet);if(x.species!==species)throw Error("孵化物種不符 "+JSON.stringify({expected:species,actual:x.species}));')
p.write_text(s,'utf8')
