from pathlib import Path
from lxml import html
import json,csv,shutil,hashlib,re
R=Path(__file__).resolve().parents[1]
# Consolidate successful repository records, preserving the pinned default-branch snapshots.
code=[json.loads(p.read_text())['record'] for p in sorted((R/'metadata').glob('*-repository.json'))]
(R/'metadata/code_manifest.json').write_text(json.dumps(code,ensure_ascii=False,indent=2))
# libCEED is a paper, rather than a manual.
for ext in ['pdf','txt']:
 src=R/'ref-paper/manuals'/('P20_libCEED.'+ext)
 if src.exists():shutil.copy2(src,R/('ref-paper/fulltext' if ext=='pdf' else 'ref-paper/text')/src.name)
extra_doi={'P01':'10.1016/j.cpc.2025.109567','P07':'10.1177/10943420221100262','P11':'10.23919/ISC.2026.11520474','P14':'10.1016/j.compfluid.2015.07.016','P15':'10.1016/j.camwa.2020.05.004','P16':'10.1016/j.parco.2021.102841','P18':'10.1016/j.jcp.2019.04.010','P19':'10.1016/j.parco.2021.102831'}
rows=[]
for f in sorted((R/'metadata').glob('P*-abs.html')):
 k=f.name[:-9];d=html.fromstring(f.read_text());meta={e.get('name'):e.get('content') for e in d.xpath('//meta[starts-with(@name,"citation_")]')};authors=d.xpath('//meta[@name="citation_author"]/@content');hist=' '.join(' '.join(e.text_content().split()) for e in d.xpath('//*[contains(@class,"submission-history")]'))
 aid=meta.get('citation_arxiv_id');doi=meta.get('citation_doi') or extra_doi.get(k[:3],'');title=meta['citation_title'].replace(r'GAL{\AE}XI','GALÆXI');ver=re.findall(r'\[v(\d+)\]',hist)
 rec={'id':k,'title':title,'authors':authors,'date':meta['citation_date'].replace('/','-'),'doi':doi,'arxiv':aid,'arxiv_version':'v'+ver[-1] if ver else '', 'url':'https://arxiv.org/abs/'+aid,'scope':'foundation-outside-window' if k[:3] in ['P13','P14'] else '2016-10-28_to_2026-10-28','status':'fulltext','publication_status':'preprint copy; journal DOI separately recorded' if doi else 'preprint','local_pdf':'ref-paper/fulltext/'+k+'.pdf','local_text':'ref-paper/text/'+k+'.txt','submission_history':hist}
 rows.append(rec)
# Repository original manuscript and DOI verified metadata-only items.
for k in ['P20_libCEED','P21_HiFiLES','P22_GiMMiK','P23_Kokkos','P24_Portability','P25_Kokkos3']:
 if k=='P20_libCEED':j=json.loads((R/'metadata/verified-search-4.json').read_text())['message']['items'][0]
 else:j=json.loads((R/'metadata'/(k+'-crossref.json')).read_text())['message']
 authors=[' '.join([a.get('given',''),a.get('family','')]).strip() for a in j.get('author',[])];date='-'.join(map(str,j.get('published',{}).get('date-parts',[[0]])[0]));pdf=R/'ref-paper/fulltext'/(k+'.pdf')
 rows.append({'id':k,'title':j['title'][0],'authors':authors,'date':date,'doi':j['DOI'],'arxiv':'','arxiv_version':'','url':'https://doi.org/'+j['DOI'],'scope':'foundation-outside-window' if k[:3] in ['P21','P22'] else '2016-10-28_to_2026-10-28','status':'fulltext' if pdf.exists() else ('repository-manuscript-source' if k=='P21_HiFiLES' else 'metadata-only'),'publication_status':'published','local_pdf':str(pdf.relative_to(R)) if pdf.exists() else '', 'local_text':'ref-paper/text/'+k+'.txt' if pdf.exists() else '', 'source_manuscript':'ref-code/HiFiLES/doc/AIAApaper/aiaa_atlanta_2014/main.tex' if k=='P21_HiFiLES' else ''})
rows.sort(key=lambda x:x['id'])
(R/'metadata/papers.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
with (R/'ref-paper/文献目录.csv').open('w',encoding='utf-8-sig',newline='') as f:
 fields=['id','title','date','doi','arxiv','arxiv_version','scope','status','url','local_pdf'];w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
bib=[];ris=[]
for r in rows:
 typ='article' if r['doi'] else 'misc';auth=' and '.join(r['authors']);year=r['date'][:4];key=r['id']
 fields={'title':'{'+r['title']+'}','author':auth,'year':year,'doi':r['doi'],'url':r['url'],'note':'Local evidence: '+r['status']+'; preprint date shown where applicable'}
 bib.append('@'+typ+'{'+key+',\n'+',\n'.join('  '+k+' = {'+v.replace('%',r'\%')+'}' for k,v in fields.items() if v)+'\n}')
 ris.append('\n'.join(['TY  - JOUR','ID  - '+key,'TI  - '+r['title']]+['AU  - '+a for a in r['authors']]+['PY  - '+year,'DO  - '+r['doi'],'UR  - '+r['url'],'N1  - Evidence: '+r['status'],'ER  - ']))
(R/'ref-paper/references.bib').write_text('\n\n'.join(bib)+'\n');(R/'ref-paper/references.ris').write_text('\n\n'.join(ris)+'\n')
print('repositories',len(code),'papers',len(rows),'full PDFs',sum(x['status']=='fulltext' for x in rows))
