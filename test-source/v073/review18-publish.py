"""Publish the authorized October 18 completed pet cores only under preview/v0.7.3."""
from pathlib import Path
import sys, json, shutil, re, hashlib, datetime
from urllib.parse import unquote
import importlib.util

P = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('publisher', P/'publish-preview.py')
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
ROOT, W, PREFIX, DEST = old.ROOT, old.W, old.PREFIX, old.DEST
O = ROOT/'V0.7.3_18項修正_2026-10-18'
BUILD = '20261018-review18-1'
PAGES = ['閱讀我_先看這裡.html','逐項施工工程覆蓋表.html','BUG修復與待補清單.html','完整測試及驗收報告.html','素材圖片清單與預覽.html']
git, digest = old.git, old.digest

def prepare():
    changed=[n for n in git(W,'diff','--name-only','-z').split('\0') if n]
    untracked=[n for n in git(W,'ls-files','--others','--exclude-standard','-z').split('\0') if n]
    assert all(n.startswith(PREFIX+'/') for n in changed+untracked), 'Unexpected changes outside preview'
    head, remote = git(W,'rev-parse','HEAD'), git(W,'rev-parse','origin/main')
    if head != remote:
        git(W,'merge','--ff-only','origin/main')
    base = git(W,'rev-parse','HEAD')
    protected = {n:git(W,'rev-parse','HEAD:'+n) for n in ['index.html','定案規則_0.7.2.json']}
    text = (P/'preview.html').read_text('utf8')
    for a,b in [('/github-release/assets/','../../assets/'),('/新增美術_2026-10-16/','new-assets/'),('/素材美術_2026-10-18/','material-assets/'),('/物品美術_2026-10-18/','item-assets/'),('/人物全身_2026-10-18/','fullbody-assets/'),('/物品獨立美術_2026-10-18/','unique-item-assets/'),('10/18 本地補完','10/18 獨立測試補完')]:
        text = text.replace(a,b)
    text = text.replace('正式母檔、正式版本與GitHub發布內容維持施工前狀態。','正式母檔與正式入口維持0.7.2；本輪提供GitHub 0.7.3獨立測試頁。')
    text = text.replace('本地獨立測試補完','獨立測試補完').replace('正式母檔與GitHub未更新。','正式母檔與正式入口維持0.7.2；本輪已提供GitHub 0.7.3獨立測試頁。')
    text += '<script>window.JZ073_BUILD_ID='+json.dumps(BUILD)+';</script>'
    (DEST/'index.html').write_text(text,'utf8')
    for folder, target in [('新增美術_2026-10-16','new-assets'),('素材美術_2026-10-18','material-assets'),('物品美術_2026-10-18','item-assets'),('人物全身_2026-10-18','fullbody-assets'),('物品獨立美術_2026-10-18','unique-item-assets')]:
        (DEST/target).mkdir(exist_ok=True)
        for f in (ROOT/folder).glob('*.png'):
            if f.name in text: shutil.copy2(f,DEST/target/f.name)
    assert len(list((DEST/'material-assets').glob('*.png'))) == 69
    shutil.copytree(O/'施工來源', DEST/'施工來源',dirs_exist_ok=True)
    source=DEST/'test-source/v073'; source.mkdir(parents=True,exist_ok=True)
    for f in (old.O/'Git測試分支/test-source/v073').iterdir():
        if f.is_file(): shutil.copy2(f,source/f.name)
    replacements = [
        ('九州修仙錄_V0.7.3_獨立測試版.html','index.html'),
        ('../素材美術_2026-10-18/','material-assets/'),('../物品美術_2026-10-18/','item-assets/'),('../人物全身_2026-10-18/','fullbody-assets/'),('../物品獨立美術_2026-10-18/','unique-item-assets/'),
        ('正式母檔、正式版本及GitHub內容未更新','正式母檔與正式入口維持0.7.2；本輪提供GitHub 0.7.3獨立測試頁'),
        ('本輪未執行推送或發布','本輪僅發布preview/v0.7.3獨立測試頁，正式入口未改'),
        ('未發布GitHub','已提供GitHub獨立測試頁'),
        ('2026-10-18本地獨立測試補完','2026-10-18獨立測試補完'),
        ('（單檔，內嵌原圖與本輪素材圖）','（GitHub線上版，共用原圖與本輪素材圖）')]
    for name in PAGES:
        html=(O/name).read_text('utf8')
        for a,b in replacements: html=html.replace(a,b)
        (DEST/name).write_text(html,'utf8')
    for pattern in ['*.json','*.png']:
        for f in O.glob(pattern): shutil.copy2(f,DEST/f.name)
    broken=[]
    for name in PAGES:
        for ref in re.findall(r'(?:href|src)="([^"#]+)"',(DEST/name).read_text('utf8')):
            if not re.match(r'^(?:https?:|data:|mailto:)',ref):
                target=DEST/unquote(ref.split('#')[0].split('?')[0])
                if not target.is_file(): broken.append([name,ref])
    assert not broken, broken
    assert all(f.stat().st_size < 100*1024*1024 for f in DEST.rglob('*') if f.is_file())
    state={'base':base,'protectedBlobs':protected,'build':BUILD,'url':old.URL,'indexSha256':digest(DEST/'index.html'),'materialImages':69,'documents':5,'sourceCommit':json.loads((O/'本地測試分支保存紀錄.json').read_text('utf8'))['commit']}
    (P/'review18-publish-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8')
    print(json.dumps(state,ensure_ascii=False))

def publish():
    state=json.loads((P/'review18-publish-state.json').read_text('utf8'))
    git(W,'add','--',PREFIX)
    changed=[x for x in git(W,'diff','--cached','--name-only','-z').split('\0') if x]
    assert changed and all(x.startswith(PREFIX+'/') for x in changed)
    assert digest(DEST/'index.html') == state['indexSha256']
    git(W,'commit','-m','Publish 18 gameplay review fixes and independent item art to 0.7.3 preview')
    changed=[x for x in git(W,'diff','--name-only','-z',state['base'],'HEAD').split('\0') if x]
    assert all(x.startswith(PREFIX+'/') for x in changed)
    for n,blob in state['protectedBlobs'].items(): assert git(W,'rev-parse','HEAD:'+n)==blob
    git(W,'push','origin','HEAD:refs/heads/main')
    record={**state,'kind':'independent-preview','deploymentCommit':git(W,'rev-parse','HEAD'),'changedFiles':len(changed),'changedOnlyPreview':True,'formalEntryUnchanged':True,'formalVersion':'0.7.2','publishedAt':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='seconds')}
    (O/'GitHub獨立測試部署紀錄.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),'utf8')
    print(json.dumps(record,ensure_ascii=False))

if __name__=='__main__':
    {'prepare':prepare,'publish':publish}[sys.argv[1]]()
