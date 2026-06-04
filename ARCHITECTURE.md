# Arquitetura — IFRS 16 Lease Intelligence

> Documentação arquitetural de alto nível do sistema de produção.

---

## 1. Visão Geral

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Web App    │  │  Admin      │  │  API Docs   │  │  Stripe Portal      │ │
│  │  (Firebase) │  │  Dashboard  │  │  (/docs)    │  │  (Billing)          │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
└─────────┼────────────────┼────────────────┼────────────────────┼────────────┘
          └────────────────┴────────────────┴────────────────────┘
                                    │
                    ┌───────────────▼────────────────┐
                    │      Firebase Hosting / CDN      │
                    └───────────────┬────────────────┘
                                    │
┌───────────────────────────────────▼─────────────────────────────────────────┐
│                            APPLICATION LAYER                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     FastAPI Application (Cloud Run)                  │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │  Auth    │ │ Contracts│ │  Calc    │ │  Stripe  │ │  Admin   │  │   │
│  │  │  (JWT)   │ │  (CRUD)  │ │  Engine  │ │  (Billing)│ │  (RBAC)  │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  │                                                                      │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────────┐   │   │
│  │  │  Remeas. │ │  Journal │ │  License │ │  Notification        │   │   │
│  │  │  Service │ │  Entries │ │  Manager │ │  Service             │   │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼─────────────────────────────────────────┐
│                              DATA LAYER                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    PostgreSQL 14+ (Supabase)                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │   │
│  │  │  users      │  │  contracts  │  │  versions   │  │  economic  │ │   │
│  │  │  (JWT)      │  │  (lease)    │  │  (history)  │  │  indexes   │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │   │
│  │                                                                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │   │
│  │  │  licenses   │  │subscriptions│  │  audit_log  │  │  configs   │ │   │
│  │  │  (Stripe)   │  │  (Stripe)   │  │  (immutable)│  │  (RLS)     │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Domain Model — IFRS 16 Calculation Engine

```
┌─────────────────┐       ┌─────────────────────────┐       ┌─────────────────┐
│    Contract     │1─────N│    Contract Version     │1─────N│  Calc Result    │
├─────────────────┤       ├─────────────────────────┤       ├─────────────────┤
│ id              │       │ id                      │       │ id              │
│ user_id (FK)    │       │ contract_id (FK)        │       │ version_id (FK) │
│ name            │       │ version_number          │       │ month           │
│ categoria       │       │ data_inicio             │       │ parcela         │
│ status          │       │ prazo_meses             │       │ juros           │
│ is_deleted      │       │ carencia_meses          │       │ amortizacao     │
└─────────────────┘       │ parcela_inicial         │       │ passivo_final   │
                          │ taxa_desconto_anual     │       │ ativo_liquido   │
                          │ reajuste_tipo           │       │ depreciacao     │
                          │ reajuste_valor          │       │ passivo_cp      │
                          │ resultados_json         │       │ passivo_lp      │
                          └─────────────────────────┘       └─────────────────┘
```

---

## 3. Fórmulas do Motor de Cálculo

### Valor Presente (VP)
```
VP = Σ (Parcela_mes / (1 + taxa_mensal)^mes)

taxa_mensal = (1 + taxa_anual)^(1/12) - 1
```

### ROU Asset e Lease Liability (Reconhecimento Inicial)
```
ROU Asset = VP total dos pagamentos
Lease Liability (CP) = Soma das amortizações dos próximos 12 meses
Lease Liability (LP) = Saldo devedor total - CP
```

### Schedule Mensal
```
Juros_mes = Passivo_inicial × taxa_mensal
Amortizacao_mes = Pagamento_mes - Juros_mes
Passivo_final = Passivo_inicial + Juros_mes - Pagamento_mes
Depreciacao_mes = VP_total / prazo_meses
Ativo_liquido = VP_total - Depreciacao_acumulada
```

### Remensuração por Índice
```
Novo_VP = VP_original × (1 + variacao_indice)
Ajuste = Novo_VP - VP_original
```

---

## 4. Decisões Arquiteturais (ADRs)

### ADR-001 — Firebase Hosting + Cloud Run
**Contexto:** Separar frontend estático do backend dinâmico para escalabilidade independente.
**Decisão:** Firebase Hosting para frontend (cache global CDN) + Cloud Run para backend (scale-to-zero).
**Consequência:** Custo reduzido em períodos de baixo uso; deploy independente.

### ADR-002 — Supabase PostgreSQL com RLS
**Contexto:** Multi-tenant com dados financeiros sensíveis.
**Decisão:** Row-Level Security no PostgreSQL + `user_id` em todas as tabelas.
**Consequência:** Isolamento garantido a nível de banco; queries simplificadas.

### ADR-003 — Versionamento Imutável de Contratos
**Contexto:** Auditoria exige rastreabilidade de toda alteração em contrato.
**Decisão:** Tabela `contract_versions` append-only. Edição cria nova versão; delete lógico apenas.
**Consequência:** Histórico completo para auditoria; volume de dados cresce com versões.

### ADR-004 — Stripe para Billing e Licenciamento
**Contexto:** Necessidade de cobrar por uso/plano sem construir sistema de pagamento próprio.
**Decisão:** Stripe Checkout + Customer Portal + Webhooks para sincronização de assinaturas.
**Consequência:** Compliance PCI-DSS delegada à Stripe; menor time-to-market.
