from pathlib import Path
import requests,json,tarfile,io,hashlib,concurrent.futures
R=Path(__file__).resolve().parents[1]
repos={'PyFR':'PyFR/PyFR','FLEXI':'flexi-framework/flexi','GALAEXI':'flexi-framework/galaexi','HORSES3D':'horses-framework/horses3d','HiFiLES':'HiFiLES/HiFiLES-solver','MFEM':'mfem/mfem'}
def fetch(item):
 name,repo=item
 try:
  r=requests.get('https://api.github.com/repos/'+repo,timeout=40);r.raise_for_status();meta=r.json()
  r=requests.get('https://api.github.com/repos/'+repo+'/commits/'+meta['default_branch'],timeout=40);r.raise_for_status();commit=r.json();sha=commit['sha']
  url=f'https://codeload.github.com/{repo}/tar.gz/{sha}';r=requests.get(url,timeout=180);r.raise_for_status();data=r.content
  out=R/'ref-code'/name;out.mkdir(exist_ok=True)
  with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as tf:
   for m in tf.getmembers():
    parts=m.name.split('/',1)
    if len(parts)<2 or not parts[1]:continue
    m.name=parts[1];tf.extract(m,out,filter='data')
  rec={'name':name,'repo':repo,'url':meta['html_url'],'branch':meta['default_branch'],'commit':sha,'commit_date':commit['commit']['committer']['date'],'license':meta.get('license'),'archive_url':url,'archive_sha256':hashlib.sha256(data).hexdigest(),'retrieved':'2026-10-28','bytes':len(data)}
  (R/'metadata'/f'{name}-repository.json').write_text(json.dumps({'record':rec,'repository':meta,'commit':commit},ensure_ascii=False,indent=2))
  print(name,sha,len(data),flush=True);return rec
 except Exception as e:print(name,'ERROR',str(e),flush=True);return {'name':name,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(fetch,repos.items()))
(R/'metadata/code_manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
