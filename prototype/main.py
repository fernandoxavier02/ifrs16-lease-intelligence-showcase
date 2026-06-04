"""Main - IFRS 16 Lease Intelligence Prototype."""

import json
from decimal import Decimal
from models import LeaseInputs
from engine import calcular_lease


def main():
    print("=" * 70)
    print("IFRS 16 Lease Intelligence - Prototype")
    print("=" * 70)

    contratos = [
        LeaseInputs(
            name="Galpao Logistica Centro",
            categoria="IM",
            prazo_meses=60,
            carencia_meses=0,
            parcela_inicial=Decimal("8500.00"),
            taxa_anual=Decimal("9.5"),
            reajuste_anual=Decimal("4.5"),
            mes_reajuste=1,
        ),
        LeaseInputs(
            name="Frota Entregas Ligeiras",
            categoria="VE",
            prazo_meses=36,
            carencia_meses=3,
            parcela_inicial=Decimal("3200.00"),
            taxa_anual=Decimal("11.0"),
            reajuste_anual=Decimal("0.0"),
            mes_reajuste=1,
        ),
    ]

    for idx, c in enumerate(contratos, 1):
        result = calcular_lease(c)
        print(f"\n>>> Contrato {idx}: {c.name} ({c.categoria})")
        print(f"    Prazo: {c.prazo_meses} meses | Parcela: R$ {c.parcela_inicial:,.2f} | Taxa: {c.taxa_anual}% a.a.")
        print(f"    Valor Presente (ROU Asset / Liability): R$ {result.vp_total:,.2f}")
        print(f"    Total Nominal: R$ {result.total_nominal:,.2f} | AVP: R$ {result.avp:,.2f}")

        entry0 = result.schedule[0]
        print(f"    Liability CP: R$ {entry0.passivo_cp:,.2f} | LP: R$ {entry0.passivo_lp:,.2f}")

        print(f"\n    Schedule (primeiros 6 meses):")
        print(f"    {'Mes':>4} | {'Parcela':>10} | {'Juros':>10} | {'Amort':>10} | {'Passivo':>12} | {'Ativo Liq':>10}")
        print(f"    {'-'*4}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}-+-{'-'*12}-+-{'-'*10}")
        for s in result.schedule[:6]:
            print(f"    {s.mes:>4} | R$ {s.parcela:>7.2f} | R$ {s.juros:>7.2f} | R$ {s.amortizacao:>7.2f} | R$ {s.passivo_final:>9.2f} | R$ {s.ativo_liquido:>7.2f}")

    print("\n" + "=" * 70)
    print("Prototype execution completed successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()
