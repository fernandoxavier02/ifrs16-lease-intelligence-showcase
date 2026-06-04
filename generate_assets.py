"""Generate professional mockup images for IFRS 16 showcase."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from decimal import Decimal
import sys
sys.path.insert(0, "D:/ifrs16-lease-intelligence-showcase/prototype")
from models import LeaseInputs
from engine import calcular_lease

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

OUTPUT = "D:/ifrs16-lease-intelligence-showcase/assets"

def save(fig, name, sub="screenshots"):
    fig.savefig(f"{OUTPUT}/{sub}/{name}", dpi=180, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"[ASSET] {name}")

# Pre-calc data
imovel = LeaseInputs("Galpao", "IM", 60, 0, Decimal("8500"), Decimal("9.5"), Decimal("4.5"), 1)
res = calcular_lease(imovel)
months = [s.mes for s in res.schedule]
passivos = [float(s.passivo_final) for s in res.schedule]
ativos = [float(s.ativo_liquido) for s in res.schedule]
juros = [float(s.juros) for s in res.schedule]
amort = [float(s.amortizacao) for s in res.schedule]

# 1. Dashboard
fig = plt.figure(figsize=(14, 8))
fig.patch.set_facecolor('#f8f9fa')
ax_title = fig.add_axes([0, 0.92, 1, 0.08])
ax_title.set_facecolor('#1565C0')
ax_title.text(0.5, 0.5, 'IFRS 16 Lease Intelligence Dashboard', fontsize=18, fontweight='bold', color='white', ha='center', va='center')
ax_title.set_xticks([]); ax_title.set_yticks([]); ax_title.spines[:].set_visible(False)

kpis = [
    ('ROU Asset', f'R$ {float(res.vp_total):,.0f}', '#2E7D32'),
    ('Lease Liability CP', f'R$ {float(res.schedule[0].passivo_cp):,.0f}', '#C62828'),
    ('Lease Liability LP', f'R$ {float(res.schedule[0].passivo_lp):,.0f}', '#E65100'),
    ('Total AVP', f'R$ {float(res.avp):,.0f}', '#6A1B9A'),
]
for i, (label, value, color) in enumerate(kpis):
    ax = fig.add_axes([0.03 + i*0.24, 0.72, 0.22, 0.17])
    ax.set_facecolor('white')
    rect = FancyBboxPatch((0,0),1,1, boxstyle="round,pad=0.02", facecolor='white', edgecolor=color, linewidth=3, transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(0.5, 0.6, value, fontsize=20, fontweight='bold', color=color, ha='center', va='center', transform=ax.transAxes)
    ax.text(0.5, 0.25, label, fontsize=10, color='#555', ha='center', va='center', transform=ax.transAxes)
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_xticks([]); ax.set_yticks([]); ax.spines[:].set_visible(False)

ax_chart = fig.add_axes([0.08, 0.12, 0.84, 0.54])
ax_chart.plot(months, passivos, label='Lease Liability', color='#C62828', linewidth=2.5)
ax_chart.plot(months, ativos, label='ROU Asset (Liquido)', color='#2E7D32', linewidth=2.5)
ax_chart.fill_between(months, passivos, alpha=0.1, color='#C62828')
ax_chart.fill_between(months, ativos, alpha=0.1, color='#2E7D32')
ax_chart.set_xlabel('Mes', fontsize=11)
ax_chart.set_ylabel('Valor (BRL)', fontsize=11)
ax_chart.set_title('Evolucao do Passivo e Ativo ao longo do prazo do contrato', fontsize=12, fontweight='bold')
ax_chart.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
ax_chart.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,p: f'R${x/1000:.0f}k'))
ax_chart.grid(axis='y', alpha=0.3, linestyle='--')
ax_chart.spines['top'].set_visible(False)
ax_chart.spines['right'].set_visible(False)

ax_foot = fig.add_axes([0, 0, 1, 0.05])
ax_foot.set_facecolor('#1565C0')
ax_foot.text(0.5, 0.5, 'IFRS 16 Lease Intelligence v1.8.2 | Contrato: Galpao Logistica Centro | Usuario: controller@empresa.ficticia', fontsize=9, color='white', ha='center', va='center')
ax_foot.set_xticks([]); ax_foot.set_yticks([]); ax_foot.spines[:].set_visible(False)

save(fig, '01-lease-dashboard.png')

# 2. Amortization Schedule stacked area
fig, ax = plt.subplots(figsize=(14, 7))
ax.stackplot(months[:36], [juros[:36], amort[:36]], labels=['Juros', 'Amortizacao'], colors=['#FF9800', '#1976D2'], alpha=0.85)
ax.set_xlabel('Mes', fontsize=11)
ax.set_ylabel('Valor (BRL)', fontsize=11)
ax.set_title('Composicao da Parcela Mensal — Juros vs Amortizacao (primeiros 36 meses)', fontsize=13, fontweight='bold')
ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,p: f'R${x:,.0f}'))
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout()
save(fig, '02-amortization-schedule.png')

# 3. ROU vs Liability
fig, ax = plt.subplots(figsize=(12, 6))
width = 0.35
x = np.arange(1, 13)
rou_vals = [ativos[i-1] for i in range(1, 13)]
liab_vals = [passivos[i-1] for i in range(1, 13)]
ax.bar(x - width/2, rou_vals, width, label='ROU Asset (Liquido)', color='#2E7D32', edgecolor='white')
ax.bar(x + width/2, liab_vals, width, label='Lease Liability', color='#C62828', edgecolor='white')
ax.set_xlabel('Mes', fontsize=11)
ax.set_ylabel('Valor (BRL)', fontsize=11)
ax.set_title('ROU Asset vs Lease Liability — Comparativo Mensal (Ano 1)', fontsize=13, fontweight='bold')
ax.set_xticks(x)
ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,p: f'R${x/1000:.0f}k'))
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout()
save(fig, '03-rou-liability-chart.png')

# 4. Architecture
fig, ax = plt.subplots(figsize=(13, 9))
ax.set_xlim(0, 13); ax.set_ylim(0, 9); ax.axis('off'); fig.patch.set_facecolor('white')

def box(x,y,w,h,c,t,s="",tc='white'):
    r = FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.05",facecolor=c,edgecolor='white',linewidth=2)
    ax.add_patch(r)
    ax.text(x+w/2,y+h/2+0.15,t,fontsize=9,fontweight='bold',color=tc,ha='center',va='center')
    if s: ax.text(x+w/2,y+h/2-0.25,s,fontsize=7,color=tc,ha='center',va='center',alpha=0.9)

def arrow(x1,y1,x2,y2,c='#888'):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='->',color=c,lw=1.5))

ax.text(6.5,8.7,'IFRS 16 Lease Intelligence — Architecture',fontsize=14,fontweight='bold',color='#1a1a1a',ha='center')

ax.text(0.5,8.0,'CLIENT LAYER',fontsize=10,fontweight='bold',color='#555')
box(1,7.2,2.5,0.6,'#1565C0','Firebase Hosting','Web App')
box(4,7.2,2.5,0.6,'#1565C0','Admin Dashboard','RBAC')
box(7,7.2,2.5,0.6,'#1565C0','Stripe Portal','Billing')
box(10,7.2,2.5,0.6,'#1565C0','API Docs','/docs')

box(3.5,6.0,6,0.6,'#6A1B9A','Cloud Run — FastAPI','Auto-scaling · Stateless')

ax.text(0.5,5.3,'APPLICATION',fontsize=10,fontweight='bold',color='#555')
box(1,4.2,2.5,0.9,'#2E7D32','Auth\nJWT + License','Session Manager')
box(3.8,4.2,2.5,0.9,'#2E7D32','Contracts\nCRUD + Versions','Immutable History')
box(6.6,4.2,2.5,0.9,'#2E7D32','Calc Engine\nPV + Schedule','IFRS 16 Formula')
box(9.4,4.2,2.5,0.9,'#2E7D32','Stripe\nWebhook Handler','Sync Billing')

ax.text(0.5,3.5,'DATA LAYER',fontsize=10,fontweight='bold',color='#555')
box(1,2.4,3.5,0.9,'#E65100','PostgreSQL 14+','Supabase · RLS · Multi-tenant')
box(5,2.4,3.5,0.9,'#E65100','Audit Log','Append-only · Versioned')
box(9,2.4,3,0.9,'#E65100','Economic Indexes','IGPM · IPCA · SELIC · CDI')

ax.text(0.5,1.7,'EXTERNAL',fontsize=10,fontweight='bold',color='#555')
box(3,0.8,3,0.7,'#455A64','Stripe API','Payments · Subscriptions')
box(7,0.8,3,0.7,'#455A64','BCB API','Selic · CDI · IGPM')

save(fig, '04-architecture-diagram.png', sub='diagrams')

# 5. Stripe Billing
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_facecolor('#f8f9fa')
plans = ['Basic', 'Pro', 'Enterprise']
subs = [42, 18, 5]
mrr = [4200, 9000, 7500]
colors = ['#42A5F5', '#1565C0', '#0D47A1']

x = np.arange(len(plans))
width = 0.35
ax2 = ax.twinx()
bars1 = ax.bar(x - width/2, subs, width, label='Assinaturas Ativas', color=colors, edgecolor='white', alpha=0.85)
bars2 = ax2.bar(x + width/2, mrr, width, label='MRR (BRL)', color=colors, edgecolor='white', alpha=0.5, hatch='//')

ax.set_xlabel('Plano', fontsize=11)
ax.set_ylabel('Assinaturas', fontsize=11)
ax2.set_ylabel('MRR (BRL)', fontsize=11)
ax.set_title('Stripe Billing — Distribuicao de Planos e MRR', fontsize=13, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(plans)
ax.legend(loc='upper left'); ax2.legend(loc='upper right')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False); ax2.spines['top'].set_visible(False)
plt.tight_layout()
save(fig, '05-stripe-billing.png')

# 6. Journal Entries
fig, ax = plt.subplots(figsize=(13, 7))
ax.set_facecolor('#fafafa')
ax.set_xlim(0, 13); ax.set_ylim(0, 8); ax.axis('off')

ax.text(6.5, 7.5, 'Lancamentos Contabeis IFRS 16 — Reconhecimento Inicial', fontsize=14, fontweight='bold', color='#1a1a1a', ha='center')
ax.text(6.5, 7.0, 'Contrato: Galpao Logistica Centro | VP Total: R$ 403,847.23', fontsize=10, color='#666', ha='center')

entries = [
    ('RECONHECIMENTO INICIAL', [
        ('D - Ativo de Direito de Uso (ROU)', '403,847.23', ''),
        ('C - Passivo de Arrendamento (CP)', '', '48,215.40'),
        ('C - Passivo de Arrendamento (LP)', '', '355,631.83'),
    ]),
    ('MES 1 — JUROS E DEPRECIACAO', [
        ('D - Despesa de Juros (DRE)', '3,197.13', ''),
        ('D - Despesa de Depreciacao (DRE)', '6,730.79', ''),
        ('C - Passivo de Arrendamento', '', '3,197.13'),
        ('C - Depreciacao Acumulada', '', '6,730.79'),
    ]),
]

y = 5.8
for title, rows in entries:
    ax.text(0.5, y, title, fontsize=11, fontweight='bold', color='#1565C0')
    y -= 0.4
    for conta, deb, cred in rows:
        ax.text(1.0, y, conta, fontsize=9, color='#333')
        ax.text(8.5, y, deb, fontsize=9, color='#2E7D32', ha='right', family='monospace')
        ax.text(11.5, y, cred, fontsize=9, color='#C62828', ha='right', family='monospace')
        y -= 0.35
    y -= 0.3

# Table header line
ax.plot([0.8, 12], [6.1, 6.1], color='#ddd', linewidth=1)
ax.text(8.5, 6.25, 'Debito', fontsize=8, fontweight='bold', color='#666', ha='right')
ax.text(11.5, 6.25, 'Credito', fontsize=8, fontweight='bold', color='#666', ha='right')

save(fig, '06-journal-entries.png')

print("\n[INFO] All IFRS 16 assets generated successfully!")
