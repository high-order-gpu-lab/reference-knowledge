from pathlib import Path
import csv,json
R=Path(__file__).resolve().parents[1]
rows=[
['E01','PyFR v2.0.3','P01','PDF p17 Tables 2–3','FP64; TGV; 13,891,500 tetrahedra; p=7','MI250X/Frontier; 2 GCD per card','2048 ranks / 1024 cards','16 ranks / 8 cards','strong scaling efficiency','0.46','ratio','HIP-aware MPI disabled','published-table','not single-card baseline'],
['E02','PyFR v2.0.3','P01','PDF p17 Tables 2–3','same as E01','GH200/Alps','2048 ranks / 2048 GPUs','16 ranks / 16 GPUs','strong scaling efficiency','0.47','ratio','CUDA-aware MPI enabled','published-table','hardware differs from E01'],
['E03','GALAEXI','P02','PDF p12–13 Table 2','explicit Navier–Stokes; polynomial degree 7','A100; 40 GiB','1 GPU','none','device memory per spatial DoF','0.869','KiB/spatial-DoF','all solution variables included in memory; denominator spatial nodes','published-table','not implicit-solver capacity'],
['E04','GALAEXI','P02','PDF p12 section 4.3','same as E03','A100; 40 GiB','1 GPU','none','capacity reported','48000000','spatial-DoF','per solution variable','published-text','rounded example; not 48M total scalar unknowns'],
['E05','HORSES3D-GPU','P03','PDF p18 Fig7 discussion','TGV KEP p=5; 16384 hex/GPU; 1000 steps','H100 MareNostrum 5; 64 GB HBM2e','256 GPUs','4 GPUs / one node','weak scaling efficiency','approximately 0.90','ratio','fixed spatial DoFs/GPU','preprint-text','not measured on DCU; not 2048-GPU efficiency'],
['E06','HORSES3D-GPU','P03','PDF p15–16 Fig4 discussion','TGV p=3–7; SDG/KEP','H100 64 GB','1 GPU','highest tested load at each p','load reaching about 90% of best throughput','16384','elements/GPU','per-p comparison; not CPU speedup','preprint-text','hardware and discretization dependent'],
['E07','HiFiLES','README','README.md line23','not fully stated','not stated','up to 16 GPUs','not fully stated','strong / weak scalability claim','0.88 / above 0.90','ratio','missing hardware/problem/timing context','official-README-incomplete','exclude from strict cross-code ranking'],
['E08','MFEM LOR','P06','PDF p16 section4.4','1.1e9 DoF high-order problem; low-order-refined preconditioning','V100 SXM2','256 GPUs','weak scaling study baseline; see Fig10','setup / solve weak scaling efficiency','0.83 / 0.87','ratio','setup and solve timed separately','published-text','not compressible DG full solver'],
['E09','MARBL/MFEM','P07','PDF p11 section4.2 / Fig3','3D shaped charge ALE+TMOP','12 V100 GPUs; 16 GB each','12 GPUs total','initial performant implementation','aggregate device memory before / after','181 / 97.3','GB','sum across 12 GPUs; not per GPU','published-text','application-level result'],
['E10','GALAEXI APU','P10','PDF p3–4 Fig1','uniform periodic Cartesian; p=9; 4.096M DoF/APU;10 RK steps','MI300A Hunter; SPX mode','512 APUs','one node','weak scaling efficiency','0.904','ratio','2.097e9 global spatial DoFs','preprint-text','paper version; public main code differs'],
['E11','GALAEXI APU','P10','PDF p4 section2.3','explicit DGSEM','MI300A','application memory statement','none','memory per one million DoFs','approximately 1.2','GB per 1M DoF','paper units preserved','preprint-text','cannot directly compare KiB with GB without convention'],
]
fields=['evidence_id','software','source_id','locator','problem','hardware','scale','baseline','metric','value','unit','timing_or_definition','evidence_type','caveat']
with (R/'analysis/raw_data/性能证据表.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.writer(f);w.writerow(fields);w.writerows(rows)
(R/'metadata/performance_evidence.json').write_text(json.dumps([dict(zip(fields,r)) for r in rows],ensure_ascii=False,indent=2))
with (R/'analysis/raw_data/PyFR强扩展原始表.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['platform','ranks','physical_GPUs','GDoF_per_s_as_paper','speedup_vs_16_ranks','efficiency','source'])
 for name,div,t,sp,eff in [('Frontier_MI250X',2,[26.21,50.87,98.70,193.37,369.10,669.80,1133.48,1537.68],[1,1.94,3.77,7.38,14.08,25.56,43.25,58.68],[1,.97,.94,.92,.88,.80,.68,.46]),('Alps_GH200',1,[96.07,199.60,404.73,806.95,1599.12,2861.56,4632.03,5753.96],[1,2.08,4.21,8.40,16.64,29.79,48.21,59.89],[1,1.04,1.05,1.05,1.04,.93,.75,.47])]:
  for n,a,b,c in zip([16,32,64,128,256,512,1024,2048],t,sp,eff):w.writerow([name,n,n//div,a,b,c,'P01 PDF p17'])
with (R/'analysis/raw_data/GALAEXI显存原始表.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['polynomial_degree','KiB_per_spatial_DoF','source'])
 for i,v in enumerate([1.457,1.188,1.049,.996,.942,.895,.869,.841,.827,.808,.801,.787],1):w.writerow([i,v,'P02 PDF p13 Table2'])
# This is intentionally a header-only experiment template: no invented runs.
with (R/'analysis/raw_data/后续实测记录模板.csv').open('w',encoding='utf-8-sig',newline='') as f:
 csv.writer(f).writerow(['run_id','software','commit','case','equations','mesh_sha256','element_types','polynomial_degree','space_accuracy_order','node_count','nvar','scalar_dof','precision','hardware','gpu_count','gcd_per_gpu','mpi_ranks','cpu_baseline_cores','compiler','backend','driver','mpi','gpu_aware_mpi','time_integrator','dt','steps','nonlinear_tolerance','linear_tolerance','iterations','correctness_error','warmup','timing_scope','setup_s','solve_s','mpi_s','io_s','total_s','peak_allocated_bytes','peak_device_used_bytes','repeat_id','log_path'])
