# Jupyter-ready Python code: cálculo del NPV y análisis solicitado.
import numpy as np
import pandas as pd

# Parámetros
monthly_cost = 1000.0          # costo mensual original
months_original = 12
r = 0.01                       # tasa efectiva mensual
terminal_value = 18000.0       # valor al final del proyecto (valor presente de los flujos futuros)
currency = "$"

def pv_amount(amount, month, r):
    """Valor presente de una cantidad 'amount' que ocurre en 'month' (meses desde inicio)"""
    return amount / ((1 + r) ** month)

def npv_for_schedule(monthly_cost, months, terminal_value, r):
    """Calcula NPV dado costo mensual pagado al final de cada mes (meses 1..months)
       y un ingreso terminal en el mes 'months' igual a terminal_value."""
    outflows_pv = sum(pv_amount(monthly_cost, t, r) for t in range(1, months+1))
    terminal_pv = pv_amount(terminal_value, months, r)
    npv = -outflows_pv + terminal_pv
    return {
        "npv": npv,
        "pv_investment": outflows_pv,
        "terminal_pv": terminal_pv
    }

# a) NPV escenario original (12 meses)
res_a = npv_for_schedule(monthly_cost, months_original, terminal_value, r)

# b) Extensión 3 meses (total 15 meses) mismo costo mensual, ingreso terminal en mes 15
months_b = months_original + 3
res_b = npv_for_schedule(monthly_cost, months_b, terminal_value, r)

# c) Rentabilidad = NPV / PV_investment para cada caso
rent_a = res_a["npv"] / res_a["pv_investment"]
rent_b = res_b["npv"] / res_b["pv_investment"]

# d) Retraso en 6 meses: escenario de 18 meses (12 + 6)
months_delay6 = months_original + 6
res_delay6 = npv_for_schedule(monthly_cost, months_delay6, terminal_value, r)
delta_npv_delay6 = res_delay6["npv"] - res_a["npv"]
pct_change_npv_delay6 = 100.0 * delta_npv_delay6 / res_a["npv"] if res_a["npv"] != 0 else np.nan

# e) Análisis coste adicional 5% mensual para garantizar calendario original
monthly_cost_mgr = monthly_cost * 1.05
res_mgr = npv_for_schedule(monthly_cost_mgr, months_original, terminal_value, r)
rent_mgr = res_mgr["npv"] / res_mgr["pv_investment"]

# f) Desafío: si el proyecto se extiende a 15 meses (3 meses extra) y se desea
#    obtener la misma utilidad (NPV) que el caso original, cuál es el valor mensual máximo aceptable?
npv_target = res_a["npv"]
# Factor presente de una anualidad mensual descontada = sum_{t=1..15} 1/(1+r)^t
pv_factor_15 = sum(1.0/((1+r)**t) for t in range(1, months_b+1))
terminal_pv_15 = pv_amount(terminal_value, months_b, r)
# Ecuación: npv_target = -c * pv_factor_15 + terminal_pv_15  => c = (terminal_pv_15 - npv_target) / pv_factor_15
c_accept = (terminal_pv_15 - npv_target) / pv_factor_15

# Preparar tabla resumen
summary = pd.DataFrame([
    {"Escenario": "Original - 12 meses", "Meses": months_original, "Costo mensual": monthly_cost,
     "NPV": res_a["npv"], "PV inversión": res_a["pv_investment"], "Rentabilidad (NPV/PV_inv)": rent_a},
    {"Escenario": "Extendido +3 meses - 15 meses", "Meses": months_b, "Costo mensual": monthly_cost,
     "NPV": res_b["npv"], "PV inversión": res_b["pv_investment"], "Rentabilidad (NPV/PV_inv)": rent_b},
    {"Escenario": "Retraso +6 meses - 18 meses", "Meses": months_delay6, "Costo mensual": monthly_cost,
     "NPV": res_delay6["npv"], "PV inversión": res_delay6["pv_investment"], "Rentabilidad (NPV/PV_inv)": (res_delay6["npv"]/res_delay6["pv_investment"])},
    {"Escenario": "Con gestor (+5% costo mensual) - 12 meses", "Meses": months_original, "Costo mensual": monthly_cost_mgr,
     "NPV": res_mgr["npv"], "PV inversión": res_mgr["pv_investment"], "Rentabilidad (NPV/PV_inv)": rent_mgr},
])

# Mostrar resultados formateados
pd.options.display.float_format = '{:,.2f}'.format
print("=== Resumen numérico ===\n")
display(summary)

print("\n=== Detalles adicionales ===\n")
print(f"a) NPV escenario original (12 meses): {currency}{res_a['npv']:.2f}")
print(f"   PV de la inversión (suma PV de outflows): {currency}{res_a['pv_investment']:.2f}")
print(f"   PV del valor terminal en mes 12: {currency}{res_a['terminal_pv']:.2f}")
print()
print(f"b) NPV escenario extendido 3 meses (15 meses): {currency}{res_b['npv']:.2f}")
print(f"   PV de la inversión (15 meses): {currency}{res_b['pv_investment']:.2f}")
print(f"   PV del valor terminal en mes 15: {currency}{res_b['terminal_pv']:.2f}")
print()
print(f"c) Rentabilidades:")
print(f"   - Caso original: {rent_a*100:.2f}%")
print(f"   - Caso extendido +3 meses: {rent_b*100:.2f}%")
print()
print(f"d) Impacto de retraso de 6 meses (18 meses):")
print(f"   - NPV en 18 meses: {currency}{res_delay6['npv']:.2f}")
print(f"   - Cambio absoluto respecto a original: {currency}{delta_npv_delay6:.2f}")
print(f"   - Cambio porcentual respecto a original: {pct_change_npv_delay6:.2f}%")
print()
print(f"e) Con gerente (5% costo mensual adicional) - NPV: {currency}{res_mgr['npv']:.2f}")
print(f"   PV inversión (con gerente): {currency}{res_mgr['pv_investment']:.2f}")
print(f"   Rentabilidad (con gerente): {rent_mgr*100:.2f}%")
print(f"   Comparación: NPV con gestor vs NPV sin gestor (original): {currency}{res_mgr['npv'] - res_a['npv']:.2f}")
print()
print(f"f) Desafío - costo mensual máximo aceptable para igualar NPV original si el proyecto dura 15 meses:")
print(f"   - Costo mensual máximo aceptable: {currency}{c_accept:.2f} por mes (comparado con {currency}{monthly_cost:.2f} original)")
print()
print("Notas:")
print("- Todas las entradas de costo mensual se asumen pagadas al final de cada mes (vencido).")
print("- El terminal_value se asume pagado una única vez al final del periodo (mes correspondiente).")
print("- Rentabilidad = NPV / PV_inversión (ambos en valor presente).")

