from pathlib import Path
import requests,json,concurrent.futures,time
R=Path(__file__).resolve().parents[1]
queries=['PyFR GPU performance','GALÆXI GPU discontinuous Galerkin','HORSES3D GPU','HiFiLES GPU','MFEM GPU high order finite element','matrix free high order GPU finite element','GiMMiK GPU','libCEED GPU','Discontinuous Galerkin Methods for Solving Elliptic and Parabolic Equations','GPU discontinuous Galerkin implicit solver']
def run(q):
 try:
  r=requests.get('https://api.crossref.org/works',params={'query':q,'rows':10,'filter':'from-pub-date:2016-10-28,until-pub-date:2026-10-28'},timeout=60);r.raise_for_status();j=r.json();(R/'metadata'/('crossref-'+str(queries.index(q))+'.json')).write_text(json.dumps(j,ensure_ascii=False,indent=2))
  return q,[{'title':x.get('title',[''])[0],'doi':x.get('DOI'),'year':x.get('published',{}).get('date-parts'),'link':x.get('link',[])} for x in j['message']['items']]
 except Exception as e:return q,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 out=dict(ex.map(run,queries))
(R/'metadata/discovery.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
for q,a in out.items():
 print('\nQUERY',q)
 for x in a if isinstance(a,list) else []:print(x['year'],x['doi'],x['title'])
for q in ['HORSES3D GPU','horses gpu']:
 r=requests.get('https://api.github.com/search/repositories',params={'q':q},timeout=30);j=r.json();(R/'metadata'/('github-search-'+q.replace(' ','-')+'.json')).write_text(json.dumps(j,indent=2));print('GITHUB',q,[(x['full_name'],x['description']) for x in j.get('items',[])][:10])
