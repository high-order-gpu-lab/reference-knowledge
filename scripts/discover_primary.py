import requests,json,concurrent.futures
from pathlib import Path
from lxml import html
R=Path('review/metadata')
urls={'pyfr-home':'https://www.pyfr.org/','mfem-pubs':'https://mfem.org/publications/','nrgi-pubs':'https://numericsresearchgroup.org/publications.html','arxiv-galaexi':'https://export.arxiv.org/api/query?search_query=all:galaexi&max_results=5','arxiv-horses':'https://export.arxiv.org/api/query?search_query=all:horses3d&max_results=10','openalex-pyfr':'https://api.openalex.org/works?search=PyFR&per-page=15','openalex-horses':'https://api.openalex.org/works?search=HORSES3D%20GPU&per-page=10','openalex-galaexi':'https://api.openalex.org/works?search=GAL%C3%86XI&per-page=10'}
def fetch(item):
 k,u=item
 try:
  r=requests.get(u,timeout=55);r.raise_for_status();(R/(k+'.raw')).write_text(r.text)
  if k.startswith('openalex'):
   return k,[(a['title'],a['doi'],a['publication_year'],a.get('open_access'),a.get('best_oa_location')) for a in r.json().get('results',[])][:15]
  if k.startswith('arxiv'):return k,r.text[:18000]
  doc=html.fromstring(r.content);links=[(a.text_content().strip(),a.get('href')) for a in doc.xpath('//a[@href]')]
  (R/(k+'-links.json')).write_text(json.dumps(links,ensure_ascii=False,indent=2));return k,[a for a in links if any(s in (a[0]+' '+a[1]).lower() for s in ['arxiv','pyfr','gala','public','gpu','ceed','high-order'])][:60]
 except Exception as e:return k,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for k,v in ex.map(fetch,urls.items()):print(k,json.dumps(v,ensure_ascii=False))
