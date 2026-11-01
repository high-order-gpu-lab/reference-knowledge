import requests,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
rows=json.loads((R/'metadata/papers.json').read_text());out=[]
for x in rows:
 if not x['doi']:continue
 path=R/'metadata'/(x['id']+'-crossref.json')
 try:
  if path.exists():j=json.loads(path.read_text())
  else:
   rr=requests.get('https://api.crossref.org/works/'+x['doi'],headers={'User-Agent':'DG-local-review/1.0'},timeout=30);rr.raise_for_status();j=rr.json();path.write_text(json.dumps(j,ensure_ascii=False,indent=2));time.sleep(1.2)
  m=j['message'];print(x['id'],m.get('title'),m.get('published'),flush=True);out.append({'id':x['id'],'doi':x['doi'],'status':'verified','title':m.get('title'),'published':m.get('published'),'published-print':m.get('published-print'),'published-online':m.get('published-online')})
 except Exception as e:out.append({'id':x['id'],'doi':x['doi'],'status':'fetch-failed','error':str(e)});print(x['id'],str(e),flush=True)
(R/'metadata/doi_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
