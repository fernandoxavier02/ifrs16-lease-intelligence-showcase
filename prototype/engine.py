"""Engine - IFRS 16 Lease Intelligence Prototype."""

from decimal import Decimal, ROUND_HALF_UP
from typing import List
from models import LeaseInputs, ScheduleEntry, LeaseResult


def calcular_lease(inputs: LeaseInputs) -> LeaseResult:
    """
    Motor de calculo IFRS 16:
    1. Calcula taxa mensal a partir da taxa anual
    2. Gera fluxo de caixa com reajustes anuais
    3. Calcula Valor Presente (VP) - base para ROU Asset e Lease Liability
    4. Gera schedule de amortizacao mensal
    5. Calcula split CP/LP (curto prazo / longo prazo)
    """
    # Taxa mensal efetiva
    taxa_mensal = (Decimal(1) + inputs.taxa_anual / Decimal(100)) ** (Decimal(1) / Decimal(12)) - Decimal(1)
    taxa_mensal = taxa_mensal.quantize(Decimal("0.00000001"))

    # Fluxo de caixa
    fluxo = []
    total_nominal = Decimal("0")
    total_vp = Decimal("0")

    for mes in range(1, inputs.prazo_meses + 1):
        parcela = Decimal("0")
        if mes > inputs.carencia_meses:
            reajustes = (mes - 1) // 12
            parcela = inputs.parcela_inicial * ((Decimal(1) + inputs.reajuste_anual / Decimal(100)) ** reajustes)
            parcela = parcela.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        fator_desconto = Decimal(1) / ((Decimal(1) + taxa_mensal) ** mes)
        vp = (parcela * fator_desconto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        total_nominal += parcela
        total_vp += vp
        fluxo.append({"mes": mes, "parcela": parcela, "vp": vp})

    total_nominal = total_nominal.quantize(Decimal("0.01"))
    total_vp = total_vp.quantize(Decimal("0.01"))
    avp = (total_nominal - total_vp).quantize(Decimal("0.01"))

    # ROU Asset = VP total
    rou_asset = total_vp
    deprec_mensal = (rou_asset / inputs.prazo_meses).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Schedule de amortizacao
    schedule = []
    passivo_atual = total_vp
    deprec_acumulada = Decimal("0")

    for mes in range(1, inputs.prazo_meses + 1):
        passivo_inicial = passivo_atual
        juros = (passivo_inicial * taxa_mensal).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        pagamento = fluxo[mes - 1]["parcela"]
        amortizacao = (pagamento - juros).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        passivo_final = (passivo_inicial + juros - pagamento).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if passivo_final < 0:
            passivo_final = Decimal("0")

        deprec_acumulada += deprec_mensal
        ativo_liquido = (rou_asset - deprec_acumulada).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if ativo_liquido < 0:
            ativo_liquido = Decimal("0")

        # CP/LP split: CP = soma das amortizacoes dos proximos 12 meses (ou restante)
        cp = Decimal("0")
        for i in range(mes, min(mes + 12, inputs.prazo_meses + 1)):
            if i <= inputs.prazo_meses:
                cp += fluxo[i - 1]["parcela"]
        cp = cp.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        passivo_cp = min(passivo_final, max(cp, Decimal("0"))).quantize(Decimal("0.01"))
        passivo_lp = (passivo_final - passivo_cp).quantize(Decimal("0.01"))
        if passivo_lp < 0:
            passivo_lp = Decimal("0")

        schedule.append(ScheduleEntry(
            mes=mes,
            parcela=pagamento,
            juros=juros,
            amortizacao=amortizacao,
            passivo_inicial=passivo_inicial,
            passivo_final=passivo_final,
            ativo_bruto=rou_asset,
            deprec_acumulada=deprec_acumulada,
            ativo_liquido=ativo_liquido,
            passivo_cp=passivo_cp,
            passivo_lp=passivo_lp,
        ))

        passivo_atual = passivo_final

    return LeaseResult(
        inputs=inputs,
        taxa_mensal=taxa_mensal,
        vp_total=total_vp,
        total_nominal=total_nominal,
        avp=avp,
        schedule=schedule,
    )
