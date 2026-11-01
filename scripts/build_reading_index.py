from pathlib import Path
import json,csv
R=Path(__file__).resolve().parents[1]
notes={
'P01':('重点核查全文的后端、布局、图执行和性能表','PyFR v2将后端、生成核、矩阵乘provider和图执行纳入共同架构；CPU/GPU共用上层算法。','优先读软件实现部分及PDF第17页表2–3。HIP-aware MPI与物理卡/GCD区别影响比较。'),
'P02':('重点核查全文的实现、显存和扩展章节','GALÆXI用CUDA Fortran迁移FLEXI的DGSEM，组织体/面运算、多stream和MPI。','PDF第12–14页给出PID、每DoF显存和扩展口径；显式结果不能外推隐式。'),
'P03':('重点核查全文的OpenACC实现、单卡和多卡章节','保留Fortran对象体系，单元gang/节点vector映射与局部累加是关键。','PDF第15–18页为TGV单卡/多卡；CRM另有规模测试。当前为2026预印本。'),
'P04':('核查摘要、软件范围及引用信息','提供HORSES3D算法与多物理背景，适合解释GPU版的来源。','主版论文不能替代GPU版功能验证；以独立GPU仓库限制说明为准。'),
'P05':('重点核查算子分解及架构章节','MFEM将网格、有限元空间、算子、线性求解与设备实现组织为可组合组件。','重点看部分组装和Operator；这是库框架，不是本项目完整流动求解器。'),
'P06':('重点核查全文的预条件设计和性能章节','高阶无矩阵作用与低阶细化组装预条件组合，实现setup及solve设备化。','PDF第16–17页用于区分高阶apply、LOR组装和AMG成本；不同PDE不可直接对比DG推进。'),
'P07':('重点核查内存管理及跨平台测试章节','MFEM、RAJA、Umpire分别承担算法、执行抽象和分配管理；临时缓冲复用与溢出控制影响显存。','PDF第11–13页关注181→97.3GB是12卡合计，以及节点对节点测试口径。'),
'P08':('已取得全文；核查摘要和方法入口','将固定拓扑节点移动的TMOP优化转成高阶有限元运算，用张量分解和PA减少数据移动。','与自适应后的几何维护有关，但不是误差驱动的DG p自适应实现。'),
'P09':('重点核查跨架构接口及版本边界','2026年工作用Fortran接口连接CUDA/HIP C++核，适合研究保留控制层并替换设备实现。','公开main快照仍为旧CUDA Fortran。文中部分网页访问日期写法存在歧义，不用它确定版本时间；采用arXiv提交记录。'),
'P10':('重点核查APU分区和扩展章节','研究MI300A上的DGSEM扩展与SPX/TPX/CPX分区，逻辑设备数会改变运行组织。','PDF第3–5页；512APU弱扩展90.4%，不是国产DCU实测。'),
'P11':('已取得全文；核查摘要及性能结论定位','研究MFEM关键核利用FP64 Tensor Core及融合，说明原生硬件特化可成为局部优化。','标题和摘要所述加速属于特定核与硬件，不把峰值/核加速写成所有求解器端到端结果。'),
'P12':('已取得全文；核查摘要与问题定义','针对H(div)鞍点问题设计矩阵自由GPU求解，使用块预条件、Schur近似和AMG。','可参考预条件组合方法，但方程与可压缩NS不同，不能直接采用其迭代性质。'),
'P13':('历史基础全文；核查摘要与架构背景','PyFR早期FR框架与流式架构设计，帮助理解其后端思想的来源。','发表于2014年，明确在近十年时间窗之外。实现细节以当前源码和P01为主。'),
'P14':('历史基础全文；核查摘要与框架背景','讨论PyFR混合非结构网格及异构执行。','发表于2015年；用于方法背景，不混入当前设备性能。'),
'P15':('核查软件流程与方法背景','FLEXI给出DGSEM、物理/网格处理及软件体系，作为GALÆXI算法母体。','期刊卷期2021；DOI含2020并不等于卷期年份。GPU数据看P02/P09/P10。'),
'P16':('核查GPU算法与后端章节','讨论高阶离散的GPU核、张量/批量代数和CEED生态的实现经验。','适合作为核设计综述；不同应用的性能不能拼成一个统一速度比。'),
'P17':('核查摘要及综述范围','覆盖高阶离散协同设计、无矩阵求解、网格与应用，为知识库提供系统阅读线索。','用于方法分类和追踪参考文献，不作为某个本地框架已具备功能的证明。'),
'P18':('核查摘要、目录和GPU/求解器章节入口','不可压缩NS半隐式DG；非线性显式、Stokes隐式，压力CG配GPU多重网格并使用经验roofline。','与隐式GPU的求解链有直接关联，但压力投影问题不等同于可压缩NS整体雅可比。'),
'P19':('核查摘要及架构接口讨论','PETSc强调应用编程模型和库内部编程模型可以不同，支持组合求解器和多GPU路线。','为可移植抽象层与第三方求解库互操作提供参考；具体当前能力需要选定版本确认。'),
'P20':('核查软件论文全文','libCEED提供元素离散算子的代数接口、运行时后端选择与JIT，适合嵌入现有软件。','参考restriction、basis、QFunction等职责；不是要求将HyRES整体替换为libCEED。'),
'P21':('作者仓库源稿与Crossref元数据；无单独正式PDF','HiFiLES原作者稿提供ESFR/FR、显式推进、CUDA并行及验证内容。','2014年历史例外；README的扩展声明条件不全，禁止作为严格横向性能基准。'),
'P22':('仅元数据核验；全文下载403','GiMMiK主题是为加速器生成特制矩阵乘核，当前PyFR provider为其使用方式提供源码证据。','发表于2016年5月，早于窗口起点。没有把未下载论文中的具体性能写入报告。'),
'P23':('仅元数据核验','Kokkos生态系统综述，作为执行模型/工具生态的阅读入口。','未取得全文，不给出其性能数字；当前接口学习使用官方手册快照。'),
'P24':('仅元数据核验','直接相关的五种共享内存模型在高阶非结构CFD中的可移植性比较研究。','全文尚缺，不转引其他论文对它的速度结论。列为优先补全文资料。'),
'P25':('仅元数据核验；IEEE下载418','Kokkos 3编程模型扩展文献，补充跨平台执行与数据模型背景。','未取得全文，不据此声称某GPU/DCU性能或支持范围。')}
rows=json.loads((R/'metadata/papers.json').read_text())
ver={x['id']:x for x in json.loads((R/'metadata/doi_verification.json').read_text())}
lines=['# 文献索引与阅读摘要','','时间窗：2016-10-28—2026-10-28。25条去重论文中，21条属于窗口内、4条为显式标记的历史基础例外。20篇本地PDF、1份作者仓库论文源稿、4条仅元数据记录。','', '“有全文”与“逐页精读”分开：下列逐条记录实际核查范围。报告主要结论来自重点核查的章节和对应源码；其余论文作为后续阅读资料，不虚构精读结果。','', '日期栏将首次预印本日期与正式出版日期分列；RIS/BibTeX优先使用Crossref正式出版元数据，保留arXiv版本。','']
def local_reference(r):
 if r.get('local_pdf'): return r['local_pdf'].replace('ref-paper/','')
 if r.get('source_manuscript'): return '../'+r['source_manuscript']
 return '../metadata/'+r['id']+'-crossref.json'

for r in rows:
 v=ver.get(r['id'],{});pub=v.get('published',{}).get('date-parts',[[]])[0];r['publication_date']='-'.join(map(str,pub));r['reading_scope'],r['summary'],r['boundary']=notes[r['id'][:3]]
 lines+=['## '+r['id']+' · '+r['title'],'', '- 作者：'+'; '.join(r['authors'])+f'\n- 首次预印本/原记录日期：{r["date"]}；正式出版日期：{r["publication_date"] or "未确认正式出版，按预印本归档"}。', '- 来源标识：'+(r["doi"] or r["arxiv"])+'；[本地资料]('+local_reference(r)+')','- 时间窗：'+r['scope']+'；资料状态：'+r['status']+'。']
 if r['local_pdf']:lines+=['- [本地PDF]('+r['local_pdf'].replace('ref-paper/','')+')；[可搜索文本]('+r['local_text'].replace('ref-paper/','')+')。']
 elif r.get('source_manuscript'):lines+=['- [作者仓库论文源稿](../'+r['source_manuscript']+')。']
 lines+=['- 实际阅读范围：'+r['reading_scope']+'。','',r['summary'],'',r['boundary'],'']
(R/'metadata/papers.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
(R/'ref-paper/文献索引与阅读摘要.md').write_text('\n'.join(lines))
# Export verified published metadata, while keeping preprint-only items as misc.
bib=[];ris=[]
for r in rows:
 cp=R/'metadata'/(r['id']+'-crossref.json');j=json.loads(cp.read_text())['message'] if cp.exists() else {}
 authors=[' '.join([a.get('given',''),a.get('family','')]).strip() for a in j.get('author',[])] or r['authors']
 title=(j.get('title') or [r['title']])[0]
 if title.startswith(':'):title='HORSES3D'+title
 year=(r.get('publication_date') or r['date'])[:4]
 journal=(j.get('container-title') or [''])[0]
 flds={'title':'{'+title+'}','author':' and '.join(authors),'year':year,'journal':journal,'volume':j.get('volume',''),'number':j.get('issue',''),'pages':j.get('page',''),'doi':r['doi'],'url':r['url'],'eprint':r['arxiv'],'note':'Evidence: '+r['status']+'; local reading copy may be preprint '+r['arxiv_version']}
 bib.append('@'+('article' if j else 'misc')+'{'+r['id']+',\n'+',\n'.join('  '+k+' = {'+str(v).replace('%',r'\%')+'}' for k,v in flds.items() if v)+'\n}')
 ris.append('\n'.join(['TY  - '+('JOUR' if j else 'GEN'),'ID  - '+r['id'],'TI  - '+title]+['AU  - '+a for a in authors]+['PY  - '+year,'JO  - '+journal,'DO  - '+r['doi'],'UR  - '+r['url'],'N1  - '+r['status'],'ER  - ']))
(R/'ref-paper/references.bib').write_text('\n\n'.join(bib)+'\n');(R/'ref-paper/references.ris').write_text('\n\n'.join(ris)+'\n')
fields=['id','title','date','publication_date','doi','arxiv','arxiv_version','scope','status','reading_scope','url','local_pdf']
with (R/'ref-paper/文献目录.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
