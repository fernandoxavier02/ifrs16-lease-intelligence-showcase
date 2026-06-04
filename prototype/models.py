"""Models - IFRS 16 Lease Intelligence Prototype."""

from dataclasses import dataclass
from typing import List
from decimal import Decimal


@dataclass
class LeaseInputs:
    name: str
    categoria: str  # IM, VE, EQ, PC, OT
    prazo_meses: int
    carencia_meses: int
    parcela_inicial: Decimal
    taxa_anual: Decimal
    reajuste_anual: Decimal
    mes_reajuste: int


@dataclass
class ScheduleEntry:
    mes: int
    parcela: Decimal
    juros: Decimal
    amortizacao: Decimal
    passivo_inicial: Decimal
    passivo_final: Decimal
    ativo_bruto: Decimal
    deprec_acumulada: Decimal
    ativo_liquido: Decimal
    passivo_cp: Decimal
    passivo_lp: Decimal


@dataclass
class LeaseResult:
    inputs: LeaseInputs
    taxa_mensal: Decimal
    vp_total: Decimal
    total_nominal: Decimal
    avp: Decimal
    schedule: List[ScheduleEntry]
