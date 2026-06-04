# Demo — Protótipo Educacional IFRS 16

> Protótipo didático do motor de cálculo IFRS 16. Sem multi-tenant, auth, Stripe ou dashboard web.

---

## Pré-requisitos

- Python 3.11+

---

## Execução

```bash
cd prototype
python main.py
```

---

## O que o protótipo faz

### Contratos pré-carregados (dados 100% sintéticos)

| # | Tipo | Prazo | Parcela | Taxa Anual | Índice |
|---|------|-------|---------|------------|--------|
| 1 | Imóvel Comercial | 60 meses | R$ 8.500 | 9,5% | IPCA |
| 2 | Frota de Veículos | 36 meses | R$ 3.200 | 11,0% | IGPM |

### Saída esperada

```
=== Contrato 1: Imóvel Comercial ===
Valor Presente Total:    R$ 403,847.23
ROU Asset:               R$ 403,847.23
Lease Liability CP:      R$  48,215.40
Lease Liability LP:      R$ 355,631.83

Schedule (primeiros 6 meses):
Mes 1:  Parcela R$ 8,500.00 | Juros R$ 3,197.13 | Amort R$ 5,302.87 | Passivo R$ 398,544.36 | Deprec R$ 6,730.79
Mes 2:  Parcela R$ 8,500.00 | Juros R$ 3,155.14 | Amort R$ 5,344.86 | Passivo R$ 393,199.50 | Deprec R$ 6,730.79
...
```

---

## Limitações vs. Produção

| Funcionalidade | Protótipo | Produção |
|---|---|---|
| Banco de dados | JSON em memória | PostgreSQL + RLS |
| Auth | Nenhuma | JWT + License Manager |
| Stripe Billing | Não | Basic/Pro/Enterprise |
| Remensuração por índice | Fixa | Automática (IGPM, IPCA, SELIC, CDI, INPC, TR) |
| Dashboard Web | Não | HTML5 + Tailwind + Firebase |
| Multi-tenant | Não | Sim |
| Audit Trail | Não | Append-only versionado |

---

## Disclaimer

Dados 100% fictícios. Empresas, CNPJs e valores são simulados para fins educacionais.
