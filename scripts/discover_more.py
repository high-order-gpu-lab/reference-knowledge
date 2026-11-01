from pathlib import Path
import requests,json,time
from lxml import etree
qs=['GiMMiK','FLEXI high order framework','GPU Algorithms Efficient Exascale Discretizations','libCEED Fast algebra high-order','HiFiLES high fidelity large eddy','A GPU accelerated discontinuous Galerkin incompressible flow solver','Discontinuous Galerkin Methods for Solving Elliptic and Parabolic Equations Riviere','Modern GPU Computing Numerical Methods Partial Differential Equations','Programming Massively Parallel Processors fourth edition','Nodal Discontinuous Galerkin Methods Hesthaven Warburton','Implementing Spectral Methods Partial Differential Equations Kopriva']
for i,q in enumerate(qs):
 try:
  r=requests.get('https://api.openalex.org/works',params={'search':q,'per-page':4},timeout=40);r.raise_for_status();j=r.json();Path('review/metadata/more-'+str(i)+'.json').write_text(json.dumps(j,ensure_ascii=False,indent=2))
  print('QUERY',q,flush=True)
  for a in j.get('results',[]):print(a.get('publication_year'),a['title'],a.get('doi'),[l.get('pdf_url') for l in a.get('locations',[]) if l.get('pdf_url')][:3],flush=True)
 except Exception as e:print(q,'ERROR',str(e),flush=True)
 time.sleep(.5)
