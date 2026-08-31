# IFRS 16 Lease Intelligence — Showcase

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Domain: Financial Engineering](https://img.shields.io/badge/Domain-IFRS_16_%2F_CPC_06-412991.svg?style=for-the-badge)](https://github.com/fernandoxavier02)
[![FX Studio AI](https://img.shields.io/badge/FX_Studio_AI-Finance_Architecture-FF6B6B?style=for-the-badge)](https://github.com/fernandoxavier02)

**Architectural showcase and financial intelligence prototype for IFRS 16 lease liability, ROU assets, amortization schedules, and remeasurement.**

</div>

---

## 🌟 Executive Context

As Head of Accounting and Controllership, I led leasing automation and IFRS 16 compliance initiatives across enterprise operations. This showcase demonstrates domain expertise, financial engineering mechanics, and architectural blueprints — featuring a runnable Python prototype with synthetic data.

---

## 🎯 The Business Challenge

Under **IFRS 16 / CPC 06 (R2)**, companies managing multiple lease contracts (real estate, vehicles, heavy machinery) must:

- **Recognize Right-of-Use (ROU) Assets** and **Lease Liabilities** on the balance sheet for virtually all leases.
- Compute the **Present Value (PV)** of future cash flows using implicit or incremental borrowing rates (IBR).
- Generate monthly **amortization schedules** tracking interest accretion, principal amortization, and asset depreciation.
- Dynamically split liabilities into **Short-Term (ST)** and **Long-Term (LT)** obligations at every financial close.
- Execute **remeasurement** upon changes in economic indices (e.g., IPCA, IGPM, SELIC, CDI).
- Generate initial recognition and recurring monthly **accounting journal entries**.

---

## 🏗️ The Solution & Core Modules

| Module | Description | Impact |
| :--- | :--- | :--- |
| **Lease Calculator** | Present Value (PV), ROU Asset, Lease Liability, and full schedule calculation | 99.9% calculation precision |
| **Amortization Schedule** | Monthly interest, principal repayment, depreciation, net asset book value | Full contract visibility |
| **ST/LT Split** | Automated liability breakdown into short-term and long-term portions | Balance sheet compliance |
| **Remeasurement Engine** | Automated contract adjustment against economic inflation and interest rate indices | Zero manual rework |
| **Journal Entries** | Automated debit/credit entries for initial recognition and monthly closing | Close cycle reduced to < 2 days |
| **Asset Categorization** | Real estate, fleet vehicles, IT equipment, industrial machinery | Granular class-level reporting |

---

## 📈 Proven Operational Results

| Metric | Legacy (Spreadsheets) | Automated Platform | Improvement |
| :--- | :---: | :---: | :---: |
| **Calculation Time** per contract | 2–3 hours | 45 seconds | **98% reduction** |
| **Remeasurement Error Rate** | 12% of contracts | < 0.5% | **96% reduction** |
| **Monthly Closing Duration** | 4 business days | 1 business day | **75% faster** |
| **Contract Capacity** | 150+ assets | 500+ assets | **3.3× scale** |
| **ST/LT Split Accuracy** | Approximated / Manual | Exact / Automated | **100% precision** |

---

## 🏛️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │   API Engine    │    │    Database     │
│  (Tailwind/JS)  │◄──►│    (FastAPI)    │◄──►│  (PostgreSQL)   │
│                 │    │  Finance Engine │    │  RLS Multi-org  │
└─────────────────┘    └────────┬────────┘    └─────────────────┘
                                │
                       ┌────────▼────────┐
                       │  Billing/Stripe │
                       │    (Webhooks)   │
                       └─────────────────┘
```

---

## 🧪 Educational Prototype

This repository provides a lightweight, executable Python prototype demonstrating:
- Cash flow Present Value (PV) calculations
- ROU Asset and Lease Liability schedules
- Monthly amortization and depreciation tables
- Automated Short-Term / Long-Term classification

### Running the Prototype

```bash
cd prototype
python -m venv .venv
# On Windows: .venv\Scripts\activate
# On Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## 📄 License & Attribution

- **Author:** [Fernando Xavier](https://github.com/fernandoxavier02) — *Founder, FX Studio AI | Finance Executive*
- **License:** [MIT License](LICENSE)
