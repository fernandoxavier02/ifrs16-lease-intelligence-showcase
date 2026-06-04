"""Tests - IFRS 16 Lease Intelligence Prototype."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from decimal import Decimal
from models import LeaseInputs
from engine import calcular_lease


def test_vp_calculation_simple():
    """Contrato simples: 12 meses, R$ 1.000/mes, taxa 0% -> VP = R$ 12.000"""
    c = LeaseInputs(
        name="Test Simple",
        categoria="OT",
        prazo_meses=12,
        carencia_meses=0,
        parcela_inicial=Decimal("1000.00"),
        taxa_anual=Decimal("0"),
        reajuste_anual=Decimal("0"),
        mes_reajuste=1,
    )
    r = calcular_lease(c)
    assert r.vp_total == Decimal("12000.00")
    assert r.total_nominal == Decimal("12000.00")


def test_vp_with_interest():
    """Contrato: 12 meses, R$ 1.000/mes, taxa 12% a.a. -> VP < nominal"""
    c = LeaseInputs(
        name="Test Interest",
        categoria="OT",
        prazo_meses=12,
        carencia_meses=0,
        parcela_inicial=Decimal("1000.00"),
        taxa_anual=Decimal("12.0"),
        reajuste_anual=Decimal("0"),
        mes_reajuste=1,
    )
    r = calcular_lease(c)
    assert r.vp_total < r.total_nominal
    assert r.avp > 0


def test_carencia_period():
    """Carencia de 3 meses: meses 1-3 devem ter parcela zero"""
    c = LeaseInputs(
        name="Test Carencia",
        categoria="VE",
        prazo_meses=12,
        carencia_meses=3,
        parcela_inicial=Decimal("5000.00"),
        taxa_anual=Decimal("10.0"),
        reajuste_anual=Decimal("0"),
        mes_reajuste=1,
    )
    r = calcular_lease(c)
    for s in r.schedule[:3]:
        assert s.parcela == Decimal("0.00")
    assert r.schedule[3].parcela > 0


def test_schedule_amortizes_to_zero():
    """O passivo final do ultimo mes deve ser zero (ou proximo)"""
    c = LeaseInputs(
        name="Test Zero",
        categoria="IM",
        prazo_meses=12,
        carencia_meses=0,
        parcela_inicial=Decimal("2000.00"),
        taxa_anual=Decimal("8.0"),
        reajuste_anual=Decimal("0"),
        mes_reajuste=1,
    )
    r = calcular_lease(c)
    assert r.schedule[-1].passivo_final <= Decimal("1.00")


if __name__ == "__main__":
    test_vp_calculation_simple()
    print("[PASS] test_vp_calculation_simple")
    test_vp_with_interest()
    print("[PASS] test_vp_with_interest")
    test_carencia_period()
    print("[PASS] test_carencia_period")
    test_schedule_amortizes_to_zero()
    print("[PASS] test_schedule_amortizes_to_zero")
    print("\n[SUCCESS] All tests passed!")
