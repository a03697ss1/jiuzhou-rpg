from pathlib import Path
import os,sys,json,subprocess,shutil,re,hashlib,datetime
P=Path(__file__).resolve().parent;ROOT=P.parents[1];O=ROOT/'V0.7.3_獨立測試_2026-10-17';REPO=ROOT/'github-release';W=O/'GitHub測試發布';PREFIX='preview/v0.7.3';DEST=W/PREFIX
G='C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe'
URL='https://a03697ss1.github.io/jiuzhou-rpg/preview/v0.7.3/'
ENV={**os.environ,'GIT_TERMINAL_PROMPT':'0','GCM_INTERACTIVE':'Never'}
def git(root,*args):
 p=subprocess.run([G,'-c','safe.directory='+root.as_posix(),'-C',str(root),*args],capture_output=True,text=True,encoding='utf8',env=ENV)
 if p.returncode:raise RuntimeError((p.stderr or p.stdout).strip()[:1500])
 return p.stdout.strip()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prepare():
 if not W.exists():
  git(REPO,'fetch','origin','main')
  git(REPO,'worktree','add','-b','publish/v0.7.3-preview-20261017',str(W),'origin/main')
 DEST.mkdir(parents=True,exist_ok=True)
 text=(P/'preview.html').read_text('utf8').replace('/github-release/assets/','../../assets/').replace('/新增美術_2026-10-16/','new-assets/')
 text+='<script>window.JZ073_BUILD_ID="20261017-ab-npc-preview-2";</script>'
 (DEST/'index.html').write_text(text,'utf8')
 (DEST/'new-assets').mkdir(exist_ok=True)
 for f in (ROOT/'新增美術_2026-10-16').glob('*.png'):
  if f.name in text:shutil.copy2(f,DEST/'new-assets'/f.name)
 source=DEST/'test-source/v073';source.mkdir(parents=True,exist_ok=True)
 for f in (O/'Git測試分支/test-source/v073').iterdir():
  if f.is_file():shutil.copy2(f,source/f.name)
 pages=['閱讀我_先看這裡.html','逐項施工工程覆蓋表.html','BUG修復與待補清單.html','完整測試及驗收報告.html']
 images=set()
 for name in pages:
  html=(O/name).read_text('utf8').replace('Git測試分支/test-source/','test-source/').replace('九州修仙錄_V0.7.3_獨立測試版.html','index.html')
  (DEST/name).write_text(html,'utf8')
  images.update(re.findall(r'<img[^>]+src="([^"#]+)"',html))
 for f in O.glob('*.json'):
  if f.stat().st_size>=85*1024*1024:raise ValueError('Oversize report '+f.name)
  shutil.copy2(f,DEST/f.name)
 for name in images:
  if not (O/name).is_file():raise ValueError('Missing report image '+name)
  shutil.copy2(O/name,DEST/name)
 for name in ['閱讀我_先看這裡.txt','A線完整對話709節點.txt','B線完整對話805節點.txt']:
  shutil.copy2(O/name,DEST/name)
 print(json.dumps({'prepared':True,'url':URL,'indexSha256':digest(DEST/'index.html'),'files':sum(1 for f in DEST.rglob('*') if f.is_file())},ensure_ascii=False))
def publish():
 git(W,'add','--',PREFIX)
 changes=[x for x in git(W,'diff','--cached','--name-only','-z').split('\0') if x]
 if any(not name.startswith(PREFIX+'/') for name in changes):raise ValueError('Change outside preview')
 if changes:git(W,'commit','-m','Publish independent 0.7.3 A/B story and NPC preview')
 base=json.loads((P/'baseline.json').read_text('utf8'))['commit']
 files=[x for x in git(W,'diff','--name-only','-z',base,'HEAD').split('\0') if x]
 if not files or any(not name.startswith(PREFIX+'/') for name in files):raise ValueError('Publication must only add/update independent preview')
 git(W,'push','origin','HEAD:refs/heads/main')
 commit=git(W,'rev-parse','HEAD')
 prior=json.loads((O/'GitHub獨立測試部署紀錄.json').read_text('utf8')) if (O/'GitHub獨立測試部署紀錄.json').exists() else {}
 gameCommit=prior.get('gameCommit') if prior.get('indexSha256')==digest(DEST/'index.html') else commit
 record={'kind':'independent-preview','url':URL,'path':PREFIX,'branch':'main','gameCommit':gameCommit,'deploymentCommit':commit,'publishedAt':datetime.datetime.now().astimezone().isoformat(timespec='seconds'),'formalVersion':'0.7.2','formalEntryUnchanged':True,'changedOnlyPreview':True,'indexSha256':digest(DEST/'index.html')}
 (O/'GitHub獨立測試部署紀錄.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),'utf8')
 print(json.dumps(record,ensure_ascii=False))
if __name__=='__main__':
 if sys.argv[1:] == ['prepare']:prepare()
 elif sys.argv[1:] == ['publish']:publish()
 else:raise SystemExit('Use prepare or publish')
